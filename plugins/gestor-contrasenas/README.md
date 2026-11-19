# 🔐 gestor-contrasenas

> 🚧 **En construcción.** Este plugin todavía no se puede instalar. Este README explica lo que será.

Skill para Claude Code que **genera, guarda y usa contraseñas de forma profesional** en Windows y Linux, apoyándose en un gestor de contraseñas de verdad. Y con una regla de oro: **Claude nunca llega a ver el secreto.**

---

## 📑 Índice

1. [🎯 Por qué existe](#-por-qué-existe)
2. [🛡️ La regla de oro](#️-la-regla-de-oro)
3. [🧭 Cómo funcionará](#-cómo-funcionará)
4. [🧰 Modos](#-modos)
5. [💻 Plataformas](#-plataformas)
6. [🏠 Nube o autoalojado](#-nube-o-autoalojado)
7. [📦 Ediciones](#-ediciones)
8. [🗺️ Hoja de ruta](#️-hoja-de-ruta)
9. [❓ Preguntas frecuentes](#-preguntas-frecuentes)

---

## 🎯 Por qué existe

Montando un servidor es muy fácil acabar con contraseñas donde no deben estar:

- 📝 en un `.txt` en el escritorio;
- 📸 en una captura de pantalla que va a un informe;
- 🧾 en el historial de la terminal o en un log;
- 🐙 en un commit de un repositorio público.

Esta skill nace de un caso real: una contraseña maestra que el propio programa mostraba en pantalla acabó en tres capturas destinadas a un documento. La solución fue la de siempre: **rotarla** (cambiarla) y guardar la nueva en un gestor. La skill convierte ese procedimiento en algo automático y repetible.

---

## 🛡️ La regla de oro

```
   ┌──────────────┐   genera y guarda    ┌──────────────────┐
   │  Claude Code │ ───────────────────▶ │ Gestor (cifrado) │
   │   (la skill) │   sin ver el valor   │   🔒 caja fuerte │
   └──────┬───────┘                      └────────┬─────────┘
          │                                       │
          │  "usa la contraseña X"                │ el secreto va directo
          ▼                                       ▼
   ┌──────────────┐                      ┌──────────────────┐
   │  Tú desbloq. │                      │ 📋 portapapeles  │
   │  el gestor 🔑│                      │  (se borra solo) │
   └──────────────┘                      └──────────────────┘
```

- ✅ La contraseña se **genera dentro del gestor** y se guarda en el mismo paso.
- ✅ Para usarla, va al **portapapeles** (que se vacía a los pocos segundos) o a una variable de entorno de un único comando.
- ❌ Nunca se muestra en pantalla, ni se escribe en ficheros, ni pasa por el historial.
- 🔑 El desbloqueo del gestor lo haces **tú**. Claude no teclea contraseñas maestras.

---

## 🧭 Cómo funcionará

```
  tú ──▶ "créame la contraseña de la base de datos de pruebas"
           │
           ▼
  ┌─────────────────┐   1. comprueba que el gestor está desbloqueado
  │ gestor-contras. │   2. genera 24+ caracteres aleatorios
  │                 │   3. crea la entrada: nombre, URL, usuario, notas
  └────────┬────────┘   4. te dice DÓNDE está, nunca QUÉ es
           │
           ▼
  ✔ "Guardada como «BD pruebas · postgres». Está en tu portapapeles 30 s."
```

---

## 🧰 Modos

| Modo | Qué hace | Toca el secreto |
|---|---|---|
| 🆕 `nueva` | Genera una contraseña o frase y crea la entrada | Solo dentro del gestor |
| 📋 `usar` | La busca por nombre o URL y la deja en el portapapeles | Solo en el portapapeles |
| 🔄 `rotar` | Cambia un secreto expuesto y te guía para cambiarlo en el servicio | Solo dentro del gestor |
| 🔍 `auditar` | Busca secretos en texto plano en una carpeta o repo, también en capturas de pantalla | Solo lectura; avisa, no muestra |
| 🐧 `servidor-linux` | Buenas prácticas en servidores: permisos `600`, hashes en ficheros de configuración, `.pgpass`, secretos de Docker | Revisa y propone |

---

## 💻 Plataformas

```
            ┌───────────────────────────┐
            │   gestor-contrasenas      │
            └─────────────┬─────────────┘
          ┌───────────────┴───────────────┐
          ▼                               ▼
   🪟 Windows                         🐧 Linux
   ─────────────                      ─────────────
   Bitwarden + bw CLI                 bw CLI · pass + GPG
   Set-Clipboard                      xclip · wl-copy
   winget                             apt · snap · npm
                                      servidores sin escritorio ✔
```

---

## 🏠 Nube o autoalojado

| | ☁️ Nube | 🏠 Autoalojado (Vaultwarden en Docker) |
|---|---|---|
| Disponible | 24/7 | Cuando tu servidor esté encendido |
| Copias de seguridad | Las hace el proveedor | Las haces tú |
| HTTPS | Ya viene | Lo montas tú (obligatorio) |
| Ideal para | Tus contraseñas reales | Aprender, laboratorios y equipos pequeños |

La edición Pro incluirá una guía para montar el servidor autoalojado con copias de seguridad automáticas.

---

## 📦 Ediciones

```
  ┌──────────────────────── Pro ────────────────────────┐
  │  ┌──────── Lite ────────┐                           │
  │  │  🆕 nueva  📋 usar   │  🔄 rotar   🔍 auditar    │
  │  │  (Bitwarden)         │  🐧 servidor-linux        │
  │  └──────────────────────┘  🏠 autoalojado           │
  │                            🔀 varios gestores       │
  └─────────────────────────────────────────────────────┘
```

- 🆓 **Lite** (gratis): `nueva` y `usar` con Bitwarden.
- 💎 **Pro** (de pago): todo lo demás, con varios gestores (Bitwarden, KeePassXC, `pass`…), auditoría con lectura de capturas y la guía de autoalojado.

---

## 🗺️ Hoja de ruta

- [x] 💡 Idea y diseño de la regla de oro
- [ ] 🆕 Modo `nueva` (Windows)
- [ ] 📋 Modo `usar` (Windows)
- [ ] 🐧 Soporte para Linux
- [ ] 🔄 `rotar` y 🔍 `auditar`
- [ ] 🏠 Guía de autoalojado
- [ ] 📦 Ediciones Lite y Pro publicadas

---

## ❓ Preguntas frecuentes

**¿Claude puede leer mis contraseñas?**
No. La skill está diseñada para que el valor vaya del gestor al portapapeles sin pasar por la conversación.

**¿Necesito Bitwarden?**
Para la Lite, sí: es gratuito y de código abierto. La Pro admitirá otros gestores.

**¿Y si una contraseña ya se filtró?**
Para eso está `rotar`: no basta con borrarla del sitio donde apareció, hay que cambiarla.

---

🚧 *Plugin en construcción. Todavía no forma parte del marketplace.*

**Autor:** José Antonio Pastor Rivera
