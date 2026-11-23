---
title: finalize-skill
subtitle: Skill de Claude Code que cierra el desarrollo de una skill · versión 0.1.0
author: José Antonio Pastor Rivera
date: 23 de noviembre de 2026
---

# Idea 💡

Al terminar las primeras skills se vio que cada una se daba por acabada de una forma distinta: unas tenían README completo y otras no, ninguna tenía un informe del trabajo hecho y nadie había comprobado si funcionaban en Linux. `finalize-skill` es la lista de comprobación que se pasa **siempre** antes de dar una skill por terminada, tanto en el repositorio público `claude-code-skills` como en el privado.

Lo que hace, en cinco pasos que el autor aprueba uno a uno:

1. revisión en Linux;
2. comprobaciones (tests, cabecera del `SKILL.md`, ausencia de datos personales y empaquetado);
3. informe final en PDF, DOCX y ODT, más un PDF en inglés;
4. README completo con lo que finalmente se hizo;
5. propuestas de mejora para la siguiente versión.

> **Qué no es:** no hace commits ni publica nada. Subir los cambios o publicar los informes lo decide siempre el autor.

# Diseño 🧩

## Flujo

```
   skill terminada
        |
        v
   1. Revisión Linux --> pendientes.md si hay
        |                que probar en la VM
        v
   2. Comprobaciones: tests, cabecera,
      datos personales, zip
        |
        v
   3. Índice propuesto --> aprobación
        |
        v
      Informe .md --> styled-docs --> PDF, DOCX,
        |                             ODT y PDF en inglés
        v
      docs/informes/ (último)
      docs/informes/historicos/ (cada versión)
        |
        v
   4. README completo, con enlace al informe
        |
        v
   5. Propuestas de mejora --> decide el autor
```

## Decisiones

| Decisión | Motivo |
|---|---|
| Skill del repositorio (`.claude/skills/`), no plugin | Es una norma de trabajo del propio repositorio, no algo que se vaya a vender |
| Aprobación del autor en cada paso | Un informe con el índice equivocado obliga a rehacerlo entero |
| Índice común para todas las skills, con el emoji detrás del título | Los informes se pueden comparar entre sí y el emoji se ve igual en el índice |
| Una sola tabla de incidencias (I-01…) | Las demás secciones la citan; dos tablas acababan contando lo mismo |
| Último informe en `docs/informes/` y cada versión en `historicos/` | Seguimiento completo de la evolución de cada skill sin perder versiones |
| Versionado semántico | Parche si solo se arregla o documenta, menor si la skill hace algo nuevo |

# Implementación 🛠️

| Fichero | Contenido |
|---|---|
| `SKILL.md` | Los cinco pasos, la estructura del informe, las versiones, los commits y lo que no se hace aquí |
| `scripts/aoo_convert.py` | Conversión de DOCX a ODT y PDF con Apache OpenOffice 4 por UNO |

`aoo_convert.py` se ejecuta con el Python de OpenOffice (2.7). Arranca OpenOffice sin ventana, abre el DOCX, devuelve a los marcadores su nombre real (OpenOffice los renombra a `Bookmark`, `Bookmark1`… al importarlos) y guarda el ODT y el PDF. Sin ese paso, los enlaces del índice no llevarían a ninguna parte.

La forma preferida de generar el informe es la skill `styled-docs` (repositorio privado), que reúne la creación del DOCX, la conversión y la comprobación de enlaces del PDF. Los pasos a mano siguen documentados en el `SKILL.md` por si `styled-docs` no está disponible.

# Pruebas ✅

- **Uso real.** La lista se aplicó al cerrar `styled-docs`, `explain-repo` y la skill de preparación de exámenes. Sus tres informes se generaron siguiendo el paso 3 y se comprobaron con 0 enlaces rotos.
- **Este informe** se ha generado con `styled-docs` siguiendo la propia skill, igual que los informes de los demás plugins cerrados el mismo día.
- La skill no tiene código propio aparte de `aoo_convert.py`, que se probó convirtiendo los informes anteriores.

# Incidencias 🐞

| N.º | Incidencia | Causa | Arreglo | Estado |
|---|---|---|---|---|
| I-01 | El índice del PDF no llevaba a ninguna parte | OpenOffice renombra los marcadores del DOCX a `Bookmark`, `Bookmark1`… | `aoo_convert.py` les devuelve el nombre real | Resuelta |
| I-02 | La conversión se quedaba colgada | `soffice --convert-to` es de LibreOffice; Apache OpenOffice abre una ventana y espera | Conversión por UNO con OpenOffice sin ventana | Resuelta |
| I-03 | Títulos impresos como «2. 2. Diseño» | OpenOffice numera el estilo `Heading 1` en su esquema | Estilo de párrafo propio para los títulos | Resuelta |
| I-04 | `python -I` no encontraba python-docx ni Pillow | Están en el site-packages del usuario | Ejecutar con `python` normal | Resuelta |
| I-05 | Cada informe tenía apartados distintos | La primera versión copiaba la estructura de las prácticas de SGE sin fijarla | Índice común de 12 apartados | Resuelta |
| I-06 | Los informes de cada versión se sobrescribían | Solo existía `docs/informes/` | Carpeta `historicos/` con la versión en el nombre | Resuelta |
| I-07 | Rutas de Windows fijas en `aoo_convert.py` | El script se escribió solo para el portátil | `styled-docs` ya lo resolvió en su copia; aquí sigue pendiente | No resuelta |

# Ajustes tras las pruebas ✏️

| Antes | Después |
|---|---|
| `cerrar-skill`, en español | `finalize-skill`, en inglés como el resto de skills nuevas |
| Estructura de las prácticas de SGE con índice de incidencias aparte (I-05) | Índice común de 12 apartados con una sola tabla de incidencias |
| Apartado final «Preguntas de Claude» solo en el chat | Apartado 🚀 dentro del informe y también en el chat |
| Informe generado a mano con python-docx y OpenOffice | `styled-docs` como vía preferida, con los pasos a mano de respaldo |
| Un informe por skill, que se sobrescribía (I-06) | Último informe más histórico por versión |
| Sin norma de versiones | Parche o versión menor en cada cierre |
| Sin norma de commits | Un commit por cambio, con su push |

# Integración con otras skills 🔗

| Skill | Relación | Por qué |
|---|---|---|
| `styled-docs` | Genera el informe | Índice con enlaces comprobados, notas de ida y vuelta, DOCX y ODT |
| `normalize-names` (`organize-files`) | Fija el nombre de los ficheros del informe y del histórico | Mismo criterio en todos los repositorios: minúsculas, guiones y versión `v0-1-0` |
| `write-skill` (gstack) | Se usa antes, al escribir la skill | `finalize-skill` comprueba el resultado, no cómo se escribió |
| Todas las skills de los dos repositorios | Pasan por aquí antes de darse por terminadas | Es la norma de cierre del `CLAUDE.md` |

# Revisión Linux 🐧

- **¿Tiene sentido en Linux?** Sí: la lista de comprobación no depende del sistema.
- **Qué cambia:** `python3` en lugar de `python`, y la ruta de OpenOffice (`/opt/openoffice4/program`). `aoo_convert.py` tiene las rutas de Windows fijas (I-07).
- **¿Lo contempla ya el código?** En la vía preferida sí, porque `styled-docs` busca OpenOffice en los dos sistemas. En la vía a mano, no.
- **Pendiente:** probar la vía a mano en la máquina virtual Linux del USB.

# Lecciones aprendidas 🎓

**Fijar la estructura antes del segundo informe.** El primer informe copió la estructura de las prácticas de SGE y el segundo la adaptó a su manera. Con dos informes distintos ya no se podían comparar. Desde entonces el índice es común y solo se quita un apartado si de verdad no tiene nada.

**Guardar cada versión desde el principio.** Los primeros informes se sobrescribían al cerrar una versión nueva, y la versión anterior solo quedaba en el historial de git. Con `historicos/` la evolución de cada skill se ve abriendo una carpeta.

**Un cambio, un commit.** Mezclar la skill, su informe y una norma del `CLAUDE.md` en un solo commit hacía difícil encontrar o deshacer uno de ellos. Ahora cada cambio va por separado, con su push.

**Reutilizar la herramienta que ya existe.** El paso a mano de python-docx y OpenOffice funcionaba, pero cada informe repetía los mismos arreglos. Al aparecer `styled-docs`, la skill pasó a usarlo y dejó los pasos a mano solo como respaldo.

# Uso de IA 🤖

La skill se ha elaborado con **Claude Code**, la herramienta de desarrollo asistido de Anthropic, con el modelo Claude Opus 5.5, bajo la dirección y revisión del autor en cada paso.

| Herramienta | Uso |
|---|---|
| Claude Code | Redacción de la skill, de `aoo_convert.py` y de este informe |
| `styled-docs` | Generación de este informe en PDF, DOCX y ODT |
| Apache OpenOffice 4 | Conversión a ODT y PDF |

## Encargos principales

1. **Encargo inicial.** Definir un proceso de cierre obligatorio para todas las skills: revisión en Linux, informe en varios formatos con la estructura de las prácticas del autor y README completo.
2. **Nombre en inglés.** Renombrar la skill a `finalize-skill` y redactarla en inglés, como el resto de skills nuevas.
3. **Índice común.** Unificar el índice de todos los informes, con su emoji detrás del título y las propuestas de mejora dentro del informe, y añadir una norma de versiones.
4. **Histórico.** Conservar el último informe en `docs/informes/` y una copia renombrada de cada versión en `docs/informes/historicos/`, y aplicarlo a todas las skills.
5. **Commits.** Hacer un commit por cada cambio, con su push, para que el historial quede ordenado.

# Propuestas de mejora 🚀

Propuestas para la siguiente versión. El autor decide cuáles se aceptan.

1. **Script de archivo.** Un script `archive_report.py <skill> <versión>` que copie los ficheros del informe a `historicos/` con el nombre correcto y se niegue a sobrescribir una versión ya archivada. Hoy se hace a mano.
2. **Quitar la copia de `aoo_convert.py`.** Usar siempre el de `styled-docs`, que ya funciona en Linux (I-07), en lugar de mantener dos copias.
3. **Comprobación automática del índice.** Un script que verifique que el `.md` del informe tiene los 12 apartados en orden, con su emoji, antes de generarlo.
4. **Versión en `plugin.json`.** Comprobar que la versión de la portada coincide con la de `plugin.json` y con el nombre del histórico.

# Referencias 📚

- `CLAUDE.md` del repositorio `claude-code-skills`: norma de cierre de skills.
- `styled-docs` (repositorio privado): generación de documentos con índice comprobado.
- `normalize-names` (plugin `organize-files`, repositorio privado): normas de nombres.
- Apache OpenOffice 4, API UNO: conversión de documentos.
