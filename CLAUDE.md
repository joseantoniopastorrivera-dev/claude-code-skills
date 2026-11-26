# claude-code-skills (marketplace de plugins con mis skills de Claude Code)

## Cómo trabajar conmigo
Reglas comunes a todos mis repos (copia de mi `C:\dev\CLAUDE.md`, para que también las lean las sesiones en la nube). Soy estudiante de DAM en el IES Isidra de Guzmán.
- En prácticas evaluables, resuélvelas completas (sin modo de pistas). Al terminar, crea junto a la entrega (en `docs/` si existe) un `guia-defensa-<practica>.md` para defenderla en clase, al estilo de la guía de DataStock. Las guías de defensa no se suben nunca a GitHub: cada repo tiene `guia-defensa-*.md` en su `.gitignore` (añádelo si falta).
- Estructura de la guía de defensa: cómo usarla; cómo arrancar, ejecutar y ensayar sin estropear la entrega; qué pide el enunciado y dónde se cumple cada requisito; visión general (capas, flujo, decisiones de diseño a justificar); y por cada requisito: qué pide, dónde está, explicación línea a línea, cómo demostrarlo, errores típicos, preguntas de la profesora con su respuesta y 🔧 modificaciones en directo (el cambio que podrían pedir, con el código exacto y dónde va). Al final: casos prácticos «¿qué pasaría si…?», «corrige este error» (síntoma → causa → arreglo) y chuleta con plan de ensayo.
- Si la tarea es grande, antes de tocar nada dime cómo lo harías (plan por pasos) y espera a que lo apruebe o lo corrija.
- Cuando escribas código, explícalo línea por línea y di por qué elegiste esa forma y no otra.
- Si ves un error de concepto o algo que no entiendo bien, dímelo aunque no te lo pregunte.
- Responde en español.
- No hagas commit ni push sin que te lo pida. Commits con `Co-Authored-By: Claude <noreply@anthropic.com>` (repo personal); en los repos de asignaturas del grado, nunca.
- **Pull requests en todos los repos (asignaturas y personales):** nunca se commitea directo en `main`. Una rama por cambio (nombre con guiones, sin barra: con barra GitHub dio error 500), sus commits pequeños, `gh pr create --fill --base main`, tests en local y CI en verde (`gh pr checks <n> --watch`), y `gh pr merge <n> --merge --delete-branch` (nunca squash, para que cada commit quede en el historial). Si el repo no tiene tests o CI para lo que cambia, dilo y propón añadirlos. Si la carpeta la comparten otras sesiones, trabaja en un worktree propio y no cambies de rama allí. Sigue valiendo que el commit, push y merge solo se hacen cuando yo lo pida.
- No subas binarios generados (`target/`, `*.class`, `__pycache__/`, `*.pyc`, `bin/`, `obj/`, `Library/` de Unity).
- Nunca leas, muestres ni subas ficheros `.env`, tokens ni credenciales.
- PDFs, .docx, .odt y .pptx son apuntes o enunciados: léelos solo si hacen falta para la tarea.

## Normas de este repo
- **Todas las skills empiezan siendo privadas**: solo para Claude y para mí. Su código no se publica (ni en este repo ni en el portal de skills de Claude) hasta que estén listas para sacarse con versión Lite y Pro, y yo lo decida de forma explícita. Las ideas y el código privado viven en el repo **privado** `claude-code-skills-private` (`C:\dev\claude-code-skills-private`, carpeta `ideas/`), nunca en este repo público.
- **Trabajamos siempre con la versión Pro (completa).** La Lite no se desarrolla aparte: cuando toque publicar, se saca recortando la Pro.
- **Nombres al publicar (también en los README):** la Lite gratuita se llama `<nombre-de-skill>` y la completa, `<nombre-de-skill>-pro`. En el repo privado la completa se llama solo `<nombre-de-skill>`. Al pasar una skill a este repo hay que revisar las dos versiones (qué entra en la Lite y qué queda solo en la Pro).
- **Idioma:** las skills nuevas, solo en inglés (código y `SKILL.md`). Los README publicados van en inglés y debajo en español, y explican cómo pedir otro idioma (abriendo una issue). `music-library-organizer` se queda con sus tres idiomas.
- **Licencia:** un plugin con licencia propia lleva su `LICENSE` en su carpeta y lo dice en su README; el resto del repo es MIT.
- Mientras una skill no tenga versión Lite publicada, en GitHub solo puede haber un **README «en construcción»**: largo, con índice, emoticonos y esquemas en ASCII art, que explique lo que será. Nunca el código ni detalles internos sensibles.
- **Plantilla de esos README**: [plugins/gestor-contrasenas/README.md](plugins/gestor-contrasenas/README.md) y [plugins/optimizar-ordenador/README.md](plugins/optimizar-ordenador/README.md). Estructura:
  - aviso 🚧 arriba y abajo;
  - índice con anclas;
  - por qué existe (un caso real sin datos personales);
  - cómo funciona, con esquemas en ASCII art;
  - tabla de skills o modos;
  - lo que nunca hará;
  - plataformas;
  - ediciones Lite/Pro en cajas anidadas;
  - hoja de ruta con casillas;
  - preguntas frecuentes;
  - autor.
- Mientras estén en construcción, esos plugins no se añaden a `marketplace.json`, pero sí a la sección «🚧 En construcción» del README principal.

## Cerrar una skill
Las skills nuevas se crean con `forge-skill` y ninguna se da por terminada sin pasar por `finalize-skill` (antes `cerrar-skill`). Las dos están en el plugin `skill-lifecycle` del repo privado (`C:\dev\claude-code-skills-private\skill-lifecycle\skills\`). `finalize-skill` hace:
- **Revisión en Linux 🐧:** si tiene sentido en Linux, qué cambia y si el código ya lo contempla. Las pruebas en la máquina virtual Linux del USB se apuntan como pendientes.
- **Informe final** con el nombre de la skill en minúsculas con guiones (reglas de `normalize-names`, plugin `organize-files` del repo privado), en PDF, DOCX y ODT, más un PDF en inglés. Todos los informes tienen el mismo índice, con su emoji detrás del título, también en el índice: portada, índice con enlaces, idea 💡, diseño 🧩, implementación 🛠️, pruebas ✅, incidencias 🐞 (una sola tabla con causa y solución), ajustes tras las pruebas ✏️, integración con otras skills 🔗, revisión Linux 🐧, lecciones aprendidas 🎓, uso de IA 🤖 (elaborado con Claude Code, encargos redactados de forma formal y nunca transcritos), propuestas de mejora 🚀 y referencias 📚.
- **Último informe e históricos:** en `docs/informes/` solo está el último informe; cada versión se archiva también en `docs/informes/historicos/`, renombrada con su versión (`<skill>-v0-1-0.pdf`, `.docx`, `.odt`, `.md`, `-en.pdf`, `-en.md`), desde el primer informe. No se borra ni se pisa ninguna versión anterior.
- **Commits:** uno por cambio (la skill, su informe, su README, una norma…), cada uno con su mensaje y con push después de cada uno; nunca todo mezclado en un commit.
- Con el PDF aprobado, se **completa el README** con lo que finalmente se ha hecho, respetando su formato.
- Cada idea o skill lleva propuestas de mejora de Claude que decido yo: en las ideas, un apartado **«Preguntas de Claude»**; en las skills cerradas, el apartado 🚀 del informe.
- Cada cierre que cambia la skill sube la versión: parche (0.1.0 → 0.1.1) si solo arregla o documenta, menor (0.1.0 → 0.2.0) si la skill hace algo nuevo o distinto.

## Karpathy guidelines

Source: <https://github.com/multica-ai/andrej-karpathy-skills> (CLAUDE.md at commit 2c60614, MIT, by forrestchang), derived from <https://x.com/karpathy/status/2015883857489522876>. Text copied verbatim below; only the file's own "# CLAUDE.md" title line was dropped, and blank lines, link brackets and a code-fence language were added so it passes markdownlint.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

### How the Karpathy guidelines fit my rules

My own rules (C:\dev\CLAUDE.md, each repo's CLAUDE.md, memory) win where they are more specific. Read them together like this:

1. **"No features beyond what was asked":** in graded practicals, everything in the assignment statement or required by my own rules (the defence guide, a screenshot of every step, the AI-use section) counts as asked, including optional and extra-credit items. Anything else is proposed first, never added silently.
2. **"Loop independently":** the verify-and-fix loop starts only after I approve the plan of a large task, and it never includes commit, push or merge unless I ask.
3. **"Write a test that reproduces it":** use the repo's tests when they exist. When they don't (reports, documents), state the concrete check instead (open the PDF, start Odoo, take a screenshot) and propose adding tests.
4. **"Match existing style" / "Minimum code":** the assignment statement's required structure wins. Line-by-line explanations go in the chat, not in the code, so they don't count against simplicity.
