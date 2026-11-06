"""Clasifica documentos descargados en la carpeta de su UT, dentro del repo de su asignatura.

Uso:
    python clasificar.py --plan plan.json        # simula: decide destinos, no mueve nada
    python clasificar.py --ejecutar plan.json    # mueve las entradas con estado "seguro"
    python clasificar.py --papelera plan.json    # manda a la Papelera las descargas "duplicado"

Opciones: --origen (por defecto ~/Downloads), --dev (raíz de los repos, por defecto C:/dev),
--asignaturas (tabla repo -> palabras clave).

Origen: los documentos sueltos se clasifican por su nombre. Una subcarpeta cuyo nombre indica
una asignatura ("ut2 ingles") se recorre entera y su nombre manda sobre el de cada archivo;
sus subcarpetas se conservan dentro de la UT. Las demás subcarpetas se ignoran.

Estados del plan:
    seguro     destino decidido; --ejecutar lo moverá
    dudoso     ninguna asignatura, varias empatadas o sin UT clara: decide Claude o el usuario
    ut-nueva   asignatura clara pero no existe carpeta para esa UT: créala y vuelve a simular
"nombre_opaco": true marca nombres que no dicen qué es el documento (worksheet_524271.pdf).
    duplicado  ya hay un archivo idéntico (mismo hash) en algún repo, con cualquier nombre
    colision   el destino existe con otro contenido, u otra descarga va al mismo sitio
Para resolver una entrada a mano, rellena "destino" (ruta absoluta) y pon "estado": "seguro".
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

# Con python -I la carpeta del script no está en sys.path: hay que añadirla para importar normalizar.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalizar import DOCUMENTOS, normalizar  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
ASIGNATURAS = os.path.join(AQUI, '..', 'skills', 'clasificar-descargas', 'asignaturas.json')
# Número de UT en un nombre ya normalizado: ut3, ut-03, tema-3, unidad-3, unit-3, ra4, session-3
UT_EN_NOMBRE = re.compile(r'(?:^|-)(?:ut|tema|unidad|unit|ra|session|sesion)-?0*(\d+)(?=[a-z]?(?:-|$))')
# Números de UT en el nombre de una carpeta de repo: ut02-…, ut1-…, ut02-ut03-… (cubre dos), ra4a-…, session-1-…
UT_EN_CARPETA = re.compile(r'(?:^|-)(?:ut|ra|session|sesion)-?0*(\d+)(?=[a-z]?(?:-|$))')
# Carpetas de herramientas o generadas: no tienen documentos de clase y pueden ser enormes
PODAR = {'.git', 'node_modules', 'target', '.venv', 'venv', '__pycache__', 'library', 'obj', 'bin'}
# Nombre que no dice qué es: un código largo (worksheet_524271) o sin ninguna palabra (12345)
OPACO = re.compile(r'\d{5,}|^[^a-z]*$')


def hash_de(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b''):
            h.update(bloque)
    return h.hexdigest()


def asignatura(nombre, tabla):
    """Repo con más palabras clave en el nombre. Devuelve (repo o None, candidatos empatados)."""
    texto = f'-{nombre}-'
    puntos = {repo: sum(f'-{normalizar(p)}-' in texto for p in claves) for repo, claves in tabla.items()}
    maximo = max(puntos.values(), default=0)
    empatados = sorted(r for r, p in puntos.items() if p == maximo and p > 0)
    return (empatados[0] if len(empatados) == 1 else None), empatados


def carpetas_de_ut(repo, numero):
    """Carpetas de primer nivel del repo cuyo nombre cubre esa UT."""
    return sorted(d for d in os.listdir(repo)
                  if os.path.isdir(os.path.join(repo, d))
                  and numero in {int(n) for n in UT_EN_CARPETA.findall(d.lower())})


def documentos(origen, tabla):
    """Lista (ruta, subcarpeta a conservar, pista) de cada documento, y las carpetas ignoradas."""
    encontrados, ignoradas = [], []
    for f in sorted(os.listdir(origen)):
        ruta = os.path.join(origen, f)
        if os.path.isfile(ruta):
            encontrados.append((ruta, '', ''))
        elif os.path.isdir(ruta):
            pista = normalizar(f)
            if asignatura(pista, tabla)[0] is None:  # 'netbeans', proyectos descomprimidos…
                ignoradas.append(f)
                continue
            for raiz, dirs, archivos in os.walk(ruta):
                dirs.sort()
                sub = os.path.relpath(raiz, ruta)
                sub = '' if sub == '.' else '/'.join(normalizar(p) for p in sub.split(os.sep))
                encontrados += [(os.path.join(raiz, a), sub, pista) for a in sorted(archivos)]
    return [d for d in encontrados if os.path.splitext(d[0])[1].lower() in DOCUMENTOS], ignoradas


def clasificar(ruta, sub, pista, dev, tabla):
    base, ext = os.path.splitext(os.path.basename(ruta))
    sin_ext = normalizar(base)
    e = {'origen': ruta, 'nombre': normalizar(base, ext), 'repo': None, 'ut': None,
         'destino': None, 'estado': 'dudoso', 'motivo': '', 'candidatos': [],
         'nombre_opaco': bool(OPACO.search(sin_ext))}

    # La carpeta manda sobre el nombre del archivo: el usuario la nombró a propósito
    repo, empatados = asignatura(pista or sin_ext, tabla)
    if not repo:
        e['candidatos'] = empatados
        e['motivo'] = f'empate entre {", ".join(empatados)}' if empatados else 'ninguna palabra clave'
        return e
    e['repo'] = repo
    ruta_repo = os.path.join(dev, repo)
    if not os.path.isdir(os.path.join(ruta_repo, '.git')):
        e['motivo'] = f'{ruta_repo} no existe o no es un repo git: revisa asignaturas.json'
        return e

    uts_pista = {int(n) for n in UT_EN_NOMBRE.findall(pista)}
    uts_nombre = [int(n) for n in UT_EN_NOMBRE.findall(sin_ext)]
    if len(uts_pista) == 1:  # 'ut1 y ut2 ingles' no sirve de pista: decide el nombre del archivo
        e['ut'] = uts_pista.pop()
    elif uts_nombre:
        e['ut'] = uts_nombre[0]
    else:
        e['motivo'] = 'asignatura clara, UT desconocida'
        return e
    uts = carpetas_de_ut(ruta_repo, e['ut'])
    if not uts:
        e['estado'], e['motivo'] = 'ut-nueva', f'{repo} no tiene carpeta para la UT {e["ut"]}'
        return e
    if len(uts) > 1:
        e['candidatos'], e['motivo'] = uts, 'varias carpetas para esa UT'
        return e
    carpeta = os.path.join(ruta_repo, uts[0])
    if os.path.isdir(os.path.join(carpeta, 'apuntes')):
        carpeta = os.path.join(carpeta, 'apuntes')
    e['destino'] = os.path.join(carpeta, *sub.split('/'), e['nombre']) if sub else os.path.join(carpeta, e['nombre'])
    e['estado'] = 'seguro'
    return e


def ya_guardados(dev, tamanos):
    """hash -> ruta de los documentos de los repos que pesan lo mismo que alguna descarga.

    Filtrar por tamaño primero evita calcular el hash de todo C:/dev: dos archivos de distinto
    tamaño nunca son iguales, así que solo se calcula el de los candidatos.
    """
    indice = {}
    for repo in sorted(os.listdir(dev)):
        if not os.path.isdir(os.path.join(dev, repo, '.git')):
            continue
        for raiz, dirs, archivos in os.walk(os.path.join(dev, repo)):
            dirs[:] = [d for d in dirs if d.lower() not in PODAR]
            for a in archivos:
                ruta = os.path.join(raiz, a)
                if os.path.splitext(a)[1].lower() in DOCUMENTOS and os.path.getsize(ruta) in tamanos:
                    indice.setdefault(hash_de(ruta), ruta)
    return indice


def marcar_ya_guardados(entradas, dev):
    """Una descarga idéntica a un documento de cualquier repo es un duplicado, se llame como se llame."""
    tamanos = {os.path.getsize(e['origen']) for e in entradas}
    indice = ya_guardados(dev, tamanos) if tamanos else {}
    for e in entradas:
        copia = indice.get(hash_de(e['origen'])) if os.path.getsize(e['origen']) in tamanos else None
        if copia:
            e['estado'], e['destino'], e['duplicado_de'] = 'duplicado', None, copia
            e['motivo'] = f'ya está en {os.path.relpath(copia, dev)}'


def planificar(origen, dev, tabla):
    docs, ignoradas = documentos(origen, tabla)
    entradas = [clasificar(ruta, sub, pista, dev, tabla) for ruta, sub, pista in docs]
    marcar_ya_guardados(entradas, dev)
    revisar_destinos(entradas)
    return entradas, ignoradas


def revisar_destinos(entradas):
    """Marca duplicados y colisiones. Compara sin mayúsculas: Windows no las distingue."""
    vistos = {}
    for e in entradas:
        if e['estado'] != 'seguro':
            continue
        clave = os.path.normcase(os.path.abspath(e['destino']))
        if clave in vistos:
            e['estado'], e['motivo'] = 'colision', f'otra descarga va al mismo sitio: {vistos[clave]}'
        elif os.path.exists(e['destino']):
            if hash_de(e['destino']) == hash_de(e['origen']):
                e['estado'], e['motivo'] = 'duplicado', 'ya está en el destino, idéntico'
                e['duplicado_de'] = e['destino']
            else:
                e['estado'], e['motivo'] = 'colision', 'el destino existe con otro contenido'
        vistos.setdefault(clave, e['origen'])


def dentro_de_un_repo(destino, dev):
    """El destino tiene que estar en un repo git directamente bajo dev."""
    rel = os.path.relpath(os.path.abspath(destino), os.path.abspath(dev))
    partes = rel.replace('\\', '/').split('/')
    return (not rel.startswith('..') and len(partes) >= 2
            and os.path.isdir(os.path.join(dev, partes[0], '.git')))


def quitar_vacias(carpeta, origen):
    """Borra las carpetas que han quedado vacías, de dentro hacia fuera, sin llegar a origen."""
    while os.path.normcase(carpeta) != os.path.normcase(origen) \
            and os.path.commonpath([carpeta, origen]) == origen:
        try:
            os.rmdir(carpeta)  # solo funciona si está vacía: nunca borra archivos
        except OSError:
            return
        carpeta = os.path.dirname(carpeta)


def ejecutar(plan, dev, origen):
    with open(plan, encoding='utf-8') as fh:
        entradas = json.load(fh)
    movidos, saltados = {}, []
    for e in entradas:
        archivo = os.path.relpath(e['origen'], origen)
        if e['estado'] != 'seguro':
            saltados.append(f'{archivo}: {e["estado"]}')
            continue
        destino = e['destino']
        if not destino or not dentro_de_un_repo(destino, dev):
            saltados.append(f'{archivo}: destino fuera de los repos ({destino})')
        elif not os.path.isfile(e['origen']):
            saltados.append(f'{archivo}: ya no está en el origen')
        elif os.path.exists(destino):  # pudo aparecer después de simular: nunca sobrescribir
            saltados.append(f'{archivo}: el destino ya existe, no se sobrescribe')
        else:
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.move(e['origen'], destino)
            quitar_vacias(os.path.dirname(e['origen']), origen)
            repo = os.path.relpath(destino, dev).replace('\\', '/').split('/')[0]
            movidos.setdefault(repo, []).append(os.path.relpath(destino, os.path.join(dev, repo)))
    for repo, archivos in sorted(movidos.items()):
        print(f'## {repo}: {len(archivos)}')
        for a in archivos:
            print(f'- {a}')
    for s in saltados:
        print('SALTADO', s)


def a_la_papelera(ruta):
    """Manda un archivo a la Papelera de reciclaje de Windows: se puede recuperar, no es un borrado."""
    # La ruta va por variable de entorno, no dentro del comando: así un nombre con comillas
    # o con ';' no puede convertirse en código de PowerShell.
    orden = ("Add-Type -AssemblyName Microsoft.VisualBasic; "
             "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("
             "$env:RUTA_PAPELERA, 'OnlyErrorDialogs', 'SendToRecycleBin')")
    r = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', orden],
                       env={**os.environ, 'RUTA_PAPELERA': ruta}, capture_output=True, text=True)
    return r.returncode == 0 and not os.path.exists(ruta)


def papelera(plan, origen):
    """Manda a la Papelera las descargas marcadas como duplicado, si siguen siendo idénticas."""
    if os.name != 'nt':
        sys.exit('--papelera solo funciona en Windows')
    with open(plan, encoding='utf-8') as fh:
        entradas = json.load(fh)
    for e in entradas:
        if e['estado'] != 'duplicado':
            continue
        archivo, copia = os.path.relpath(e['origen'], origen), e.get('duplicado_de')
        # Se vuelve a comprobar ahora: entre simular y ejecutar pudo cambiar cualquiera de los dos
        if not (copia and os.path.isfile(copia) and os.path.isfile(e['origen'])
                and hash_de(copia) == hash_de(e['origen'])):
            print(f'SALTADO {archivo}: ya no es idéntico a la copia guardada o falta alguno')
        elif a_la_papelera(e['origen']):
            quitar_vacias(os.path.dirname(e['origen']), origen)
            print(f'A la Papelera: {archivo} (se queda {copia})')
        else:
            print(f'ERROR {archivo}: no se pudo mandar a la Papelera')


def portada(pdf, carpeta):
    """Guarda la primera imagen JPEG de un PDF escaneado para poder mirarla sin OCR ni poppler."""
    with open(pdf, 'rb') as fh:
        datos = fh.read()
    m = re.search(rb'/DCTDecode.*?stream\r?\n', datos, re.S)
    if not m:
        sys.exit(f'{pdf}: no tiene imágenes JPEG; pide al usuario que diga qué es')
    salida = os.path.join(carpeta, normalizar(os.path.splitext(os.path.basename(pdf))[0], '.jpg'))
    with open(salida, 'wb') as fh:
        fh.write(datos[m.end():datos.find(b'endstream', m.end())])
    print(salida)


def mostrar(entradas, ignoradas, origen):
    for e in entradas:
        destino = e['destino'] or (', '.join(e['candidatos']) if e['candidatos'] else '?')
        print(f'[{e["estado"]}] {os.path.relpath(e["origen"], origen)} -> {destino}'
              + (f'  ({e["motivo"]})' if e['motivo'] else '')
              + ('  [nombre opaco]' if e['nombre_opaco'] else ''))
    for c in ignoradas:
        print(f'[ignorada] carpeta {c}/ (su nombre no indica ninguna asignatura)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    accion = ap.add_mutually_exclusive_group(required=True)
    accion.add_argument('--plan', metavar='PLAN_JSON', help='simula y escribe el plan')
    accion.add_argument('--ejecutar', metavar='PLAN_JSON', help='mueve las entradas "seguro" del plan')
    accion.add_argument('--papelera', metavar='PLAN_JSON',
                        help='manda a la Papelera de reciclaje las descargas "duplicado" del plan')
    accion.add_argument('--portada', nargs=2, metavar=('PDF', 'CARPETA'),
                        help='extrae la primera imagen de un PDF escaneado a CARPETA')
    ap.add_argument('--origen', default=os.path.join(os.path.expanduser('~'), 'Downloads'))
    ap.add_argument('--dev', default='C:/dev')
    ap.add_argument('--asignaturas', default=ASIGNATURAS)
    a = ap.parse_args()
    a.origen, a.dev = os.path.abspath(a.origen), os.path.abspath(a.dev)  # el plan guarda rutas absolutas
    if a.portada:
        portada(*a.portada)
    elif a.papelera:
        papelera(a.papelera, a.origen)
    elif a.plan:
        with open(a.asignaturas, encoding='utf-8') as fh:
            tabla = json.load(fh)
        entradas, ignoradas = planificar(a.origen, a.dev, tabla)
        with open(a.plan, 'w', encoding='utf-8') as fh:
            json.dump(entradas, fh, ensure_ascii=False, indent=1)
        mostrar(entradas, ignoradas, a.origen)
        print(f'\n{len(entradas)} documentos. Plan en {a.plan}. No se ha movido nada.')
    else:
        ejecutar(a.ejecutar, a.dev, a.origen)
