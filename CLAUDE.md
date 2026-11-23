# claude-code-skills (marketplace de plugins con mis skills de Claude Code)

## Cómo trabajar conmigo
Reglas comunes a todos mis repos (copia de mi `C:\dev\CLAUDE.md`, para que también las lean las sesiones en la nube). Soy estudiante de DAM en el IES Isidra de Guzmán.
- En prácticas evaluables, resuélvelas completas (sin modo de pistas). Al terminar, crea junto a la entrega (en `docs/` si existe) un `guia-defensa-<practica>.md` para defenderla en clase, al estilo de la guía de DataStock. Las guías de defensa no se suben nunca a GitHub: cada repo tiene `guia-defensa-*.md` en su `.gitignore` (añádelo si falta).
- Estructura de la guía de defensa: cómo usarla; cómo arrancar, ejecutar y ensayar sin estropear la entrega; qué pide el enunciado y dónde se cumple cada requisito; visión general (capas, flujo, decisiones de diseño a justificar); y por cada requisito: qué pide, dónde está, explicación línea a línea, cómo demostrarlo, errores típicos, preguntas de la profesora con su respuesta y 🔧 modificaciones en directo (el cambio que podrían pedir, con el código exacto y dónde va). Al final: casos prácticos «¿qué pasaría si…?», «corrige este error» (síntoma → causa → arreglo) y chuleta con plan de ensayo.
- Si la tarea es grande, antes de tocar nada dime cómo lo harías (plan por pasos) y espera a que lo apruebe o lo corrija.
- Cuando escribas código, explícalo línea por línea y di por qué elegiste esa forma y no otra.
- Si ves un error de concepto o algo que no entiendo bien, dímelo aunque no te lo pregunte.
- Responde en español.
- No hagas commit ni push sin que te lo pida. Commits sin `Co-Authored-By` ni líneas de atribución.
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
