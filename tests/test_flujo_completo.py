"""Prueba de extremo a extremo con la biblioteca falsa de ejemplos/."""
import csv
import subprocess
import sys
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parent.parent


def ejecutar(script, *args):
    resultado = subprocess.run([sys.executable, str(RAIZ_REPO / script), *map(str, args)],
                               capture_output=True, text=True)
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout


def audios(carpeta: Path):
    return sorted(p for p in carpeta.rglob("*.wav") if "_herramientas" not in p.parts)


def test_flujo_completo(tmp_path):
    bib = tmp_path / "biblioteca"
    ejecutar("ejemplos/crear_biblioteca_prueba.py", bib)
    originales = audios(bib)
    assert len(originales) == 13

    # Fase 1: inventario
    salida = ejecutar("src/inventario.py", bib)
    assert "Rotos: 1 | Truncados: 1" in salida

    # Fase 2: duplicados
    salida = ejecutar("src/duplicados.py", bib / "_herramientas" / "salida" / "inventario.csv")
    assert "Canciones únicas: 8" in salida          # 6 de enero + Basalto + Fiebre
    assert "Archivos sobrantes: 3" in salida        # 2 copias en febrero + 1 en la subcarpeta

    # Simular no mueve nada
    ejecutar("src/organizar.py", bib)
    assert audios(bib) == originales

    # Ejecutar
    ejecutar("src/organizar.py", bib, "--ejecutar")
    assert len(list((bib / "Biblioteca").rglob("*.wav"))) == 8
    assert len(list((bib / "_Cuarentena").rglob("*.wav"))) == 5   # 3 sobrantes + 2 rotos
    assert (bib / "Biblioteca" / "Nova Kern" / "Cold Circuit - Nova Kern.wav").exists()
    assert (bib / "Biblioteca" / "Mira Tal" / "Fiebre - Mira Tal.wav").exists()

    # Cada entrada de cada playlist apunta a un archivo que existe
    listas = bib / "Listas"
    playlist_sub = listas / "Descargas Marzo - Sesion Hipnotica.m3u8"
    assert playlist_sub.exists()
    for m3u in listas.glob("*.m3u8"):
        for linea in m3u.read_text(encoding="utf-8").splitlines():
            if linea and not linea.startswith("#"):
                assert (listas / linea.replace("\\", "/")).resolve().exists(), linea
    assert "# FALTA" in playlist_sub.read_text(encoding="utf-8")

    # Ejecutar dos veces está bloqueado
    resultado = subprocess.run([sys.executable, str(RAIZ_REPO / "src/organizar.py"), str(bib),
                                "--ejecutar"], capture_output=True, text=True)
    assert resultado.returncode != 0

    # Deshacer devuelve todo a su sitio
    ejecutar("src/organizar.py", bib, "--deshacer")
    assert audios(bib) == originales


def test_inventario_genera_rutas_con_barra(tmp_path):
    bib = tmp_path / "biblioteca"
    ejecutar("ejemplos/crear_biblioteca_prueba.py", bib)
    ejecutar("src/inventario.py", bib)
    with open(bib / "_herramientas" / "salida" / "inventario.csv", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    assert all("\\" not in f["ruta_relativa"] for f in filas)
