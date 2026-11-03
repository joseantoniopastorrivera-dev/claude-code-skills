# Decisiones técnicas y lecciones aprendidas

Problemas reales que aparecieron al trabajar con una biblioteca de unos 4.700 archivos, y cómo se resolvieron.

## 1. "Mismo nombre" no significa "mismo archivo"

Hay tres niveles de duplicado, y cada uno necesita una técnica distinta:

| Nivel | Ejemplo | Cómo se detecta |
|---|---|---|
| Copia exacta | Mismo archivo copiado en dos carpetas | SHA-256 del archivo completo |
| Mismo audio, otras etiquetas | "Alarico - Vowels" / "Alarico, Vault Records - Vowels" | **MD5 de audio en la cabecera del FLAC** |
| Misma canción, otro formato | FLAC y AAC del mismo tema | Nombre normalizado |

El formato FLAC guarda en su bloque `STREAMINFO` un MD5 del audio descomprimido. Leerlo es gratis (`mutagen` lo expone como `info.md5_signature`) y no depende de las etiquetas ni del nivel de compresión.

## 2. Calcular el hash solo cuando hace falta

Leer 150 GB completos lleva mucho tiempo. Pero dos archivos de distinto tamaño **no pueden ser idénticos**, así que primero se agrupa por tamaño y solo se calcula el hash de los grupos con más de un archivo. Es la misma técnica que usa `fdupes`. En la biblioteca real hizo falta calcularlo de 1.071 archivos de 4.754.

## 3. Union-Find para agrupar por varias pistas a la vez

Si A se llama igual que B, y B tiene el mismo audio que C, entonces A, B y C son la misma canción, aunque A y C no compartan nada directamente. Union-Find (conjuntos disjuntos, con compresión de camino) resuelve esta transitividad en tiempo casi lineal. Comparar todos los pares serían unos 22 millones de comparaciones.

## 4. Descargas "a medias" que parecen enteras

Un FLAC descargado al 5 % conserva la cabecera, que sigue diciendo "dura 6 minutos". Para detectarlo se calculan los **kbps reales** (`tamaño × 8 / duración`): un FLAC de verdad nunca baja de ~250 kbps.

## 5. Las etiquetas pierden el nombre del remix

En muchos archivos el título de la etiqueta era solo "Ipanema", mientras que el nombre de archivo decía "Ipanema (Flug Rework)". Si se renombra a partir de las etiquetas, 9 reworks distintos acaban con el mismo nombre. Por eso **el nombre nuevo se construye a partir del nombre de archivo**, y la etiqueta solo se usa para resolver ambigüedades.

## 6. Artistas con caracteres que Windows prohíbe

El artista "OFF / GRID" no puede escribirse tal cual en un nombre de archivo de Windows, así que en las descargas aparecía como `OFF - GRID`, `OFF  GRID` y `OFF- GRID`. La etiqueta (`OFF / GRID`) indica dónde termina realmente el artista: se prueban todos los puntos de corte y se elige el que coincide comparando solo letras y números.

## 7. Un "remix" que no era un remix

Dos archivos, "Stuck in A Dream" y "Stuck In A Dream (Antigone Remix)", tenían **exactamente el mismo MD5 de audio**. La tienda había servido la versión original dos veces con distinto nombre. Sin el MD5 del FLAC no se habría detectado.

## 8. Unicode: no todas las letras raras son "letra + tilde"

La normalización NFKD separa "å" en "a" + "°", pero **"ø" es una letra propia** y no se descompone, así que "Rødhåd" no coincidía con "Rodhad". Lo descubrieron los tests. Se corrigió con una tabla de traducción (`ø→o`, `æ→ae`, `ß→ss`…).

## 9. Operaciones masivas seguras

- **Simulación por defecto (dry-run)**: el modo que no toca nada es el que se ejecuta si no se indica otra cosa.
- **Nunca se borra**: lo que sobra va a `_Cuarentena/` y lo elimina el usuario cuando ha comprobado que todo está bien.
- **Registro tipo journal**: cada movimiento se escribe y se vuelca a disco (`flush`) en el momento, así que si el proceso se corta, `--deshacer` sabe exactamente qué revertir.
- **`os.rename` en el mismo disco** es instantáneo, porque solo cambia la entrada en el sistema de archivos y no copia datos.
- **Windows no distingue mayúsculas**: las colisiones de nombre se comprueban en minúsculas.

## 10. Playlists portables

Las `.m3u8` usan rutas relativas (`../Biblioteca/...`), así que siguen funcionando aunque la unidad cambie de letra.
