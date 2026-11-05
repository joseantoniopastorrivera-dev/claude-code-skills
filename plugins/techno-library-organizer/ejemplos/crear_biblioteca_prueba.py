"""
Crea una biblioteca FALSA para probar los scripts sin usar música real.

Uso:
    python ejemplos/crear_biblioteca_prueba.py biblioteca_prueba

Genera tonos WAV (solo librería estándar de Python) con los casos típicos:
copias exactas entre listas, distinta numeración de pista, una lista dentro
de una subcarpeta, un formato Bandcamp, un archivo vacío y una descarga a medias.
Los artistas y títulos son inventados.
"""
import math
import shutil
import struct
import sys
import wave
from pathlib import Path

FRECUENCIA_MUESTREO = 22050      # 22 kHz mono 16 bit = 352 kbps (como un audio sin pérdida)
DURACION_S = 35                  # por encima del mínimo de 30 s de inventario.py


def crear_tono(ruta: Path, hz: float) -> None:
    """Un tono distinto por canción: así cada canción tiene un audio diferente."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    muestras = (int(8000 * math.sin(2 * math.pi * hz * i / FRECUENCIA_MUESTREO))
                for i in range(FRECUENCIA_MUESTREO * DURACION_S))
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FRECUENCIA_MUESTREO)
        w.writeframes(b"".join(struct.pack("<h", m) for m in muestras))


def main():
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else "biblioteca_prueba")
    if raiz.exists():
        sys.exit(f"{raiz} ya existe; bórrala o elige otro nombre.")

    canciones = {
        "Nova Kern - Cold Circuit": 220, "Nova Kern - Iron Bloom": 247,
        "Lumen Drift - Night Engine": 262, "Lumen Drift, Kael - Static Garden": 294,
        "Orbe - Hollow (Rework)": 330, "Orbe - Hollow": 349,
    }
    enero, febrero = raiz / "Lista Enero", raiz / "Lista Febrero"
    sub = raiz / "Descargas Marzo" / "Playlist" / "Sesion Hipnotica"

    for n, (nombre, hz) in enumerate(canciones.items(), 1):
        crear_tono(enero / f"{n:02d}. {nombre}.wav", hz)

    febrero.mkdir(parents=True)
    sub.mkdir(parents=True)

    # Febrero repite dos temas de enero con otra numeración (copias exactas)
    shutil.copy(enero / "01. Nova Kern - Cold Circuit.wav", febrero / "007 - Nova Kern - Cold Circuit.wav")
    shutil.copy(enero / "03. Lumen Drift - Night Engine.wav", febrero / "008 - Lumen Drift - Night Engine.wav")
    crear_tono(febrero / "009 - Vela Sur - Basalto.wav", 392)

    # Lista dentro de subcarpetas + nombre estilo Bandcamp
    crear_tono(sub / "01 - Mira Tal - Curated by Nadie - 03 Fiebre.wav", 440)
    shutil.copy(febrero / "009 - Vela Sur - Basalto.wav", sub / "02 - Vela Sur - Basalto.wav")

    # Descargas rotas
    (sub / "03 - Kito - Vacia.wav").write_bytes(b"")                       # 0 bytes
    crear_tono(sub / "04 - Kito - A Medias.wav", 494)
    datos = (sub / "04 - Kito - A Medias.wav").read_bytes()
    (sub / "04 - Kito - A Medias.wav").write_bytes(datos[: len(datos) // 5])  # 20 %

    total = sum(1 for _ in raiz.rglob("*.wav"))
    print(f"Biblioteca de prueba creada en {raiz} ({total} archivos)")


if __name__ == "__main__":
    main()
