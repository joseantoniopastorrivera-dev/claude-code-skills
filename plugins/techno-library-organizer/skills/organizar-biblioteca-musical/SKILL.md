---
name: organizar-biblioteca-musical
description: Usar al limpiar o reorganizar una biblioteca de música de DJ: duplicados, descargas rotas, carpetas-lista a playlists, renombrado Título - Artista.
---

# Organizar una biblioteca musical de DJ

Procedimiento para quitar duplicados, detectar descargas rotas y pasar de "una carpeta por lista" a **una biblioteca única + playlists**, sin perder en qué listas estuvo cada canción.

Scripts de referencia: la carpeta `src/` de este plugin (`../../src/` desde esta carpeta: `inventario.py`, `duplicados.py`, `organizar.py`). Requieren `pip install mutagen`.

## Reglas que no se saltan

1. **Primero solo lectura.** Inventario y análisis antes de tocar nada.
2. **Plan por pasos y esperar aprobación** antes de mover archivos.
3. **Simular por defecto** (dry-run); mover solo con `--ejecutar`.
4. **Nunca borrar.** Sobrantes y rotos van a `_Cuarentena/`; el usuario la borra cuando ha comprobado todo.
5. **Registro de cada movimiento** (journal con `flush`) para poder `--deshacer`.
6. **No mover si la carpeta la usa un software de DJ** (Rekordbox, Serato, Traktor guardan rutas) sin preguntar antes. Preguntar qué software y equipo usa (p. ej. Engine DJ + USB).
7. **Explicar cada paso y el código línea a línea**, y el porqué de cada elección.

## Fase 0 — Reconocimiento

- Listar las carpetas de primer nivel. Los listados remotos suelen cortarse (p. ej. 2000 entradas): listar por carpeta si se trunca.
- Atención a **listas dentro de subcarpetas** (`X\Playlist\Y`): la "lista" es la carpeta que contiene el archivo, no la de primer nivel.
- Estimar duplicados por nombre normalizado solo como orientación; nunca para borrar.
- Preguntar: software de DJ, biblioteca única + playlists o mantener carpetas, si tiene Python, si quiere huella acústica (lenta; solo para dudosos).

## Fase 1 — Inventario (en el PC del usuario)

El hash de cientos de GB se calcula en local, no a distancia. `python inventario.py "<raíz>"` produce `_herramientas/salida/inventario.csv` con: lista, ruta, tamaño, fecha, códec, bitrate, **kbps_real**, duración, etiquetas, **md5_audio_flac**, sha256, estado.

- Estado `ROTO`: error de lectura, < 100 KB o < 30 s.
- Estado `TRUNCADO`: sin pérdida con kbps_real (`tamaño·8/duración`) < 250. Una descarga a medias conserva la cabecera con la duración completa.
- SHA-256 **solo de archivos que comparten tamaño** (distinto tamaño ⇒ no idénticos).
- Ignorar carpetas que empiezan por `_`.
- Si se repite el inventario, **renombrar antes el CSV anterior** (no sobrescribir originales).

## Fase 2 — Duplicados

`python duplicados.py "<raíz>/_herramientas/salida/inventario.csv"` → `canciones.csv`, `archivos.csv`, `para_redescargar.csv`.

- Agrupar con **Union-Find** por tres pistas: nombre normalizado, SHA-256 y **MD5 de audio del FLAC** (STREAMINFO; detecta mismo audio con distintas etiquetas).
- Normalizar nombre: quitar extensión, nº de pista, "(Original Mix)", tildes (NFKD) **y letras que NFKD no separa** (ø→o, æ→ae, ß→ss…).
- Mejor copia: sin pérdida (FLAC/WAV/ALAC) > kbps_real > tiene etiquetas > tamaño.
- Historial: listas de cada canción ordenadas por fecha (avisar de que la fecha puede ser la de una copia, no la de la lista).
- Revisar los **dudosos**: mismo audio con nombres distintos puede ser un error de la tienda (p. ej. un "remix" que es la versión original).

## Fase 3 — Organizar

`python organizar.py "<raíz>"` (simula) → revisar `plan_organizacion.csv` → `--ejecutar` → si algo falla, `--deshacer`.

Resultado:
```
Biblioteca/<Artista>/<Título> - <Artista>.ext
Listas/<lista>.m3u8                (orden original; huecos como "# FALTA")
Listas/_Pendiente FLAC.m3u8        (solo en AAC/MP3)
Listas/_Pendiente redescargar.txt
_Cuarentena/<ruta original>
```

- **Formato de nombre:** `Título - Artista.ext`.
- **Nunca borrar lo que solo existe en baja calidad (m4a/AAC/MP3):** va a la biblioteca y a `_Pendiente FLAC`. Solo va a cuarentena el m4a si existe el FLAC de la misma canción.
- Comprobar el códec real: `.m4a` puede ser AAC (con pérdida) o ALAC (sin pérdida).
- Construir el nombre **desde el nombre de archivo**, no desde las etiquetas (las etiquetas suelen perder el nombre del remix y crearían colisiones).
- Usar la etiqueta solo para desambiguar artistas con " - " (p. ej. "OFF / GRID" llega como `OFF - GRID`).
- Formato Bandcamp `Artista - Álbum - NN Título` → `Título`. Caras de vinilo `A1.` exigen punto ("A4" puede ser artista).
- Quitar `< > : " / \ | ? *`; comparar colisiones en minúsculas (Windows no distingue); sufijo ` (2)` si chocan.
- `os.rename` en el mismo disco (instantáneo); comprobar que el destino no existe; bloquear una segunda ejecución.
- Playlists con rutas relativas (`..\Biblioteca\...`).
- Engine DJ puede no importar `.m3u8`: comprobar versión y ofrecer otro formato si hace falta.

## Fase 4 — Verificación antes de borrar la cuarentena

1. Renombrar `inventario.csv` → `inventario_original.csv` y repetir el inventario: debe dar `Total = canciones únicas | Rotos: 0 | Truncados: 0`.
2. Comprobar que cada entrada de las playlists existe.
3. Escucha dirigida (saltando al último minuto): una canción con muchas copias, un rework entre varios, un artista con " - ", un dudoso, una solo-m4a, un WAV y temas de la carpeta con más rotos.
4. Probar una playlist en el reproductor y en el software de DJ.
5. Avisar: en discos externos Windows suele borrar sin Papelera y `--deshacer` deja de funcionar. No borrar `_herramientas` (historial).
6. Carpetas vacías: borrar solo las vacías, de la más profunda a la más superficial, simulando primero (PowerShell `Remove-Item -WhatIf`).

## Si se publica el trabajo (GitHub)

- Nunca subir audio ni datos reales (CSV, playlists, nombres de carpetas con nombres de personas). Cifras solo agregadas.
- `.gitignore` que bloquee audio, `*.csv`, `*.m3u8`, `_herramientas/`, `Biblioteca/`, `Listas/`, `_Cuarentena/`.
- Datos de ejemplo sintéticos (tonos WAV con `wave`, artistas inventados) y tests con pytest.
- Correo noreply de GitHub en los commits; respetar las instrucciones del usuario sobre líneas de atribución en los commits.
