# ✏️ create-ascii-art

> 🚧 **Under construction.** This plugin cannot be installed yet. This README explains what it will be.

**[English](#english) · [Español](#español)**

---

## English

### 📑 Contents

1. [Why it exists](#-why-it-exists)
2. [How it works](#-how-it-works)
3. [Diagram types](#-diagram-types)
4. [What it will never do](#-what-it-will-never-do)
5. [Platforms](#-platforms)
6. [Editions](#-editions)
7. [Roadmap](#-roadmap)
8. [FAQ](#-faq)

### 🎯 Why it exists

Some explanations are long in words and obvious in a drawing: a folder tree, the layers of an app, the steps of a process. When you follow Claude from a phone or a terminal, images and rendered diagrams are often not available, but plain text always is. This skill draws those explanations as text that fits on a phone screen.

### 🛟 How it works

```
long explanation
       │
       ▼
pick a type ─▶ tree | layers | flow | table | timeline
       │
       ▼
draw it: max ~60 columns, in a code block
       │
       ▼
one line of explanation below the drawing
```

Other skills will use it too: for example, to show a rename preview as a "before → after" tree and ask for approval.

### 🧰 Diagram types

| Type | Good for |
|---|---|
| Tree (before → after) | Renames, moves, migrations |
| Layers | Architecture of an app |
| Flow | Steps of a process, with decisions |
| Table | Comparing options |
| Timeline | Phases, years, versions |
| States | Life cycle of a thread or an order |

Small example (a flow):

```
[Read] → [Report] → [Plan] → OK? ─ yes → [Apply]
                               │
                               no → [Fix plan]
```

### 🚫 What it will never do

- Put emojis inside a drawing: they take two columns and break the alignment.
- Draw wider than a phone screen without splitting the diagram.
- Replace real image tools when you do need an image.

### 💻 Platforms

Any: it is plain text. Unicode box characters by default, plain ASCII (`+--`, `|--`, `->`) for old consoles or files that may break the encoding.

### 📦 Editions

```
┌────────────────────────────────────────┐
│ create-ascii-art-pro (paid)            │
│  ┌──────────────────────────────────┐  │
│  │ create-ascii-art (free)          │  │
│  │  - style rules and templates     │  │
│  └──────────────────────────────────┘  │
│  + exact alignment script              │
└────────────────────────────────────────┘
```

Whether it will have a paid edition is not decided yet: it may stay a free building block for other skills.

### 🗺️ Roadmap

- [x] Style rules written
- [ ] Skill and templates
- [ ] Used by other skills for previews
- [ ] Free edition published here

### ❓ FAQ

**Why not Mermaid?** Mermaid needs a renderer. On a phone or in a terminal you would only see its source code.

**Another language?** [Open an issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

## Español

### 📑 Índice

1. [Por qué existe](#-por-qué-existe)
2. [Cómo trabaja](#-cómo-trabaja)
3. [Tipos de diagrama](#-tipos-de-diagrama)
4. [Lo que nunca hará](#-lo-que-nunca-hará)
5. [Plataformas](#-plataformas)
6. [Ediciones](#-ediciones)
7. [Hoja de ruta](#️-hoja-de-ruta)
8. [Preguntas frecuentes](#-preguntas-frecuentes)

### 🎯 Por qué existe

Hay explicaciones que son largas con palabras y evidentes con un dibujo: un árbol de carpetas, las capas de una aplicación, los pasos de un proceso. Cuando sigues a Claude desde el móvil o desde un terminal, muchas veces no hay imágenes ni diagramas renderizados, pero el texto plano siempre está. Esta skill dibuja esas explicaciones como texto que cabe en la pantalla del móvil.

### 🛟 Cómo trabaja

```
explicación larga
       │
       ▼
elige un tipo ─▶ árbol | capas | flujo | tabla | tiempo
       │
       ▼
lo dibuja: ~60 columnas como máximo, en un bloque
       │
       ▼
una línea de explicación debajo del dibujo
```

Otras skills también la usarán: por ejemplo, para enseñar la vista previa de un renombrado como un árbol «antes → después» y pedir la aprobación.

### 🧰 Tipos de diagrama

| Tipo | Sirve para |
|---|---|
| Árbol (antes → después) | Renombrados, movimientos, migraciones |
| Capas | Arquitectura de una aplicación |
| Flujo | Pasos de un proceso, con decisiones |
| Tabla | Comparar opciones |
| Línea de tiempo | Fases, cursos, versiones |
| Estados | Ciclo de vida de un hilo o un pedido |

Ejemplo pequeño (un flujo):

```
[Leer] → [Informe] → [Plan] → ¿Bien? ─ sí → [Aplicar]
                                 │
                                 no → [Corregir plan]
```

### 🚫 Lo que nunca hará

- Meter emojis dentro de un dibujo: ocupan dos columnas y descuadran la alineación.
- Dibujar más ancho que la pantalla del móvil sin partir el diagrama.
- Sustituir a las herramientas de imagen cuando de verdad necesitas una imagen.

### 💻 Plataformas

Todas: es texto plano. Caracteres de caja Unicode por defecto y ASCII puro (`+--`, `|--`, `->`) para consolas antiguas o ficheros que pueden romper la codificación.

### 📦 Ediciones

```
┌────────────────────────────────────────┐
│ create-ascii-art-pro (de pago)         │
│  ┌──────────────────────────────────┐  │
│  │ create-ascii-art (gratis)        │  │
│  │  - reglas de estilo y plantillas │  │
│  └──────────────────────────────────┘  │
│  + script de alineación exacta         │
└────────────────────────────────────────┘
```

Todavía no está decidido si tendrá edición de pago: puede quedarse como una pieza gratuita para otras skills.

### 🗺️ Hoja de ruta

- [x] Reglas de estilo escritas
- [ ] Skill y plantillas
- [ ] Usada por otras skills para las vistas previas
- [ ] Edición gratuita publicada aquí

### ❓ Preguntas frecuentes

**¿Por qué no Mermaid?** Mermaid necesita un programa que lo dibuje. En el móvil o en un terminal solo verías su código.

**¿Otro idioma?** [Abre una issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

> 🚧 **Under construction / En construcción.**

**Author / Autor:** José Antonio Pastor Rivera
