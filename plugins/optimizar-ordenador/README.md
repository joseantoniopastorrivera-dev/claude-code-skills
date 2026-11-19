# 🧹 optimizar-ordenador

> 🚧 **En construcción.** Este plugin todavía no se puede instalar. Este README explica lo que será.

Plugin para Claude Code que ayuda a **recuperar espacio y mantener ordenado un ordenador**, con una forma de trabajar muy concreta: **primero mira, luego enseña cifras, después propone, y solo actúa con tu permiso y con red de seguridad.**

---

## 📑 Índice

1. [🎯 Por qué existe](#-por-qué-existe)
2. [🛟 Cómo trabaja (siempre igual)](#-cómo-trabaja-siempre-igual)
3. [🧰 Las seis skills](#-las-seis-skills)
4. [📊 Ejemplo de informe](#-ejemplo-de-informe)
5. [🚫 Lo que nunca hará](#-lo-que-nunca-hará)
6. [💻 Plataformas](#-plataformas)
7. [📦 Ediciones](#-ediciones)
8. [🗺️ Hoja de ruta](#️-hoja-de-ruta)
9. [❓ Preguntas frecuentes](#-preguntas-frecuentes)

---

## 🎯 Por qué existe

Un día el disco del sistema se queda con **67 MB libres** y no hay forma de saber qué lo ha llenado. Las herramientas de siempre te enseñan carpetas enormes, pero no te dicen:

- 🤔 **qué es** cada cosa;
- ⚠️ si **se puede tocar** sin romper nada;
- 📦 si es mejor **moverla** que borrarla;
- 🔁 cómo evitar que **vuelva a pasar**.

Este plugin traduce todo eso a un plan claro.

---

## 🛟 Cómo trabaja (siempre igual)

```
  ① 👀 Solo lectura          ② 📊 Informe con cifras
  ┌──────────────────┐       ┌──────────────────────┐
  │ analiza sin tocar│ ───▶  │ qué ocupa, qué es,   │
  │ nada             │       │ si se puede tocar    │
  └──────────────────┘       └──────────┬───────────┘
                                        │
  ④ 🛟 Actúa con red          ③ ✅ Plan por bloques
  ┌──────────────────┐       ┌──────────▼───────────┐
  │ Papelera o       │ ◀───  │ tú apruebas cada     │
  │ cuarentena + log │       │ bloque, uno a uno    │
  │ para deshacer ↩️  │       └──────────────────────┘
  └──────────────────┘
```

---

## 🧰 Las seis skills

| | Skill | Qué hace |
|---|---|---|
| 📊 | `analizar-espacio` | Los archivos y carpetas que más ocupan, explicando qué es cada cosa. Distingue el tamaño **aparente** del **real** en disco. |
| 👯 | `buscar-duplicados` | Encuentra copias exactas comparando el contenido (hash) y propone cuál conservar. |
| 🏷️ | `sugerir-nombres` | Detecta nombres confusos (`documento (1).pdf`, `final_v2_DEFINITIVO`) y propone uno nuevo a partir del contenido. |
| 🗜️ | `sugerir-formatos` | Propone formatos que ocupan menos (WAV → FLAC, BMP → PNG…) y avisa de cuáles pierden calidad. |
| 🗓️ | `limpieza-periodica` | Prepara una limpieza programada de temporales y cachés que se ejecuta **sin Claude** (no gasta tokens). |
| 📦 | `revisar-programas` | Lista los programas con su tamaño y su último uso, los desinstala con su desinstalador oficial y busca restos. |

```
                    ┌──────────────────────┐
                    │  📊 analizar-espacio  │  ◀── se empieza por aquí
                    └──────────┬───────────┘
        ┌──────────────┬───────┴──────┬──────────────┐
        ▼              ▼              ▼              ▼
  👯 duplicados   🏷️ nombres     🗜️ formatos    📦 programas
        └──────────────┴───────┬──────┴──────────────┘
                               ▼
                    🗓️ limpieza-periodica
                     (para que no vuelva)
```

---

## 📊 Ejemplo de informe

```
  Disco C:  ██████████████████████████████████████░  99,9 % lleno

  Top carpetas                        Tamaño   ¿Se puede tocar?
  ─────────────────────────────────── ──────── ──────────────────
  📁 dev\…\node_modules (x14)         18,2 GB  ✅ se regenera
  🎮 userdata.img                     512 GB*  ⚠️ *aparente: 4 GB reales
  🗂️  Descargas (sin tocar en 1 año)   9,7 GB  🤔 revisar
  💤 hiberfil.sys                      6,4 GB  ⚙️ ajuste de Windows

  Propuesta: mover dev\ a otro disco con una unión → +31 GB
```

*(Cifras de ejemplo.)*

---

## 🚫 Lo que nunca hará

- ❌ Borrar directamente: siempre Papelera o cuarentena, con un registro para deshacer.
- ❌ Tocar ficheros del sistema, credenciales, `.env` ni tokens.
- ❌ "Limpiar el registro" de Windows: arriesga mucho a cambio de casi nada.
- ❌ Bajar la calidad de fotos, audio o vídeo en bloque sin una prueba previa que tú veas.
- ❌ Mover una carpeta sin comprobar antes que ningún programa depende de esa ruta.

---

## 💻 Plataformas

- 🪟 **Windows**: primero.
- 🐧 **Linux** y 🍎 **macOS**: en estudio (cambian las rutas, las cachés y el programador de tareas).

---

## 📦 Ediciones

```
  ┌──────────────────────── Pro ─────────────────────────┐
  │  ┌──────── Lite ─────────┐                           │
  │  │ 📊 analizar-espacio   │  👯 duplicados  🏷️ nombres │
  │  │ (informe de solo      │  🗜️ formatos   📦 programas│
  │  │  lectura)             │  🗓️ limpieza periódica    │
  │  └───────────────────────┘  ↩️ deshacer               │
  └──────────────────────────────────────────────────────┘
```

- 🆓 **Lite** (gratis): el informe de solo lectura.
- 💎 **Pro** (de pago): las seis skills, con cuarentena y deshacer.

---

## 🗺️ Hoja de ruta

- [x] 💡 Idea y reglas comunes
- [ ] 📊 `analizar-espacio`
- [ ] 👯 `buscar-duplicados`
- [ ] 🏷️ `sugerir-nombres`
- [ ] 🗜️ `sugerir-formatos`
- [ ] 🗓️ `limpieza-periodica`
- [ ] 📦 `revisar-programas`
- [ ] 📦 Ediciones Lite y Pro publicadas

---

## ❓ Preguntas frecuentes

**¿Borra cosas sin preguntar?**
Nunca. Todo pasa por un plan que apruebas por bloques, y lo que se quita va a la Papelera o a una cuarentena.

**¿Por qué no limpia a diario?**
Las cachés existen para que todo vaya más rápido: si se borran cada día, se vuelven a llenar enseguida. Lo razonable es cada semana o cada mes, y cuando el disco baje de un umbral.

**¿Sustituye al Sensor de almacenamiento de Windows?**
No: lo configura y añade solo lo que este no cubre.

---

🚧 *Plugin en construcción. Todavía no forma parte del marketplace.*

**Autor:** José Antonio Pastor Rivera
