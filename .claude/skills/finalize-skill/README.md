# finalize-skill ✅

Repository skill that is always run before a skill is treated as finished, in this repository and in the private one.

## What it does

1. 🐧 **Linux review:** does the skill make sense on Linux, what changes and whether the code already handles it.
2. ✅ **Checks:** tests, `SKILL.md` frontmatter, no personal data, zips.
3. 📄 **Final report** in PDF, DOCX and ODT plus an English PDF, with the same 12 sections for every skill. The latest report stays in `docs/informes/` and every version is archived in `docs/informes/historicos/` (`<skill>-v0-1-0.pdf`…).
4. 📘 **README** completed with what was finally done.
5. 🚀 **Proposed improvements** for the next version; the author decides.

Each step waits for the author's approval. Commits go one per change, each pushed, and only when the author asks.

## How to use it

Type `/finalize-skill` in Claude Code inside this repository, or say that a skill is finished.

## Report

Version 0.1.0: [Spanish PDF](docs/informes/finalize-skill.pdf) ([DOCX](docs/informes/finalize-skill.docx), [ODT](docs/informes/finalize-skill.odt)) and [English PDF](docs/informes/finalize-skill-en.pdf). Every version is kept in [`docs/informes/historicos/`](docs/informes/historicos/).

## Linux

The checklist works the same. The manual conversion script `scripts/aoo_convert.py` still has Windows paths; the preferred path (`styled-docs`) already finds OpenOffice on Linux.

---

# finalize-skill ✅ (español)

Skill del repositorio que se pasa siempre antes de dar una skill por terminada, aquí y en el repositorio privado.

1. 🐧 **Revisión Linux:** si tiene sentido en Linux, qué cambia y si el código ya lo contempla.
2. ✅ **Comprobaciones:** tests, cabecera del `SKILL.md`, sin datos personales, zips.
3. 📄 **Informe final** en PDF, DOCX y ODT más un PDF en inglés, con los mismos 12 apartados para todas las skills. El último informe se queda en `docs/informes/` y cada versión se archiva en `docs/informes/historicos/` (`<skill>-v0-1-0.pdf`…).
4. 📘 **README** completado con lo que finalmente se hizo.
5. 🚀 **Propuestas de mejora** para la siguiente versión; decide el autor.

Cada paso espera la aprobación del autor. Los commits van uno por cambio, cada uno con su push, y solo cuando el autor lo pide.

**Uso:** escribe `/finalize-skill` en Claude Code dentro de este repositorio, o di que una skill está terminada.

**Informe** de la versión 0.1.0: [PDF en español](docs/informes/finalize-skill.pdf) ([DOCX](docs/informes/finalize-skill.docx), [ODT](docs/informes/finalize-skill.odt)) y [PDF en inglés](docs/informes/finalize-skill-en.pdf). Todas las versiones se guardan en [`docs/informes/historicos/`](docs/informes/historicos/).

¿Necesitas el README en otro idioma? Abre una issue.
