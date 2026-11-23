# Music Library Organizer

**[English](#english) · [Español](#español)**

---

## English

A skill for Claude Code (and other agents) that checks a **music library of any genre**, DJ libraries included. It finds duplicates and broken downloads and tells you how much space they waste. **It never moves or deletes a file.**

### Two editions

```
                │ music-library-   │ music-library-
                │ organizer        │ organizer-pro
────────────────┼──────────────────┼─────────────────
Price           │ Free             │ Paid (Agensi)
Where           │ This repo        │ Agensi
Inventory       │ Yes              │ Yes
Broken files    │ Yes              │ Yes
Duplicates      │ Yes              │ Yes
Organize files  │ No               │ Yes
Playlists .m3u8 │ No               │ Yes
Undo            │ Not needed       │ Yes
```

The free edition (this plugin) only reads. The Pro edition, `music-library-organizer-pro`, also tidies the library up. It is coming soon to [Agensi](https://agensi.io).

### How it works

```
[Inventory] → [Duplicates] → Report
 read only     read only       │
                               ▼
            Pro only: [Dry run] → OK? ─ yes → [Organize]
                                  │
                                  no → nothing changes
```

The free edition stops at the report. Everything it writes goes to `<library>/_mlo/output/` as CSV files.

### What the Pro edition does with your folders

```
Music/                       Library/
├─ Techno 2019/              ├─ Artist A/
│  ├─ track1.flac   ──────▶  │  └─ Track 1 - Artist A.flac
│  └─ track1 (1).mp3 ─────▶  _Quarantine/  (extra copy)
└─ Warm-up/                  Playlists/
   └─ track1.flac            ├─ Techno 2019.m3u8
                             └─ Warm-up.m3u8
```

One copy of each track stays on disk, and every old folder becomes a playlist. Nothing is deleted: extra copies go to `_Quarantine/` and everything can be undone.

### Results on a real library

| | Before | After (Pro) |
|---|---|---|
| Audio files | 4,754 (157.6 GB) | **3,559 unique tracks (126.6 GB)** |
| Space recovered | | **31.2 GB** (996 redundant copies) |
| Broken downloads detected | undetected | **199** (196 empty + 3 truncated) |
| Playlists | 32 folders | **32 `.m3u8` playlists** in their original order |

The free edition shows the same figures in its report; only the Pro edition applies them.

### Install

```
/plugin marketplace add joseantoniopastorrivera-dev/claude-code-skills
/plugin install music-library-organizer@claude-code-skills
```

It needs Python 3.8+ and `pip install mutagen`. Then ask Claude something like "check my music library in D:\Music".

### Linux

It works the same on Linux: use `python3` and `pip install mutagen` (or your distribution's `python3-mutagen` package). A test on a Linux virtual machine is still pending.

### Languages

The skill works in English, Spanish and Dutch (`--lang en|es|nl`). Would you like another language? [Open an issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues) with the language you need.

### License

Free to use, redistribution not allowed: see [LICENSE](LICENSE). This plugin does **not** use the MIT license of the rest of the repository. Versions 1.x, published earlier in this repository, remain MIT.

---

## Español

Skill para Claude Code (y otros agentes) que revisa una **biblioteca musical de cualquier género**, también de DJ. Encuentra los duplicados y las descargas rotas y te dice cuánto espacio desperdician. **Nunca mueve ni borra un archivo.**

### Dos ediciones

```
                │ music-library-   │ music-library-
                │ organizer        │ organizer-pro
────────────────┼──────────────────┼─────────────────
Precio          │ Gratis           │ De pago (Agensi)
Dónde           │ Este repo        │ Agensi
Inventario      │ Sí               │ Sí
Archivos rotos  │ Sí               │ Sí
Duplicados      │ Sí               │ Sí
Ordenar         │ No               │ Sí
Playlists .m3u8 │ No               │ Sí
Deshacer        │ No hace falta    │ Sí
```

La edición gratuita (este plugin) solo lee. La edición Pro, `music-library-organizer-pro`, además ordena la biblioteca. Llegará pronto a [Agensi](https://agensi.io).

### Cómo trabaja

```
[Inventario] → [Duplicados] → Informe
 solo lectura   solo lectura     │
                                 ▼
          Solo Pro: [Simulación] → ¿Bien? ─ sí → [Ordenar]
                                   │
                                   no → no cambia nada
```

La edición gratuita se queda en el informe. Todo lo que escribe va a `<biblioteca>/_mlo/output/` en ficheros CSV.

### Qué hace la edición Pro con tus carpetas

```
Musica/                      Biblioteca/
├─ Techno 2019/              ├─ Artista A/
│  ├─ tema1.flac    ──────▶  │  └─ Tema 1 - Artista A.flac
│  └─ tema1 (1).mp3 ──────▶  _Cuarentena/  (copia sobrante)
└─ Warm-up/                  Listas/
   └─ tema1.flac             ├─ Techno 2019.m3u8
                             └─ Warm-up.m3u8
```

En disco queda una sola copia de cada tema y cada carpeta antigua se convierte en una playlist. No se borra nada: las copias sobrantes van a `_Cuarentena/` (con `--lang es`) y todo se puede deshacer.

### Resultado en una biblioteca real

| | Antes | Después (Pro) |
|---|---|---|
| Archivos de audio | 4.754 (157,6 GB) | **3.559 canciones únicas (126,6 GB)** |
| Espacio recuperado | | **31,2 GB** (996 copias sobrantes) |
| Descargas rotas detectadas | sin detectar | **199** (196 vacías + 3 a medias) |
| Listas | 32 carpetas | **32 playlists `.m3u8`** con su orden original |

La edición gratuita enseña las mismas cifras en su informe; solo la Pro las aplica.

### Instalación

```
/plugin marketplace add joseantoniopastorrivera-dev/claude-code-skills
/plugin install music-library-organizer@claude-code-skills
```

Necesita Python 3.8+ y `pip install mutagen`. Después pide a Claude algo como «revisa mi biblioteca de música en D:\Musica».

### Linux

Funciona igual en Linux: usa `python3` y `pip install mutagen` (o el paquete `python3-mutagen` de tu distribución). Queda pendiente una prueba en una máquina virtual Linux.

### Idiomas

La skill funciona en inglés, español y neerlandés (`--lang en|es|nl`). ¿Quieres otro idioma? [Abre una issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues) con el idioma que necesitas.

### Licencia

Uso gratuito, sin permiso de redistribución: ver [LICENSE](LICENSE). Este plugin **no** usa la licencia MIT del resto del repositorio. Las versiones 1.x, publicadas antes en este repositorio, siguen siendo MIT.

---

**Author / Autor:** José Antonio Pastor Rivera
