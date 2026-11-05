"""
FASE 4 - Reorganizar la biblioteca.

Tres modos:
    python organizar.py "D:\\Musica"              -> SIMULA (no toca nada)
    python organizar.py "D:\\Musica" --ejecutar   -> mueve de verdad
    python organizar.py "D:\\Musica" --deshacer   -> devuelve todo a su sitio

Necesita haber ejecutado antes inventario.py y duplicados.py.

Resultado tras --ejecutar:
    Biblioteca\\<Artista>\\<Título> - <Artista>.flac   una copia de cada canción
    Listas\\<lista original>.m3u8                      cada carpeta antigua, mismo orden
    Listas\\_Pendiente FLAC.m3u8                       canciones que solo tienes en AAC/MP3
    Listas\\_Pendiente redescargar.txt                 descargas rotas sin copia buena
    _Cuarentena\\<ruta original>                       sobrantes y rotos (bórrala tú cuando quieras)
    _herramientas\\salida\\registro_movimientos.csv    para poder deshacer
"""
import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ESTRUCTURA = "artista"        # "artista" = Biblioteca\Artista\...  |  "plana" = todo junto
LARGO_MAXIMO_NOMBRE = 150     # Windows limita la ruta completa a ~260 caracteres
PROHIBIDOS_WINDOWS = r'[<>:"/\\|?*]'


# ---------------------------------------------------------------- nombres
def limpiar(texto: str) -> str:
    """Quita caracteres que Windows no permite y espacios/puntos sobrantes."""
    texto = re.sub(PROHIBIDOS_WINDOWS, "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip(" .-")


def solo_alfanumerico(texto: str) -> str:
    return re.sub(r"[^0-9a-z]", "", texto.lower())


def separar_artista_titulo(archivo: str, artista_etiqueta: str = ""):
    """'149 - Alarico - Cut 2.flac' -> ('Alarico', 'Cut 2', '.flac')"""
    base, extension = os.path.splitext(archivo)
    base = re.sub(r"^\s*\d+\s*[.\-_]\s*", "", base)          # nº de pista fuera
    base = re.sub(r"^[A-D]\d{1,2}\.\s*", "", base)             # cara de vinilo: 'A1. '
    trozos = base.split(" - ")
    artista, titulo = "Desconocido", base
    if len(trozos) > 1:
        artista, titulo = trozos[0], " - ".join(trozos[1:])    # por defecto: primer " - "
        # Si el artista lleva " - " dentro ('OFF / GRID' -> 'OFF - GRID'), la etiqueta
        # nos dice dónde acaba: probamos cada corte y nos quedamos con el que coincide.
        objetivo = solo_alfanumerico(artista_etiqueta)
        for k in range(2, len(trozos)):
            if objetivo and solo_alfanumerico(" - ".join(trozos[:k])) == objetivo:
                artista, titulo = " - ".join(trozos[:k]), " - ".join(trozos[k:])
                break
    # Formato Bandcamp: 'Álbum - 03 Título' -> 'Título'
    bandcamp = re.match(r"^.+ - \d{1,3} (.+)$", titulo)
    if bandcamp:
        titulo = bandcamp.group(1)
    if artista_etiqueta and solo_alfanumerico(artista) == solo_alfanumerico(artista_etiqueta):
        artista = artista_etiqueta.replace("/", " ")           # 'OFF / GRID' -> 'OFF GRID'
    return limpiar(artista) or "Desconocido", limpiar(titulo) or "Sin titulo", extension.lower()


def artista_principal(artista: str) -> str:
    """'Alarico, Vault Records' -> 'Alarico'  (para el nombre de la carpeta)"""
    return limpiar(re.split(r",|;| & | feat\.? | x ", artista, maxsplit=1)[0]) or "Desconocido"


def ruta_absoluta(raiz: Path, relativa: str) -> Path:
    """Une la raíz con una ruta del CSV, venga con "/" o con "\\"."""
    return raiz.joinpath(*re.split(r"[\\/]", relativa))


def numero_pista(archivo: str) -> int:
    """Para respetar el orden original de cada lista."""
    m = re.match(r"^\s*(\d+)", archivo)
    return int(m.group(1)) if m else 10**6


def nombre_playlist(lista: str) -> str:
    """'Sesiones Hipnotico\\Playlist\\tz23' -> 'Sesiones Hipnotico - tz23'"""
    partes = [p for p in re.split(r"[\\/]", lista) if p.lower() != "playlist"]
    return limpiar(" - ".join(partes))


# ---------------------------------------------------------------- plan
def construir_plan(raiz: Path, salida: Path):
    with open(salida / "archivos.csv", encoding="utf-8-sig", newline="") as f:
        archivos = list(csv.DictReader(f, delimiter=";"))
    with open(salida / "inventario.csv", encoding="utf-8-sig", newline="") as f:
        etiqueta_artista = {r["ruta_relativa"].replace("\\", "/"): r["artista"]
                            for r in csv.DictReader(f, delimiter=";")}

    movimientos = []                 # (origen, destino, motivo)
    destino_de_cancion = {}          # id_cancion -> ruta en Biblioteca
    usados = set()                   # nombres ya ocupados (en minúsculas: Windows no distingue)

    for f in sorted(archivos, key=lambda x: x["ruta_relativa"]):
        origen = ruta_absoluta(raiz, f["ruta_relativa"])
        if f["accion"] == "CONSERVAR":
            artista, titulo, ext = separar_artista_titulo(
                f["archivo"], etiqueta_artista.get(f["ruta_relativa"].replace("\\", "/"), ""))
            nombre = f"{titulo} - {artista}"[:LARGO_MAXIMO_NOMBRE].rstrip(" .")
            carpeta = (raiz / "Biblioteca" / artista_principal(artista)
                       if ESTRUCTURA == "artista" else raiz / "Biblioteca")
            destino = carpeta / f"{nombre}{ext}"
            n = 2
            while str(destino).lower() in usados:               # dos temas con igual nombre
                destino = carpeta / f"{nombre} ({n}){ext}"
                n += 1
            usados.add(str(destino).lower())
            destino_de_cancion[f["id_cancion"]] = destino
            movimientos.append((origen, destino, "BIBLIOTECA"))
        else:                                                  # SOBRANTE, ROTO, TRUNCADO
            destino = ruta_absoluta(raiz / "_Cuarentena", f["ruta_relativa"])
            movimientos.append((origen, destino, f["accion"]))
    return archivos, movimientos, destino_de_cancion


def escribir_listas(raiz: Path, archivos, destino_de_cancion, salida: Path):
    carpeta_listas = raiz / "Listas"
    carpeta_listas.mkdir(exist_ok=True)

    por_lista = defaultdict(list)
    for f in archivos:
        por_lista[f["lista"]].append(f)

    for lista, miembros in por_lista.items():
        miembros.sort(key=lambda f: (numero_pista(f["archivo"]), f["archivo"].lower()))
        lineas, vistos = ["#EXTM3U", f"#PLAYLIST:{nombre_playlist(lista)}"], set()
        for f in miembros:
            destino = destino_de_cancion.get(f["id_cancion"])
            if destino is None:                                  # roto sin copia buena
                lineas.append(f"# FALTA (volver a descargar): {f['archivo']}")
                continue
            if destino in vistos:                                # repetida dentro de la lista
                continue
            vistos.add(destino)
            lineas.append(f"#EXTINF:{int(float(f['duracion_s'] or 0))},{destino.stem}")
            lineas.append(os.path.relpath(destino, carpeta_listas))  # ..\Biblioteca\...
        (carpeta_listas / f"{nombre_playlist(lista)}.m3u8").write_text(
            "\n".join(lineas) + "\n", encoding="utf-8")

    # Pendiente FLAC: la copia elegida es de baja calidad
    with open(salida / "canciones.csv", encoding="utf-8-sig", newline="") as f:
        canciones = list(csv.DictReader(f, delimiter=";"))
    lineas = ["#EXTM3U", "#PLAYLIST:_Pendiente FLAC"]
    for c in canciones:
        if c["solo_calidad_baja"] == "SI":
            lineas.append(os.path.relpath(destino_de_cancion[c["id_cancion"]], carpeta_listas))
    (carpeta_listas / "_Pendiente FLAC.m3u8").write_text("\n".join(lineas) + "\n",
                                                        encoding="utf-8")

    # Pendiente redescargar: no existen, así que va como texto
    with open(salida / "para_redescargar.csv", encoding="utf-8-sig", newline="") as f:
        faltan = [f"{r['lista']}  |  {r['archivo']}" for r in csv.DictReader(f, delimiter=";")]
    (carpeta_listas / "_Pendiente redescargar.txt").write_text("\n".join(faltan) + "\n",
                                                               encoding="utf-8")
    return len(por_lista)


# ---------------------------------------------------------------- acciones
def simular(raiz, salida):
    archivos, movimientos, _ = construir_plan(raiz, salida)
    with open(salida / "plan_organizacion.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["motivo", "origen", "destino"])
        for origen, destino, motivo in movimientos:
            w.writerow([motivo, origen.relative_to(raiz).as_posix(),
                        destino.relative_to(raiz).as_posix()])
    cuenta = defaultdict(int)
    for *_, motivo in movimientos:
        cuenta[motivo] += 1
    print("SIMULACIÓN (no se ha movido nada):")
    for motivo, n in sorted(cuenta.items()):
        print(f"  {motivo:12} {n}")
    print(f"Revisa {salida / 'plan_organizacion.csv'}")


def ejecutar(raiz, salida):
    registro = salida / "registro_movimientos.csv"
    if registro.exists():
        sys.exit("Ya existe un registro: parece que ya se ejecutó. Usa --deshacer primero.")
    archivos, movimientos, destino_de_cancion = construir_plan(raiz, salida)

    faltan = [o for o, _, _ in movimientos if not o.exists()]
    if faltan:
        sys.exit(f"{len(faltan)} archivos del plan ya no existen (ej: {faltan[0]}). "
                 "Vuelve a lanzar inventario.py y duplicados.py.")

    hechos = 0
    with open(registro, "w", encoding="utf-8-sig", newline="") as log:
        w = csv.writer(log, delimiter=";")
        w.writerow(["origen", "destino"])
        for origen, destino, _ in movimientos:
            if destino.exists():                          # nunca pisar un archivo
                print(f"  OMITIDO, ya existe: {destino}")
                continue
            destino.parent.mkdir(parents=True, exist_ok=True)
            os.rename(origen, destino)                    # mismo disco = instantáneo
            w.writerow([origen, destino])
            log.flush()                                   # anotado aunque se corte la luz
            hechos += 1
            if hechos % 250 == 0:
                print(f"  {hechos}/{len(movimientos)} movidos...")
    n_listas = escribir_listas(raiz, archivos, destino_de_cancion, salida)
    print(f"Hecho: {hechos} archivos movidos, {n_listas} playlists en {raiz / 'Listas'}")


def deshacer(raiz, salida):
    registro = salida / "registro_movimientos.csv"
    with open(registro, encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    for fila in reversed(filas):                          # en orden inverso
        origen, destino = Path(fila["origen"]), Path(fila["destino"])
        if destino.exists() and not origen.exists():
            origen.parent.mkdir(parents=True, exist_ok=True)
            os.rename(destino, origen)
    registro.rename(registro.with_suffix(".deshecho.csv"))
    print(f"Deshechos {len(filas)} movimientos. (Las carpetas vacías y Listas\\ quedan; bórralas a mano.)")


if __name__ == "__main__":
    raiz = Path(sys.argv[1])
    salida = raiz / "_herramientas" / "salida"
    modo = sys.argv[2] if len(sys.argv) > 2 else ""
    if modo == "--ejecutar":
        ejecutar(raiz, salida)
    elif modo == "--deshacer":
        deshacer(raiz, salida)
    else:
        simular(raiz, salida)
