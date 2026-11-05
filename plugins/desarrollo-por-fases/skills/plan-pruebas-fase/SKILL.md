---
name: plan-pruebas-fase
description: Genera el plan de pruebas imprimible (Markdown y PDF) de una fase de la hoja de ruta para probarla con una persona usuaria real. Úsala cuando el usuario pida "plan de pruebas de la fase N", "PDF de pruebas" o al terminar una fase.
---

# Plan de pruebas de una fase

Resultado: `docs/plan-pruebas-faseN.md` y `docs/plan-pruebas-faseN.pdf`, con un commit cada uno.

## 0. Datos del proyecto

Lee la sección **"Skills de fases"** del `CLAUDE.md` del proyecto: hoja de ruta, rama de la fase, comando de tests, **plantilla del plan de pruebas**, **persona que prueba**, autor del PDF y reglas propias (por ejemplo, qué no puede pedir ni esperar ningún caso). Si el proyecto no indica plantilla, usa `plantilla.md` de esta carpeta.

## 1. Reunir qué se prueba

- La hoja de ruta: los puntos de la fase N (eso es el objetivo, apartado 1).
- `git log --oneline main..<rama de la fase N>`: cada commit `feat` tiene al menos un caso de prueba; los `fix`, un caso que demuestre que no vuelve a pasar.
- El comando de tests: el número de tests para la preparación.
- Si el proyecto versiona su esquema de datos, la versión esperada se lee **del código**, nunca de los datos reales.

## 2. Escribir el Markdown

Copia la plantilla y rellena cada `{…}`. Borra las líneas de instrucciones entre llaves.

Reglas de los casos:
- **Acción literal**: el texto exacto que escribe, dice o pulsa la persona que prueba, entre comillas o `código`. Nunca "probar el registro".
- **Resultado observable**: qué se ve en pantalla o en el log, con los números concretos.
- Cubrir por cada función nueva: el caso normal, una entrada vacía o absurda, el error del usuario (doble toque, cancelar) y la persistencia tras un reinicio.
- Los datos absurdos o de prueba, solo en la ronda 1 (datos de prueba). En la ronda 2, solo comprobaciones que no ensucien los datos reales.
- Aplica las reglas propias del proyecto que indique el `CLAUDE.md`.
- Numeración P01, P02… continua hasta el final; el total va en el apartado de resultado.

## 3. Generar el PDF y revisarlo

Con la skill `make-pdf` de gstack, si está instalada:

```bash
P="$HOME/.claude/skills/gstack/make-pdf/dist/pdf"
"$P" generate --page-size a4 --margins 0.75in --no-confidential --no-chapter-breaks \
  --author "<autor del CLAUDE.md>" docs/plan-pruebas-faseN.md docs/plan-pruebas-faseN.pdf
```

Si no está, pregunta al usuario con qué herramienta generar el PDF antes de instalar nada.

Para revisarlo **no abras el PDF en el navegador integrado** (lanza un diálogo de descarga). Genera la misma vista con `--to html` en el scratchpad, sírvela con `python -m http.server` en 127.0.0.1 y haz capturas: cabecera, una tabla de casos y el final. Corrige el `.md` y regenera hasta que se vea bien.

## 4. Cerrar

- Commit del `.md` y luego del `.pdf`, en el formato de commits del `CLAUDE.md`.
- Entrega el PDF al usuario y recuérdale la preparación del apartado 3 del plan.
