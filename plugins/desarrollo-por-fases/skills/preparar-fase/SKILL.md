---
name: preparar-fase
description: Arranca una fase de la hoja de ruta de un proyecto (fase 0 de preparación más el plan por pasos). Úsala cuando el usuario diga "preparar la fase N", "empezar la fase N" o "siguiente fase".
---

# Preparar una fase

Hay dos etapas y una parada obligatoria entre ellas: no se escribe código de la fase hasta que el usuario apruebe el plan.

## 0. Datos del proyecto

Lee la sección **"Skills de fases"** del `CLAUDE.md` del proyecto. De ahí salen los valores de esta skill; si falta alguno, usa el valor por defecto:

| Dato | Por defecto |
|---|---|
| Hoja de ruta | `docs/hoja-de-ruta.md` |
| Registro de decisiones | `docs/decisiones.md` |
| Rama de cada fase | `faseN` |
| Copia de seguridad antes de empezar | ninguna |
| Instalar dependencias | ninguno |
| Ejecutar los tests | ninguno (avísalo: sin tests no hay línea base) |
| Capas o módulos del proyecto | ninguno |
| Comprobaciones extra del plan | ninguna |

Si el proyecto no tiene esa sección, propón añadirla con los valores que deduzcas del repositorio, y espera a que el usuario los confirme.

## 1. Fase 0: preparación (sin pedir permiso)

1. Lee la hoja de ruta (qué entra en la fase N) y el registro de decisiones (qué ya está decidido).
2. Comprueba que la fase anterior está fusionada en `main`. Si no lo está, para y díselo.
3. `git switch main` y después `git switch -c <rama de la fase N>`.
4. Si el proyecto define una copia de seguridad, hazla **sin abrir ni leer los datos**: solo copiar el fichero. Si el origen no existe, sigue y avísalo.
5. Instala las dependencias. Las nuevas se fijan en el fichero de dependencias del proyecto.
6. Línea base: los tests tienen que pasar antes de tocar nada. Apunta cuántos son.
7. En la hoja de ruta, marca la fase como 🟡 y haz commit.

## 2. Plan por pasos (y parar)

Presenta al usuario, sin escribir código:
- Los pasos en orden, cada uno con los ficheros que toca y su test.
- Si el proyecto define capas, qué capa cambia en cada paso. Respeta las reglas de capas del `CLAUDE.md`.
- Cualquier cambio de esquema de datos, como migración **nueva**. Nunca se edita una migración ya aplicada.
- Cada **comprobación extra** que pida el proyecto (por ejemplo, límites legales del producto). Si una función no la supera, sácala de la fase y explica por qué.
- Las decisiones que tiene que tomar el usuario, con tu recomendación.

Para y espera su aprobación o sus correcciones.

## 3. Durante la fase

- Un commit por cambio pequeño, en el formato de commits del `CLAUDE.md`, y solo si los tests devuelven 0. Comprueba el código de salida: un `| tail` lo oculta.
- Cada decisión con alternativas va al registro de decisiones (Dn, con su motivo).
- Al terminar: marca los puntos con ✅ en la hoja de ruta y ofrece la skill `plan-pruebas-fase`.
