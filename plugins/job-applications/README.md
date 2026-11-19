# 💼 job-applications

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

Applying for an internship or a first job means rewriting the same CV and cover letter for every offer, and it is easy to overstate a skill or forget a requirement. This plugin works from a single **master profile** with everything you can really do, and tailors it to each offer without inventing anything.

### 🛟 How it works

```
offer (link or text)
        │
        ▼
[analyze-job-offer] ─▶ fit: high / medium / low
        │ apply?
        ▼
[tailor-cv-and-cover-letter] ─▶ CV + letter (PDF)
        │ you review
        ▼
[prepare-application] ─▶ form filled, NOT sent
        │
        ▼
     you press "Send"
```

### 🧰 The skills

| | Skill | What it does |
|---|---|---|
| 🔎 | `analyze-job-offer` | Turns an offer into a short sheet: requirements, keywords, fit with your profile and warnings. |
| ✍️ | `tailor-cv-and-cover-letter` | Writes a one-page CV and a cover letter for that offer, only with what is in your master profile, as plain ATS-friendly PDFs. |
| 📨 | `prepare-application` | Prepares the form answers, fills in the form or an email draft without sending it, and keeps a tracking table. |

### 🚫 What it will never do

- Invent experience or skills that are not in your master profile.
- Press "Send", sign up or send an email for you.
- Type passwords, ID numbers or bank details.
- Apply in bulk: one offer at a time, chosen by you.

### 💻 Platforms

Any system with Python 3 and `reportlab` for the PDFs. Filling in web forms needs a browser tool in Claude.

### 📦 Editions

```
┌────────────────────────────────────────┐
│ job-applications-pro (paid)            │
│  ┌──────────────────────────────────┐  │
│  │ job-applications (free)          │  │
│  │  - analyze-job-offer             │  │
│  └──────────────────────────────────┘  │
│  + tailored CV and letter (PDF)        │
│  + prepare-application and tracking    │
└────────────────────────────────────────┘
```

The split between editions is not final yet.

### 🗺️ Roadmap

- [x] Used on real applications
- [x] Code and skills in English
- [ ] Generalize (job portals, countries, CV formats)
- [ ] Linux review
- [ ] Free edition published here

### ❓ FAQ

**Does it store my data online?** No. Your master profile, CVs and tracking stay in a folder on your computer.

**Another language?** The documents are written in the language of the offer. For another interface language, [open an issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

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

Buscar prácticas o un primer empleo obliga a reescribir el mismo CV y la misma carta para cada oferta, y es fácil exagerar una competencia u olvidar un requisito. Este plugin trabaja con un único **perfil maestro** con todo lo que de verdad sabes hacer y lo adapta a cada oferta sin inventar nada.

### 🛟 Cómo trabaja

```
oferta (enlace o texto)
        │
        ▼
[analyze-job-offer] ─▶ encaje: alto / medio / bajo
        │ ¿te presentas?
        ▼
[tailor-cv-and-cover-letter] ─▶ CV + carta (PDF)
        │ tú lo revisas
        ▼
[prepare-application] ─▶ formulario relleno, SIN enviar
        │
        ▼
     tú pulsas «Enviar»
```

### 🧰 Las skills

| | Skill | Qué hace |
|---|---|---|
| 🔎 | `analyze-job-offer` | Convierte una oferta en una ficha corta: requisitos, palabras clave, encaje con tu perfil y avisos. |
| ✍️ | `tailor-cv-and-cover-letter` | Escribe un CV de una página y una carta para esa oferta, solo con lo que está en tu perfil maestro, en PDF sobrio que leen bien los filtros (ATS). |
| 📨 | `prepare-application` | Prepara las respuestas del formulario, lo rellena (o deja un borrador de correo) sin enviarlo y lleva una tabla de seguimiento. |

### 🚫 Lo que nunca hará

- Inventar experiencia o competencias que no están en tu perfil maestro.
- Pulsar «Enviar», inscribirse o mandar un correo por ti.
- Escribir contraseñas, DNI ni datos bancarios.
- Presentar candidaturas en masa: una oferta cada vez, elegida por ti.

### 💻 Plataformas

Cualquier sistema con Python 3 y `reportlab` para los PDF. Para rellenar formularios web, Claude necesita una herramienta de navegador.

### 📦 Ediciones

```
┌────────────────────────────────────────┐
│ job-applications-pro (de pago)         │
│  ┌──────────────────────────────────┐  │
│  │ job-applications (gratis)        │  │
│  │  - analyze-job-offer             │  │
│  └──────────────────────────────────┘  │
│  + CV y carta adaptados (PDF)          │
│  + prepare-application y seguimiento   │
└────────────────────────────────────────┘
```

El reparto entre ediciones todavía no es definitivo.

### 🗺️ Hoja de ruta

- [x] Usado en candidaturas reales
- [x] Código y skills en inglés
- [ ] Generalizar (portales de empleo, países, formatos de CV)
- [ ] Revisión en Linux
- [ ] Edición gratuita publicada aquí

### ❓ Preguntas frecuentes

**¿Guarda mis datos en internet?** No. Tu perfil maestro, tus CV y el seguimiento se quedan en una carpeta de tu ordenador.

**¿Otro idioma?** Los documentos salen en el idioma de la oferta. Para otro idioma de la skill, [abre una issue](https://github.com/joseantoniopastorrivera-dev/claude-code-skills/issues).

---

> 🚧 **Under construction / En construcción.**

**Author / Autor:** José Antonio Pastor Rivera
