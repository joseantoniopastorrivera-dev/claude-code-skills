import pytest

from duplicados import UnionFind, clave_nombre
from organizar import artista_principal, nombre_playlist, separar_artista_titulo


@pytest.mark.parametrize("a, b", [
    ("01. Alarico - Cut 2.flac", "149 - Alarico - Cut 2.flac"),          # nº de pista distinto
    ("Rødhåd - Patient Zero.flac", "Rodhad - Patient Zero.m4a"),          # tildes y extensión
    ("Lewis Fautzi - Desinformation (Original Mix).flac", "Lewis Fautzi - Desinformation.flac"),
])
def test_clave_nombre_iguala_variantes(a, b):
    assert clave_nombre(a) == clave_nombre(b)


def test_clave_nombre_distingue_remixes():
    assert clave_nombre("Oscar Mulero - Rotar.flac") != clave_nombre("Oscar Mulero - Rotar (Tensal remix).flac")


@pytest.mark.parametrize("archivo, etiqueta, esperado", [
    ("149 - Alarico - Cut 2.flac", "", ("Alarico", "Cut 2", ".flac")),
    # el artista 'OFF / GRID' llega al nombre de archivo como 'OFF - GRID'
    ("12 - OFF - GRID - Distant Thoughts.flac", "OFF / GRID", ("OFF GRID", "Distant Thoughts", ".flac")),
    # formato Bandcamp: Artista - Álbum - NN Título
    ("A. Morgan - Curated by MARRØN - 01 Sub Groover.wav", "", ("A. Morgan", "Sub Groover", ".wav")),
    # cara de vinilo
    ("B1. Sons Of Hidden - Manglar.flac", "", ("Sons Of Hidden", "Manglar", ".flac")),
    # 'A4' es un artista, no una cara de vinilo
    ("440 - A4 - Transition.flac", "", ("A4", "Transition", ".flac")),
    # títulos que llevan ' - ' se conservan
    ("Tsott - Soft Edges - Hard lines.flac", "", ("Tsott", "Soft Edges - Hard lines", ".flac")),
    # caracteres prohibidos en Windows
    ('Artista - Que? "Raro".flac', "", ("Artista", "Que Raro", ".flac")),
])
def test_separar_artista_titulo(archivo, etiqueta, esperado):
    assert separar_artista_titulo(archivo, etiqueta) == esperado


def test_artista_principal():
    assert artista_principal("Alarico, Vault Records") == "Alarico"
    assert artista_principal("Truncate & Ruskin") == "Truncate"


def test_nombre_playlist_acepta_ambos_separadores():
    assert nombre_playlist("Sesiones Hipnotico\\Playlist\\tz23") == "Sesiones Hipnotico - tz23"
    assert nombre_playlist("Sesiones Hipnotico/Playlist/tz23") == "Sesiones Hipnotico - tz23"


def test_union_find_es_transitivo():
    uf = UnionFind(4)
    uf.unir(0, 1)          # 0 y 1 se llaman igual
    uf.unir(1, 2)          # 1 y 2 tienen el mismo audio
    assert uf.raiz(0) == uf.raiz(2)
    assert uf.raiz(3) != uf.raiz(0)
