# claude-code-skills

Skills que he creado con [Claude Code](https://docs.claude.com/en/docs/claude-code) como proyecto personal. El repositorio es un **marketplace de plugins**: cada plugin agrupa las skills de un tema, y cada proyecto activa solo los que necesita.

Todas mis skills se desarrollan en privado. Aquí solo se publica la **edición gratuita** de cada una cuando está lista; la completa (`<skill>-pro`) se vende en [Agensi](https://agensi.io).

| Plugin | Skills | Para qué sirve |
|---|---|---|
| [`music-library-organizer`](plugins/music-library-organizer/) | `music-library-organizer` | Revisar una biblioteca musical de cualquier género: duplicados, descargas rotas y espacio desperdiciado. Solo lee. |

## Ediciones de pago

- [**Music Library Organizer**](plugins/music-library-organizer/): revisa una biblioteca musical de cualquier género (duplicados y descargas rotas). La edición gratuita, `music-library-organizer`, se instala desde aquí y solo lee. La completa, `music-library-organizer-pro`, también ordena y crea las playlists, y llegará pronto a [Agensi](https://agensi.io). Tiene su propia licencia, no MIT.

## 🚧 En construcción

Todavía no se pueden instalar. Cada enlace lleva a un README que explica lo que serán. Saldrán con edición Lite gratis y Pro de pago.

- 🔐 [**gestor-contrasenas**](plugins/gestor-contrasenas/): genera, guarda y usa contraseñas con un gestor de verdad (Bitwarden), en Windows y Linux, sin que Claude llegue a ver el secreto.
- 🧹 [**optimizar-ordenador**](plugins/optimizar-ordenador/): recupera espacio y mantiene el ordenador ordenado. Primero un informe de solo lectura, luego un plan que apruebas y nunca un borrado sin poder deshacerlo.
- 🧭 [**phased-development**](plugins/phased-development/): arranca cada fase de una hoja de ruta (rama, copia, tests y plan aprobado) y la cierra con un plan de pruebas imprimible. Antes `desarrollo-por-fases`.
- 🗂️ [**organize-files**](plugins/organize-files/): renombra documentos y carpetas de repos git a minúsculas con guiones y clasifica las descargas de clase en su asignatura. Antes `ordenar-archivos`.
- 💼 [**job-applications**](plugins/job-applications/): analiza ofertas, adapta el CV y la carta a cada una sin inventar nada y deja la candidatura lista para que la envíes tú.
- ✏️ [**create-ascii-art**](plugins/create-ascii-art/): dibuja explicaciones como texto (árboles, capas, flujos) que caben en la pantalla del móvil.

Las versiones 1 de `desarrollo-por-fases` y `ordenar-archivos` se publicaron aquí con licencia MIT y siguen en el historial de git con esa licencia.

## Instalación

En Claude Code:

```
/plugin marketplace add joseantoniopastorrivera-dev/claude-code-skills
/plugin install music-library-organizer@claude-code-skills
```

Para que un proyecto use un plugin sin instalarlo a mano, añade a su `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-code-skills": {
      "source": { "source": "github", "repo": "joseantoniopastorrivera-dev/claude-code-skills" }
    }
  },
  "enabledPlugins": {
    "music-library-organizer@claude-code-skills": true
  }
}
```

Cuando cambie una skill aquí, actualiza la copia instalada con `/plugin marketplace update claude-code-skills`.

## Skills genéricas y datos de cada proyecto

Las skills no contienen datos de ningún proyecto. Lo propio de cada uno (rutas, comandos, quién prueba, reglas extra) va en su `CLAUDE.md` (por ejemplo, una sección **"Phase skills"**). Así hay una sola copia de cada skill y el repositorio puede ser público.

## Estructura

```
.claude-plugin/marketplace.json     catálogo de plugins
plugins/<plugin>/
├── .claude-plugin/plugin.json
├── skills/<skill>/SKILL.md
└── …                               scripts o código que usan las skills
```

## Licencia

[MIT](LICENSE), salvo los plugins que traen su propio `LICENSE` (como `music-library-organizer`).
