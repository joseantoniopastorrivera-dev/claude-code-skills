---
name: normalizar-nombres
description: Renombra documentos (PDF, Word, OpenDocument, PowerPoint, Excel…) y carpetas de uno o varios repos git a minúsculas con guiones, sin tildes, conservando el historial y actualizando las rutas citadas. Úsala cuando el usuario pida ordenar, limpiar o normalizar nombres de archivos o carpetas.
---

# Normalizar nombres de archivos y carpetas

Convierte `UT1.2 Gestión de Tablas.pdf` en `ut1-2-gestion-de-tablas.pdf` y `1ª Evaluación/` en `1a-evaluacion/`, en uno o varios repos git a la vez.

Script: `scripts/normalizar.py` de este plugin (`../../scripts/normalizar.py` desde esta carpeta). Solo usa la biblioteca estándar de Python. Ejecútalo con `python -I -X utf8`: `-X utf8` evita que la consola de Windows rompa al imprimir tildes.

## Regla de nombres

- Minúsculas; tildes fuera con NFKD (`ñ→n`, `á→a`, `ª→a`).
- Cualquier otro carácter (espacio, punto, `_`, `+`, `#`) pasa a `-`, sin guiones repetidos ni en los extremos.
- La extensión se conserva, en minúsculas. `C#` pasa a `csharp` para que no se pierda el significado.

## Lo que nunca se renombra

- Carpetas cuyo nombre exacto usa una herramienta, y todo lo que hay dentro: `src/`, `Assets/` (Unity), `.vscode/`, `.idea/`, `.github/`, `docs/` (MkDocs), `node_modules/`, `.venv/`, `.claude/`, `.claude-plugin/`…
- **Paquetes Java y Python.** En Java la carpeta tiene que llamarse exactamente como el `package`. Si se cambia, no compila, y en Windows el error ni siquiera aparece (no distingue mayúsculas): salta después en Linux o en CI. Corregir un paquete es otra tarea, porque implica cambiar código.
- Ficheros que no son documentos (código, imágenes…). Su nombre suele estar citado desde el código.

## Pasos

1. **Comprobar que cada repo está limpio** (`git status --porcelain` vacío). El script salta los que tienen cambios.
2. **Simular**: `python -I -X utf8 normalizar.py <raíz> --salida <scratchpad>/plan.md`. La raíz puede ser un repo o una carpeta con varios. Envía el plan al usuario y **espera su aprobación**.
3. **Resolver colisiones** antes de ejecutar: dos elementos que acaban con el mismo nombre (por ejemplo `UT2.3 Modelo.pdf` y `UT2.3-Modelo.pdf`). Compara los hashes: si son idénticos, pregunta si se borra uno; si no, propón un sufijo (`-v1` para el más antiguo). El script se salta el repo entero mientras haya una colisión.
4. **Ejecutar**: `--ejecutar --registro <scratchpad>/registro.json`. Usa `git mv` **en dos pasos** (`viejo → tmp → nuevo`): en Windows, un cambio solo de mayúsculas (`Tema.pdf → tema.pdf`) no se detecta en uno. Mueve primero los ficheros y después las carpetas, de la más profunda a la más superficial.
5. **Referencias**: `--referencias <registro>` cambia los nombres solo dentro de `código` en los `.md`, y solo si forman un segmento completo de ruta. Después busca a mano los nombres viejos en el resto de ficheros de texto y descarta los falsos positivos. Que "Gimnasio Hércules" contenga `Gimnasio` no es una ruta. Suelen quedar sin cambiar:
   - árboles de carpetas dentro de bloques de código;
   - `cd` y "abre la carpeta X" en LEEME y guías;
   - referencias que ya estaban mal antes del cambio. Corrígelas y díselo al usuario.
6. **Verificar**: `git status` solo debe mostrar `R` (renombrados) y `M` en los textos editados, nunca `D` + `??`. En el diff de cada texto solo deben cambiar las líneas de rutas, no el fichero entero (saltos de línea).
7. **Commit**: uno por repo. Un commit por archivo ensucia el historial, y separar "renombrar" de "arreglar referencias" deja un commit intermedio con enlaces rotos. Tipo `chore`, con el formato de commits del usuario. Push solo si lo pide.

## Problemas conocidos

- **`Permission denied` al renombrar una carpeta**: algún proceso la tiene como directorio de trabajo (la sesión de Claude, una pestaña del terminal, el IDE). Mueve la sesión a la carpeta padre o pide al usuario que cierre esa pestaña. Si el usuario prefiere dejarla, déjala.
- **Carpetas vacías**: git no las versiona, así que el script no las ve. Búscalas con `os.walk` y renómbralas con un `mv` normal, también en dos pasos.
- **Enlaces externos**: GitHub redirige cuando se renombra un repo, pero no cuando cambian las rutas de dentro. Avisa de que los enlaces directos a archivos que se hayan compartido dejan de funcionar.
- **Proyectos abiertos en el IDE**: tras el cambio hay que reabrirlos desde la ruta nueva. Los `.iml` de IntelliJ apuntan al nombre del fichero `.iml`, que no cambia.
