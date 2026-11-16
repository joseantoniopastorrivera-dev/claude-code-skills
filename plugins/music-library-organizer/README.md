# Music Library Organizer

**[Español](#español) · [English](#english)**

---

## Español

Skill para Claude Code (y otros agentes) que **limpia y ordena una biblioteca musical de cualquier género**, también de DJ. Quita los duplicados, detecta las descargas rotas y conserva **en qué listas estuvo cada canción**. Cada carpeta antigua se convierte en una playlist y en disco queda una sola copia de cada tema.

### Resultado en una biblioteca real

| | Antes | Después |
|---|---|---|
| Archivos de audio | 4.754 (157,6 GB) | **3.559 canciones únicas (126,6 GB)** |
| Espacio recuperado | | **31,2 GB** (996 copias sobrantes) |
| Descargas rotas detectadas | sin detectar | **199** (196 vacías + 3 a medias) |
| Listas | 32 carpetas | **32 playlists `.m3u8`** con su orden original |

### Cómo trabaja

1. **Inventario** (solo lectura): lee la calidad real de cada archivo y marca los rotos y los que se descargaron a medias.
2. **Duplicados** (solo lectura): reconoce la misma canción por el nombre, por el contenido del archivo y por la huella de audio del FLAC, aunque tenga otras etiquetas, y elige la mejor copia.
3. **Organizar**: primero simula; después mueve a `Biblioteca/<Artista>/<Título> - <Artista>`, crea las playlists y lleva lo sobrante a una cuarentena. Nunca borra nada y todo se puede deshacer.

### Ediciones

- **Lite** (gratis): el informe de solo lectura (duplicados, descargas rotas y espacio desperdiciado).
- **Pro** (de pago): además organiza la biblioteca, reconstruye las playlists y permite deshacer.

En inglés, español y neerlandés. Disponible próximamente en [Agensi](https://agensi.io).

---

## English

A skill for Claude Code (and other agents) that **cleans up and organizes a music library of any genre**, DJ libraries included. It removes duplicates, detects broken downloads and **keeps track of which playlists each track belonged to**. Every old folder becomes a playlist, and only one copy of each track is kept on disk.

### Results on a real library

| | Before | After |
|---|---|---|
| Audio files | 4,754 (157.6 GB) | **3,559 unique tracks (126.6 GB)** |
| Space recovered | | **31.2 GB** (996 redundant copies) |
| Broken downloads detected | undetected | **199** (196 empty + 3 truncated) |
| Playlists | 32 folders | **32 `.m3u8` playlists** in their original order |

### How it works

1. **Inventory** (read only): reads the real quality of every file and flags broken and half-finished downloads.
2. **Duplicates** (read only): recognizes the same track by name, by file content and by the FLAC audio fingerprint, even with different tags, and picks the best copy.
3. **Organize**: dry run first; then moves tracks to `Library/<Artist>/<Title> - <Artist>`, writes the playlists and sends extras to a quarantine folder. Nothing is ever deleted and everything can be undone.

### Editions

- **Lite** (free): the read-only report (duplicates, broken downloads and wasted space).
- **Pro** (paid): also organizes the library, rebuilds the playlists and supports undo.

In English, Spanish and Dutch. Coming soon on [Agensi](https://agensi.io).

---

**Autor / Author:** José Antonio Pastor Rivera
