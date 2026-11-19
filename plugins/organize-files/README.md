# 🗂️ organize-files

> 🚧 **Under construction.** This plugin cannot be installed yet. This README explains what it will be.

**[English](#english) · [Español](#español)**

---

## English

### 📑 Contents

1. [Why it exists](#-why-it-exists)
2. [How it works](#-how-it-works)
3. [The skills](#-the-skills)
4. [What it will never do](#-what-it-will-never-do)
5. [Platforms](#-platforms)
6. [Editions](#-editions)
7. [Roadmap](#-roadmap)
8. [FAQ](#-faq)

### 🎯 Why it exists

A student downloads dozens of class documents a week. They pile up in Downloads with names like `Tema 3 FINAL (1).pdf`, and the course repositories end up with names full of spaces, accents and capitals that break links and scripts. This plugin files each document in the right place, with a clean name, without losing git history.

### 🛟 How it works

```
Downloads/                     C:\dev\<subject repo>/
├─ Tema 3 Hilos PSP.pdf ────▶  └─ ut3-threads/
├─ ut2 ingles/                    └─ tema-3-hilos-psp.pdf
│  └─ Unit 2.docx ──────────▶  ingles-profesional/ut2-…/
└─ Libro (1).pdf  ──────────▶  Recycle Bin (duplicate)
```

Always the same order: dry run, plan, your approval, then the move. Nothing is overwritten and duplicates go to the Recycle Bin, never deleted.

### 🧰 The skills

| | Skill | What it does |
|---|---|---|
| 🏷️ | `normalize-names` | Renames documents and folders in one or many git repos to lowercase with hyphens, with `git mv` so history is kept, and fixes the paths that mention them. |
| 📥 | `classify-downloads` | Moves downloaded documents to the folder of their unit in the subject's repo, finds duplicates by content and asks about anything unclear. |

### 🚫 What it will never do

- Rename Java or Python package folders, or tool folders (`src/`, `.github/`, `docs/`…).
- Overwrite a file that already exists.
- Delete a file: duplicates go to the Recycle Bin, where they can be restored.
- Commit or push without being asked.

### 💻 Platforms

Windows today (the Recycle Bin step uses PowerShell). Renaming works anywhere with Python and git; the Linux review is pending.

### 📦 Editions

```
┌────────────────────────────────────────┐
│ organize-files-pro (paid)              │
│  ┌──────────────────────────────────┐  │
│  │ organize-files (free)            │  │
│  │  - dry run and plan only         │  │
│  └──────────────────────────────────┘  │
│  + execute, references, Recycle Bin    │
└────────────────────────────────────────┘
```

The split between editions is not final yet.

### 🗺️ Roadmap

- [x] Both skills used every week on real repositories
- [x] Code and skills in English
- [ ] Generalize the subjects table (today it is the author's own course)
- [ ] Linux and macOS support for the Recycle Bin
- [ ] Free edition published here

### ❓ FAQ

**Was it published before?** Yes: version 1 (in Spanish) was in this repository under the MIT licence, and that version stays MIT. The new version is being developed privately.

**Another language?** [Open an issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

## Español

### 📑 Índice

1. [Por qué existe](#-por-qué-existe)
2. [Cómo trabaja](#-cómo-trabaja)
3. [Las skills](#-las-skills)
4. [Lo que nunca hará](#-lo-que-nunca-hará)
5. [Plataformas](#-plataformas)
6. [Ediciones](#-ediciones)
7. [Hoja de ruta](#️-hoja-de-ruta)
8. [Preguntas frecuentes](#-preguntas-frecuentes)

### 🎯 Por qué existe

Un estudiante descarga decenas de documentos de clase a la semana. Se amontonan en Descargas con nombres como `Tema 3 FINAL (1).pdf`, y los repos de las asignaturas acaban con nombres llenos de espacios, tildes y mayúsculas que rompen enlaces y scripts. Este plugin guarda cada documento en su sitio, con un nombre limpio y sin perder el historial de git.

### 🛟 Cómo trabaja

```
Descargas/                     C:\dev\<repo asignatura>/
├─ Tema 3 Hilos PSP.pdf ────▶  └─ ut3-hilos/
├─ ut2 ingles/                    └─ tema-3-hilos-psp.pdf
│  └─ Unit 2.docx ──────────▶  ingles-profesional/ut2-…/
└─ Libro (1).pdf  ──────────▶  Papelera (duplicado)
```

Siempre en el mismo orden: simulación, plan, tu aprobación y después el movimiento. No se sobrescribe nada y los duplicados van a la Papelera, nunca se borran.

### 🧰 Las skills

| | Skill | Qué hace |
|---|---|---|
| 🏷️ | `normalize-names` | Renombra documentos y carpetas de uno o varios repos git a minúsculas con guiones, con `git mv` para conservar el historial, y arregla las rutas que los citan. |
| 📥 | `classify-downloads` | Lleva los documentos descargados a la carpeta de su UT en el repo de la asignatura, encuentra duplicados por contenido y pregunta lo que no está claro. |

### 🚫 Lo que nunca hará

- Renombrar carpetas de paquetes Java o Python, ni carpetas de herramientas (`src/`, `.github/`, `docs/`…).
- Sobrescribir un archivo que ya existe.
- Borrar un archivo: los duplicados van a la Papelera, de donde se pueden recuperar.
- Hacer commit o push sin que se lo pidas.

### 💻 Plataformas

Hoy, Windows (el paso de la Papelera usa PowerShell). El renombrado funciona en cualquier sistema con Python y git; la revisión en Linux está pendiente.

### 📦 Ediciones

```
┌────────────────────────────────────────┐
│ organize-files-pro (de pago)           │
│  ┌──────────────────────────────────┐  │
│  │ organize-files (gratis)          │  │
│  │  - solo simulación y plan        │  │
│  └──────────────────────────────────┘  │
│  + ejecutar, referencias, Papelera     │
└────────────────────────────────────────┘
```

El reparto entre ediciones todavía no es definitivo.

### 🗺️ Hoja de ruta

- [x] Las dos skills se usan cada semana en repos reales
- [x] Código y skills en inglés
- [ ] Generalizar la tabla de asignaturas (hoy es la del curso del autor)
- [ ] Papelera en Linux y macOS
- [ ] Edición gratuita publicada aquí

### ❓ Preguntas frecuentes

**¿Estuvo publicado antes?** Sí: la versión 1 (en español) estuvo en este repositorio con licencia MIT, y esa versión sigue siendo MIT. La versión nueva se desarrolla en privado.

**¿Otro idioma?** [Abre una issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

> 🚧 **Under construction / En construcción.**

**Author / Autor:** José Antonio Pastor Rivera
