"""Normaliza nombres de documentos y carpetas a minúsculas con guiones en repos git.

Uso:
    python normalizar.py <raíz> [--salida plan.md]              # simula y escribe el plan
    python normalizar.py <raíz> --ejecutar [--registro reg.json] # renombra con git mv
    python normalizar.py <raíz> --referencias reg.json           # actualiza rutas en los .md

<raíz> puede ser un repo o una carpeta que contiene varios repos.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys
import unicodedata

DOCUMENTOS = {'.pdf', '.doc', '.docx', '.odt', '.ods', '.odp', '.ppt', '.pptx',
              '.xls', '.xlsx', '.rtf', '.epub'}
# Carpetas cuyo nombre exacto importa a una herramienta: no se tocan ni ellas ni lo de dentro
INTOCABLES = {'src', 'assets', 'packages', 'projectsettings', '.vscode', '.idea', '.github',
              'node_modules', 'target', 'bin', 'obj', 'docs', 'site', '.claude', '.venv',
              'venv', '__pycache__', '.claude-plugin'}


def normalizar(nombre, extension=''):
    """'UT1.2 Gestión #C.pdf' -> 'ut1-2-gestion-csharp.pdf'"""
    nombre = nombre.replace('C#', 'csharp').replace('#', 'sharp')
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', nombre).strip('-') + extension.lower()


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=off', *args],
                          capture_output=True)


def repos_bajo(raiz):
    if os.path.isdir(os.path.join(raiz, '.git')):
        return [raiz]
    return sorted(os.path.join(raiz, d) for d in os.listdir(raiz)
                  if os.path.isdir(os.path.join(raiz, d, '.git')))


def carpetas_de_paquete(repo, ficheros):
    """Carpetas que forman un paquete Java (package x.y;) o Python (__init__.py)."""
    paquetes = set()
    for f in ficheros:
        carpeta = os.path.dirname(f)
        if f.endswith('__init__.py'):
            paquetes.add(carpeta)
        elif f.endswith('.java'):
            with open(os.path.join(repo, f), encoding='utf-8', errors='ignore') as fh:
                m = re.search(r'^\s*package\s+([\w.]+)\s*;', fh.read(2000), re.M)
            if m:
                segmentos, partes = m.group(1).split('.'), carpeta.split('/')
                if partes[-len(segmentos):] == segmentos:
                    for i in range(len(segmentos)):
                        paquetes.add('/'.join(partes[:len(partes) - i]))
    return paquetes


def planificar(repo):
    """Devuelve (renombrados de ficheros, renombrados de carpetas, colisiones)."""
    ficheros = [f for f in git(repo, 'ls-files', '-z').stdout.decode('utf-8').split('\0') if f]
    carpetas = {'/'.join(f.split('/')[:i]) for f in ficheros for i in range(1, f.count('/') + 1)}
    paquetes = carpetas_de_paquete(repo, ficheros)

    def intocable(ruta):
        return any(p.lower() in INTOCABLES for p in ruta.split('/'))

    r_ficheros = {}
    for f in ficheros:
        base, ext = os.path.splitext(os.path.basename(f))
        if ext.lower() in DOCUMENTOS and normalizar(base, ext) != base + ext \
                and not intocable(os.path.dirname(f)):
            r_ficheros[f] = normalizar(base, ext)
    r_carpetas = {}
    for c in carpetas:
        nombre = c.split('/')[-1]
        if normalizar(nombre) != nombre and c not in paquetes and not intocable(c):
            r_carpetas[c] = normalizar(nombre)

    # Colisión: dos elementos del mismo padre acaban con el mismo nombre (sin distinguir mayúsculas)
    destino = collections.defaultdict(list)
    for elem in set(ficheros) | carpetas:
        padre, nombre = os.path.split(elem)
        nuevo = r_ficheros.get(elem) or r_carpetas.get(elem) or nombre
        destino[(padre, nuevo.lower())].append(elem)
    colisiones = [v for v in destino.values() if len(v) > 1]
    return r_ficheros, r_carpetas, colisiones


def mover(repo, viejo, nuevo):
    """git mv en dos pasos: en Windows un cambio solo de mayúsculas no se detecta en uno."""
    temporal = viejo + '.__tmp_renombrado__'
    r = git(repo, 'mv', viejo, temporal)
    if r.returncode:
        return r.stderr.decode('utf-8', 'replace').strip()
    r = git(repo, 'mv', temporal, nuevo)
    if r.returncode:
        git(repo, 'mv', temporal, viejo)
        return r.stderr.decode('utf-8', 'replace').strip()
    return None


def simular(raiz, salida):
    lineas, total_f, total_c = [], 0, 0
    for repo in repos_bajo(raiz):
        r_f, r_c, colisiones = planificar(repo)
        if not (r_f or r_c or colisiones):
            continue
        total_f, total_c = total_f + len(r_f), total_c + len(r_c)
        lineas.append(f'\n## {os.path.basename(repo)}: {len(r_f)} archivos, {len(r_c)} carpetas\n')
        for c in colisiones:
            lineas.append(f'- ⚠️ COLISIÓN (el repo se saltará): {", ".join(map(repr, c))}')
        lineas += [f'- `{c}` → `{n}`' for c, n in sorted(r_c.items())]
        lineas += [f'- `{f}` → `{n}`' for f, n in sorted(r_f.items())]
    cabecera = f'# Plan de renombrado\n\n**Total: {total_f} archivos y {total_c} carpetas.**\n'
    with open(salida, 'w', encoding='utf-8') as fh:
        fh.write(cabecera + '\n'.join(lineas) + '\n')
    print(f'Plan en {salida}: {total_f} archivos, {total_c} carpetas. No se ha movido nada.')


def ejecutar(raiz, registro):
    resultado, errores = {}, []
    for repo in repos_bajo(raiz):
        if git(repo, 'status', '--porcelain').stdout.strip():
            errores.append(f'{repo}: tiene cambios sin commit, se salta')
            continue
        r_f, r_c, colisiones = planificar(repo)
        if colisiones:
            errores.append(f'{repo}: colisiones {colisiones}, se salta')
            continue
        hechos = []
        # Primero los ficheros, después las carpetas de la más profunda a la más superficial:
        # así la ruta del padre sigue siendo la original cuando se mueve cada elemento.
        orden = list(r_f.items()) + sorted(r_c.items(), key=lambda x: -x[0].count('/'))
        for viejo, nombre in orden:
            padre = os.path.dirname(viejo)
            nuevo = f'{padre}/{nombre}' if padre else nombre
            error = mover(repo, viejo, nuevo)
            if error:
                errores.append(f'{repo}: {viejo}: {error}')
            else:
                hechos.append((viejo, nuevo))
        resultado[repo] = hechos
        print(f'{os.path.basename(repo)}: {len(hechos)} renombrados')
    with open(registro, 'w', encoding='utf-8') as fh:
        json.dump({'renombrados': resultado, 'errores': errores}, fh, ensure_ascii=False, indent=1)
    for e in errores:
        print('ERROR', e)
    print(f'Registro en {registro}')


def referencias(registro):
    """Cambia nombres viejos por nuevos solo dentro de `código` en los .md, como segmento de ruta."""
    with open(registro, encoding='utf-8') as fh:
        datos = json.load(fh)['renombrados']
    for repo, hechos in datos.items():
        if not hechos:
            continue
        mapa = {os.path.basename(v): os.path.basename(n) for v, n in hechos}
        patron = re.compile(r'(?<![^/`"\s])(' + '|'.join(map(re.escape, sorted(mapa, key=len, reverse=True)))
                            + r')(?=[/`"\s]|$)')
        mds = [f for f in git(repo, 'ls-files', '-z', '*.md').stdout.decode('utf-8').split('\0') if f]
        for f in mds:
            ruta = os.path.join(repo, f)
            with open(ruta, encoding='utf-8', newline='') as fh:
                texto = fh.read()
            nuevo = re.sub(r'`[^`\n]+`', lambda m: patron.sub(lambda x: mapa[x.group(1)], m.group(0)), texto)
            if nuevo != texto:
                with open(ruta, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(nuevo)
                print('actualizado', os.path.join(os.path.basename(repo), f))
    print('Revisa a mano las rutas que no estén entre comillas invertidas (árboles, LEEME, títulos).')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('raiz', nargs='?', default='.')
    ap.add_argument('--ejecutar', action='store_true', help='renombra de verdad (por defecto solo simula)')
    ap.add_argument('--salida', default='plan-renombrado.md')
    ap.add_argument('--registro', default='registro-renombrado.json')
    ap.add_argument('--referencias', metavar='REGISTRO', help='actualiza rutas en los .md usando el registro')
    a = ap.parse_args()
    if a.referencias:
        referencias(a.referencias)
    elif a.ejecutar:
        ejecutar(a.raiz, a.registro)
    else:
        simular(a.raiz, a.salida)
    sys.exit(0)
