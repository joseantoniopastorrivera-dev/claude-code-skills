# 🧭 phased-development

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

A project with a roadmap in phases tends to go wrong in the same places: code written before the plan is agreed, no backup before touching real data, no test baseline, and a phase "finished" that nobody has tried with a real user. This plugin turns every phase into the same safe routine.

### 🛟 How it works

```
 prepare-phase                     phase-test-plan
┌───────────────┐   ┌──────────┐   ┌────────────────┐
│ branch        │   │          │   │ printable plan │
│ backup        │──▶│ the work │──▶│ round 1: test  │
│ test baseline │   │ (commits)│   │ round 2: real  │
│ plan -> STOP  │   │          │   │ data, results  │
└───────────────┘   └──────────┘   └────────────────┘
```

No code is written until you approve the plan.

### 🧰 The skills

| | Skill | What it does |
|---|---|---|
| 🚦 | `prepare-phase` | Creates the phase branch, makes the backup, checks the tests and presents a step-by-step plan, then stops. |
| 🧪 | `phase-test-plan` | Writes a printable test plan (Markdown and PDF) for a real person to test the phase. |

Each project keeps its own data (roadmap path, test command, who tests) in a "Phase skills" section of its `CLAUDE.md`, so the skills stay generic.

### 🚫 What it will never do

- Write code for a phase before you approve the plan.
- Open or read your real data when it backs it up: it only copies the file.
- Commit when the tests fail.
- Edit a database migration that has already been applied.

### 💻 Platforms

Windows, Linux and macOS: it only needs git and the project's own test command.

### 📦 Editions

```
┌────────────────────────────────────────┐
│ phased-development-pro (paid)          │
│  ┌──────────────────────────────────┐  │
│  │ phased-development (free)        │  │
│  │  - prepare-phase                 │  │
│  └──────────────────────────────────┘  │
│  + phase-test-plan (Markdown + PDF)    │
└────────────────────────────────────────┘
```

The split between editions is not final yet.

### 🗺️ Roadmap

- [x] Both skills used on real projects
- [x] Code and skills in English
- [ ] Generalize for any project and language
- [ ] Linux review
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

Un proyecto con una hoja de ruta por fases suele torcerse en los mismos sitios: se escribe código antes de acordar el plan, no se hace copia antes de tocar datos reales, no hay línea base de tests y se da por «terminada» una fase que nadie ha probado con una persona real. Este plugin convierte cada fase en la misma rutina segura.

### 🛟 Cómo trabaja

```
 prepare-phase                     phase-test-plan
┌───────────────┐   ┌──────────┐   ┌────────────────┐
│ rama          │   │          │   │ plan imprimible│
│ copia         │──▶│ trabajo  │──▶│ ronda 1: prueba│
│ tests base    │   │ (commits)│   │ ronda 2: datos │
│ plan -> PARA  │   │          │   │ reales, result.│
└───────────────┘   └──────────┘   └────────────────┘
```

No se escribe código hasta que apruebas el plan.

### 🧰 Las skills

| | Skill | Qué hace |
|---|---|---|
| 🚦 | `prepare-phase` | Crea la rama de la fase, hace la copia de seguridad, comprueba los tests y presenta un plan por pasos, y para. |
| 🧪 | `phase-test-plan` | Escribe un plan de pruebas imprimible (Markdown y PDF) para que una persona real pruebe la fase. |

Cada proyecto guarda sus datos (hoja de ruta, comando de tests, quién prueba) en una sección «Phase skills» de su `CLAUDE.md`, así las skills siguen siendo genéricas.

### 🚫 Lo que nunca hará

- Escribir código de una fase antes de que apruebes el plan.
- Abrir o leer tus datos reales al hacer la copia: solo copia el fichero.
- Hacer commit con los tests en rojo.
- Editar una migración de base de datos ya aplicada.

### 💻 Plataformas

Windows, Linux y macOS: solo necesita git y el comando de tests del proyecto.

### 📦 Ediciones

```
┌────────────────────────────────────────┐
│ phased-development-pro (de pago)       │
│  ┌──────────────────────────────────┐  │
│  │ phased-development (gratis)      │  │
│  │  - prepare-phase                 │  │
│  └──────────────────────────────────┘  │
│  + phase-test-plan (Markdown + PDF)    │
└────────────────────────────────────────┘
```

El reparto entre ediciones todavía no es definitivo.

### 🗺️ Hoja de ruta

- [x] Las dos skills usadas en proyectos reales
- [x] Código y skills en inglés
- [ ] Generalizar para cualquier proyecto e idioma
- [ ] Revisión en Linux
- [ ] Edición gratuita publicada aquí

### ❓ Preguntas frecuentes

**¿Estuvo publicado antes?** Sí: la versión 1 (en español) estuvo en este repositorio con licencia MIT, y esa versión sigue siendo MIT. La versión nueva se desarrolla en privado.

**¿Otro idioma?** [Abre una issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

> 🚧 **Under construction / En construcción.**

**Author / Autor:** José Antonio Pastor Rivera
