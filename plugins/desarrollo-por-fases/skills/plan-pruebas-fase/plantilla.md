# Plan de pruebas de {PROYECTO} (fase {N})

| | |
|---|---|
| **Proyecto** | {Nombre del proyecto} |
| **Versión que se prueba** | rama `{RAMA}` |
| **Persona que prueba** | {Nombre o perfil} |
| **Responsable** | {Autor} |
| **Fecha** | ____ / ____ / {AÑO} |
| **Lugar** | ______________________________ |
| **Hora de inicio / fin** | ________ / ________ |

---

## 1. Objetivo

{Qué promete esta fase según la hoja de ruta, en 3-6 viñetas verificables.}

---

## 2. Entorno de la prueba

{Dónde se ejecuta la aplicación durante la prueba, qué necesita (red, servicios, datos) y qué opciones hay. Si hay datos personales, explica cómo se mueven y dónde no deben ir nunca (GitHub, correo, nube).}

---

## 3. Preparación (antes de la sesión)

| ✔ | Tarea | Cómo se comprueba |
|---|---|---|
| ☐ | Estar en la rama correcta | `git switch {RAMA}` |
| ☐ | Dependencias instaladas | {Comando de instalación} |
| ☐ | Tests en verde | {Comando de tests} → `{TESTS} passed` |
| ☐ | Copia de seguridad de los datos reales | {Dónde debe existir la copia} |
| ☐ | Configuración completa | {Variables o ficheros obligatorios de esta fase} |
| ☐ | Equipo enchufado y sin suspensión | |
| ☐ | Plan impreso y bolígrafo | |
{Filas extra de preparación propias de la fase.}

---

## 4. Ronda 1: pruebas funcionales con datos de prueba

{Cómo se apunta la aplicación a los datos de prueba y qué debe verse al arrancar.} La persona que prueba hace las acciones y el responsable anota el resultado. Cronometra las marcadas con ⏱.

{Una subsección ### 4.x por cada grupo de funciones. Tabla:}

| ID | Acción | Resultado esperado | OK / Fallo | Notas |
|---|---|---|---|---|
| P01 | {Acción concreta, con el texto literal entre `comillas`} | {Qué debe verse exactamente} | ☐ / ☐ | |

---

## 5. Ronda 2: paso a los datos reales

1. Para la aplicación.
2. {Cómo se vuelve a apuntar a los datos reales.}
3. Comprueba que existe la copia de seguridad.
4. Arranca la aplicación.

| ID | Comprobación | Resultado esperado | OK / Fallo | Notas |
|---|---|---|---|---|
| P{n} | Arranque | {Qué debe verse}, sin errores | ☐ / ☐ | |
| P{n+1} | Los datos anteriores siguen ahí | {Cómo se comprueba} | ☐ / ☐ | |
{Una o dos comprobaciones de las funciones nuevas sobre los datos reales.}

> Si falla el arranque: para la aplicación, restaura la copia de seguridad y apunta el error (sin datos personales).

---

## 6. Si algo falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| {Síntoma} | {Causa} | {Acción} |
{Síntomas propios de las funciones nuevas.}

---

## 7. Preguntas a la persona que prueba (5 minutos al final)

Valora del 1 (nada) al 5 (mucho):

| Pregunta | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
{3-5 preguntas sobre las funciones nuevas de la fase, más: "¿Lo usarías todos los días?"}

¿Qué echas en falta? ______________________________________________________________

¿Qué te sobra o te molesta? __________________________________________________________

---

## 8. Resultado

| Métrica | Objetivo | Medido |
|---|---|---|
| Pruebas superadas | {TOTAL} / {TOTAL} | ____ / {TOTAL} |
{Métricas propias de la fase.}

**Decisión:** ☐ Fusionar `{RAMA}` en `main` ☐ Corregir fallos y repetir

### Incidencias

| Nº | Prueba | Qué pasó | Gravedad (alta / media / baja) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
