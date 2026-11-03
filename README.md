# Techno Library Organizer

**[Español](#español) · [English](#english)**

---

## Español

Herramienta en Python para **limpiar y ordenar una biblioteca musical de DJ**. Elimina los duplicados, detecta las descargas rotas y conserva **en qué listas estuvo cada canción**. Cada carpeta antigua se convierte en una playlist y en disco queda una sola copia de cada tema.

> Este repositorio solo contiene código y datos de ejemplo inventados. **No incluye ningún archivo de audio**. El `.gitignore` bloquea los formatos de audio y los CSV generados.

### El problema

Con el tiempo, una biblioteca de techno organizada en carpetas por fechas o descargas ("Enero26", "Mayo2025 Parte 3", "Descargas de un amigo"…) acumula:

- la misma canción copiada en 4, 5 u 8 carpetas, a veces en FLAC y en AAC a la vez;
- el mismo tema con nombres distintos (`01. Artista - Tema` / `149 - Artista, Sello - Tema`);
- descargas que fallaron y quedaron en **0 bytes** o **a medias**, aunque parecen canciones normales.

### Resultado en la biblioteca real

| | Antes | Después |
|---|---|---|
| Archivos de audio | 4.754 (157,6 GB) | **3.559 canciones únicas (126,6 GB)** |
| Espacio recuperado | | **31,2 GB** (996 copias sobrantes) |
| Descargas rotas detectadas | sin detectar | **199** (196 vacías + 3 a medias) |
| Listas | 32 carpetas | **32 playlists `.m3u8`** con su orden original |

La comprobación posterior (volver a pasar el inventario) dio `3559 | Rotos: 0 | Truncados: 0`.

### Cómo funciona: 3 fases

```
inventario.py  ──►  duplicados.py  ──►  organizar.py
(solo lectura)      (solo lectura)      simular → ejecutar → (deshacer)
```

1. **`inventario.py`**: recorre la biblioteca y lee las etiquetas y la calidad de cada archivo con `mutagen`. Marca como `ROTO` o `TRUNCADO` los archivos que no son válidos y calcula el SHA-256 **solo de los archivos que comparten tamaño con otro**, porque dos archivos de distinto tamaño no pueden ser idénticos.
2. **`duplicados.py`**: agrupa las canciones con **Union-Find** a partir de tres pistas: el nombre normalizado, el SHA-256 y el **MD5 de audio que cada FLAC guarda en su cabecera**. Este último detecta el mismo audio aunque tenga otras etiquetas. Después elige la mejor copia (sin pérdida > kbps > etiquetas) y reconstruye el historial de listas de cada canción.
3. **`organizar.py`**: por defecto **simula**. Con `--ejecutar` mueve cada canción a `Biblioteca/<Artista>/<Título> - <Artista>.ext`, lleva los sobrantes y los rotos a `_Cuarentena/` (no borra nada) y genera las playlists. Cada movimiento queda anotado en un registro, así que `--deshacer` lo revierte todo.

### Uso

```bash
pip install -r requirements.txt

# Probar con una biblioteca falsa (tonos WAV generados con la librería estándar)
python ejemplos/crear_biblioteca_prueba.py biblioteca_prueba
python src/inventario.py biblioteca_prueba
python src/duplicados.py biblioteca_prueba/_herramientas/salida/inventario.csv
python src/organizar.py biblioteca_prueba               # simulación
python src/organizar.py biblioteca_prueba --ejecutar
python src/organizar.py biblioteca_prueba --deshacer

# Tests
python -m pytest
```

Lo que se aprendió por el camino (las etiquetas pierden el nombre del remix, artistas con "/" en el nombre, un "remix" que en realidad era la versión original…) está en [`docs/decisiones.md`](docs/decisiones.md).

### Tecnologías

Python 3.8+ · [mutagen](https://github.com/quodlibet/mutagen) · pytest

---

## English

A Python tool to **clean up and organize a DJ music library**. It removes duplicates, detects broken downloads and **keeps track of which playlists each song belonged to**. Every old folder becomes a playlist, and only one copy of each track is kept on disk.

> This repository contains only code and made-up sample data. **No audio files are included**. The `.gitignore` blocks audio formats and generated CSVs.

### The problem

Over time, a techno library organized into folders by date or by download batch accumulates:

- the same track copied into 4, 5 or 8 folders, sometimes as both FLAC and AAC;
- the same track under different names (`01. Artist - Track` / `149 - Artist, Label - Track`);
- downloads that failed and were left at **0 bytes** or **half-finished**, even though they look like normal tracks.

### Results on the real library

| | Before | After |
|---|---|---|
| Audio files | 4,754 (157.6 GB) | **3,559 unique tracks (126.6 GB)** |
| Space recovered | | **31.2 GB** (996 redundant copies) |
| Broken downloads detected | undetected | **199** (196 empty + 3 truncated) |
| Playlists | 32 folders | **32 `.m3u8` playlists** in their original order |

The follow-up check (running the inventory again) returned `3559 | Broken: 0 | Truncated: 0`.

### How it works: 3 phases

1. **`inventario.py`** (read-only): reads tags and audio quality with `mutagen`. Flags `ROTO` (broken) and `TRUNCADO` (truncated) files by comparing file size with duration, and computes SHA-256 **only for files that share a size with another file**, since files of different sizes can't be identical.
2. **`duplicados.py`** (read-only): groups tracks with **Union-Find** using three signals: the normalized filename, the SHA-256 and the **audio MD5 that every FLAC file stores in its header**. The last one catches identical audio even when the tags differ. It then picks the best copy (lossless > bitrate > tags) and rebuilds each track's playlist history.
3. **`organizar.py`**: runs as a **dry run by default**. With `--ejecutar` it moves each track to `Biblioteca/<Artist>/<Title> - <Artist>.ext`, sends redundant and broken files to `_Cuarentena/` (quarantine; nothing is deleted) and writes the playlists. Every move is journaled, so `--deshacer` (undo) reverts everything.

### Usage

See the commands in the Spanish section above. The script names and output messages are in Spanish.

### Tech

Python 3.8+ · [mutagen](https://github.com/quodlibet/mutagen) · pytest

---

**Autor / Author:** José Antonio Pastor Rivera — Estudiante de DAM / Cross-platform app development student
