"""
FASE 2 - Detección de duplicados (SOLO LECTURA: trabaja sobre inventario.csv).

Uso:
    python duplicados.py "D:\\Musica\\_herramientas\\salida\\inventario.csv"

Genera en la misma carpeta:
    canciones.csv   -> una fila por canción: copia elegida + en qué listas estuvo
    archivos.csv    -> una fila por archivo: CONSERVAR / SOBRANTE / ROTO
"""
import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

# Letras que NO son "letra + tilde" y que NFKD no separa: hay que traducirlas a mano
LETRAS_ESPECIALES = str.maketrans({"ø": "o", "æ": "ae", "œ": "oe", "ß": "ss",
                                   "đ": "d", "ł": "l", "þ": "th", "ı": "i"})

CALIDAD_CODEC = {"wav": 3, "flac": 3, "alac": 3, "mp3": 1, "mp4a.40.2": 1}


def clave_nombre(archivo: str) -> str:
    """'149 - Rødhåd - Patient Zero (Original Mix).flac' -> 'rodhadpatientzero'"""
    base = re.sub(r"\.[a-z0-9]+$", "", archivo.lower())                # quitar extensión
    base = re.sub(r"^\s*\d+\s*[.\-_]\s*", "", base)                     # quitar nº de pista
    base = re.sub(r"\((explicit|original mix|original|original version)\)", "", base)
    base = base.translate(LETRAS_ESPECIALES)                           # ø -> o, ß -> ss
    base = unicodedata.normalize("NFKD", base)                         # å -> a + °, ä -> a + ¨
    base = "".join(c for c in base if not unicodedata.combining(c))    # quitar los ¨ ´ ...
    return re.sub(r"[^a-z0-9]", "", base)                              # solo letras y números


class UnionFind:
    """Agrupa elementos que están conectados aunque sea indirectamente."""

    def __init__(self, n):
        self.padre = list(range(n))

    def raiz(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]   # compresión de camino
            x = self.padre[x]
        return x

    def unir(self, a, b):
        self.padre[self.raiz(a)] = self.raiz(b)


def num(valor, defecto=0.0):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return defecto


def main():
    entrada = Path(sys.argv[1])
    with open(entrada, encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f, delimiter=";"))

    for fila in filas:
        # La lista es la carpeta que contiene el archivo (incluye subcarpetas)
        # Acepta CSV antiguos con "\" (Windows) y nuevos con "/"
        fila["ruta_relativa"] = fila["ruta_relativa"].replace("\\", "/")
        fila["lista"] = fila["ruta_relativa"].rsplit("/", 1)[0] if "/" in fila["ruta_relativa"] else ""
        fila["clave"] = clave_nombre(fila["archivo"])
        fila["calidad"] = CALIDAD_CODEC.get(fila["codec"], 0)

    # 1) Unir archivos que son la misma canción por CUALQUIERA de las 3 pistas
    buenos = [i for i, f in enumerate(filas) if f["estado"] == "OK"]
    uf = UnionFind(len(filas))
    for campo in ("clave", "sha256", "md5_audio_flac"):
        primero_con_valor = {}
        for i in buenos:
            valor = filas[i][campo]
            if not valor:
                continue
            if valor in primero_con_valor:
                uf.unir(i, primero_con_valor[valor])
            else:
                primero_con_valor[valor] = i

    grupos = defaultdict(list)
    for i in buenos:
        grupos[uf.raiz(i)].append(filas[i])

    # 2) En cada grupo, elegir la mejor copia y detectar casos dudosos
    canciones = []
    for n, miembros in enumerate(grupos.values(), 1):
        miembros.sort(key=lambda f: (f["calidad"], num(f["kbps_real"]),
                                     bool(f["artista"]), num(f["tamano_bytes"])),
                      reverse=True)
        elegida = miembros[0]
        duraciones = [num(f["duracion_s"]) for f in miembros]
        claves = {f["clave"] for f in miembros}
        motivos = []
        if max(duraciones) - min(duraciones) > 3:
            motivos.append("duraciones distintas")
        if len(claves) > 1:
            motivos.append("mismo audio con nombres distintos")
        listas = sorted({f["lista"] for f in miembros},
                        key=lambda l: min(f["fecha_modificacion"] for f in miembros
                                          if f["lista"] == l))
        id_cancion = f"C{n:04d}"
        for f in miembros:
            f["id_cancion"] = id_cancion
            f["accion"] = "CONSERVAR" if f is elegida else "SOBRANTE"
        canciones.append({
            "id_cancion": id_cancion,
            "archivo_elegido": elegida["ruta_relativa"],
            "codec": elegida["codec"],
            "kbps_real": elegida["kbps_real"],
            "copias": len(miembros),
            "mb_sobrantes": round(sum(num(f["tamano_bytes"]) for f in miembros[1:]) / 1e6, 1),
            "solo_calidad_baja": "SI" if elegida["calidad"] < 3 else "",
            "dudoso": "; ".join(motivos),
            "num_listas": len(listas),
            "listas_en_orden": " -> ".join(listas),
        })

    # 3) Archivos rotos: ¿hay copia buena de esa canción en otra parte?
    clave_a_id = {f["clave"]: f["id_cancion"] for f in filas if f.get("id_cancion")}
    for f in filas:
        if f["estado"] != "OK":
            f["accion"] = f["estado"]
            f["id_cancion"] = clave_a_id.get(f["clave"], "")

    salida = entrada.parent
    with open(salida / "canciones.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(canciones[0]), delimiter=";")
        w.writeheader()
        w.writerows(canciones)
    cols = ["id_cancion", "accion", "lista", "archivo", "codec", "kbps_real",
            "duracion_s", "tamano_bytes", "ruta_relativa"]
    with open(salida / "archivos.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)

    # Rotos SIN copia buena en ningún sitio = hay que volver a descargarlos
    redescargar = [f for f in filas if f["estado"] != "OK" and not f["id_cancion"]]
    with open(salida / "para_redescargar.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["lista", "archivo", "estado"], delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(redescargar)

    sobrantes = [f for f in filas if f.get("accion") == "SOBRANTE"]
    print(f"Para volver a descargar: {len(redescargar)}")
    print(f"Canciones únicas: {len(canciones)}")
    print(f"Archivos sobrantes: {len(sobrantes)} "
          f"({sum(num(f['tamano_bytes']) for f in sobrantes) / 1e9:.1f} GB)")
    print(f"Dudosos a revisar: {sum(1 for c in canciones if c['dudoso'])}")
    print(f"Solo en calidad baja (AAC/MP3): {sum(1 for c in canciones if c['solo_calidad_baja'])}")


if __name__ == "__main__":
    main()
