"""
FASE 1 - Inventario de la biblioteca (SOLO LECTURA: no mueve ni borra nada).

Uso (en la terminal de Windows):
    pip install mutagen
    python inventario.py "D:\\Musica"

Resultado: <raiz>/_herramientas/salida/inventario.csv (se abre con Excel)
"""
import csv
import hashlib
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

EXTENSIONES_AUDIO = {".flac", ".wav", ".m4a", ".mp3", ".aiff", ".aif"}
TAMANO_MINIMO = 100 * 1024          # < 100 KB = descarga vacía o casi
DURACION_MINIMA = 30                # segundos; menos que esto no es un tema
KBPS_MIN_SIN_PERDIDA = 250          # un FLAC/WAV real nunca baja de aquí
BLOQUE = 1024 * 1024                # leer de 1 MB en 1 MB al calcular el hash


def leer_metadatos(ruta: Path) -> dict:
    """Abre el archivo con mutagen y saca calidad técnica y etiquetas."""
    datos = {"duracion_s": "", "codec": "", "bitrate_kbps": "", "sample_rate": "",
             "bits": "", "artista": "", "titulo": "", "md5_audio_flac": "", "error": ""}
    try:
        audio = MutagenFile(ruta, easy=False)
        if audio is None:
            datos["error"] = "formato no reconocido"
            return datos
        info = audio.info
        datos["duracion_s"] = round(getattr(info, "length", 0) or 0, 2)
        datos["bitrate_kbps"] = round((getattr(info, "bitrate", 0) or 0) / 1000)
        datos["sample_rate"] = getattr(info, "sample_rate", "") or ""
        datos["bits"] = getattr(info, "bits_per_sample", "") or ""

        if isinstance(audio, FLAC):
            datos["codec"] = "flac"
            md5 = info.md5_signature            # huella del AUDIO descomprimido
            datos["md5_audio_flac"] = f"{md5:032x}" if md5 else ""
            etiquetas = audio.tags or {}
            datos["artista"] = "; ".join(etiquetas.get("artist", []))
            datos["titulo"] = "; ".join(etiquetas.get("title", []))
        elif isinstance(audio, MP4):
            datos["codec"] = getattr(info, "codec", "")   # 'alac' o 'mp4a.40.2' (AAC)
            etiquetas = audio.tags or {}
            datos["artista"] = "; ".join(etiquetas.get("\xa9ART", []))
            datos["titulo"] = "; ".join(etiquetas.get("\xa9nam", []))
        else:
            datos["codec"] = ruta.suffix.lower().lstrip(".")
            facil = MutagenFile(ruta, easy=True)
            if facil is not None and facil.tags:
                datos["artista"] = "; ".join(facil.tags.get("artist", []))
                datos["titulo"] = "; ".join(facil.tags.get("title", []))
    except Exception as e:                      # archivo corrupto o truncado
        datos["error"] = f"{type(e).__name__}: {e}"
    return datos


def calcular_estado(fila: dict) -> str:
    """OK, ROTO (vacío/ilegible) o TRUNCADO (descarga a medias)."""
    if fila["error"] or fila["tamano_bytes"] < TAMANO_MINIMO:
        return "ROTO"
    duracion = fila["duracion_s"] or 0
    if duracion < DURACION_MINIMA:
        return "ROTO"
    kbps_real = fila["tamano_bytes"] * 8 / duracion / 1000
    fila["kbps_real"] = round(kbps_real)
    if fila["codec"] in ("flac", "wav", "alac") and kbps_real < KBPS_MIN_SIN_PERDIDA:
        return "TRUNCADO"
    return "OK"


def sha256_archivo(ruta: Path) -> str:
    """Huella de TODOS los bytes del archivo, leyendo por bloques."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        while bloque := f.read(BLOQUE):
            h.update(bloque)
    return h.hexdigest()


def main():
    raiz = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    salida = raiz / "_herramientas" / "salida"
    salida.mkdir(parents=True, exist_ok=True)

    # 1) Recorrer carpetas y leer metadatos
    filas = []
    inicio = time.time()
    for carpeta_actual, subcarpetas, archivos in os.walk(raiz):
        subcarpetas[:] = [d for d in subcarpetas if not d.startswith("_")]
        for nombre in archivos:
            ruta = Path(carpeta_actual) / nombre
            if ruta.suffix.lower() not in EXTENSIONES_AUDIO:
                continue
            stat = ruta.stat()
            fila = {
                "lista": ruta.parent.relative_to(raiz).as_posix(),
                "ruta_relativa": ruta.relative_to(raiz).as_posix(),   # "/" en todos los sistemas
                "archivo": nombre,
                "extension": ruta.suffix.lower(),
                "tamano_bytes": stat.st_size,
                "fecha_modificacion": time.strftime("%Y-%m-%d %H:%M",
                                                    time.localtime(stat.st_mtime)),
            }
            fila.update(leer_metadatos(ruta))
            fila["estado"] = calcular_estado(fila)
            filas.append(fila)
            if len(filas) % 200 == 0:
                print(f"  {len(filas)} archivos leídos...")
    print(f"Metadatos: {len(filas)} archivos en {time.time() - inicio:.0f} s")

    # 2) SHA-256 solo donde puede haber copias exactas (mismo tamaño)
    por_tamano = defaultdict(list)
    for fila in filas:
        if fila["estado"] == "OK":
            por_tamano[fila["tamano_bytes"]].append(fila)
    candidatos = [f for grupo in por_tamano.values() if len(grupo) > 1 for f in grupo]
    print(f"Calculando hash de {len(candidatos)} archivos con tamaño repetido...")
    for i, fila in enumerate(candidatos, 1):
        fila["sha256"] = sha256_archivo(raiz.joinpath(*fila["ruta_relativa"].split("/")))
        if i % 100 == 0:
            print(f"  hash {i}/{len(candidatos)}")

    # 3) Guardar CSV
    columnas = ["lista", "ruta_relativa", "archivo", "extension", "tamano_bytes",
                "fecha_modificacion", "estado", "codec", "bitrate_kbps", "sample_rate",
                "bits", "kbps_real", "duracion_s", "artista", "titulo", "md5_audio_flac", "sha256",
                "error"]
    destino = salida / "inventario.csv"
    with open(destino, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas, delimiter=";")
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({c: fila.get(c, "") for c in columnas})

    rotos = sum(1 for f in filas if f["estado"] == "ROTO")
    truncados = sum(1 for f in filas if f["estado"] == "TRUNCADO")
    print(f"\nListo -> {destino}")
    print(f"Total: {len(filas)} | Rotos: {rotos} | Truncados: {truncados} | "
          f"Tiempo: {time.time() - inicio:.0f} s")


if __name__ == "__main__":
    main()
