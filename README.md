# claude-code-skills

Skills que he creado con [Claude Code](https://docs.claude.com/en/docs/claude-code) durante el ciclo de DAM. El repositorio es un **marketplace de plugins**: cada plugin agrupa las skills de un tema, y cada proyecto activa solo los que necesita.

| Plugin | Skills | Para qué sirve |
|---|---|---|
| [`techno-library-organizer`](plugins/techno-library-organizer/) | `organizar-biblioteca-musical` | Limpiar una biblioteca musical de DJ: duplicados, descargas rotas y carpetas convertidas en playlists. Incluye la herramienta en Python con sus tests. |
| [`desarrollo-por-fases`](plugins/desarrollo-por-fases/) | `preparar-fase`, `plan-pruebas-fase` | Arrancar cada fase de una hoja de ruta (rama, copia de seguridad, tests y plan aprobado) y cerrarla con un plan de pruebas imprimible. |
| [`ordenar-archivos`](plugins/ordenar-archivos/) | `normalizar-nombres` | Renombrar documentos y carpetas de uno o varios repos git a minúsculas con guiones, conservando el historial. |

## Instalación

En Claude Code:

```
/plugin marketplace add joseantoniopastorrivera-dev/claude-code-skills
/plugin install desarrollo-por-fases@claude-code-skills
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
    "desarrollo-por-fases@claude-code-skills": true
  }
}
```

Cuando cambie una skill aquí, actualiza la copia instalada con `/plugin marketplace update claude-code-skills`.

## Skills genéricas y datos de cada proyecto

Las skills no contienen datos de ningún proyecto. Lo propio de cada uno (rutas, comandos, quién prueba, reglas extra) va en su `CLAUDE.md`, en una sección **"Skills de fases"**. Así hay una sola copia de cada skill y el repositorio puede ser público.

## Estructura

```
.claude-plugin/marketplace.json     catálogo de plugins
plugins/<plugin>/
├── .claude-plugin/plugin.json
├── skills/<skill>/SKILL.md
└── …                               scripts o código que usan las skills
```

## Licencia

[MIT](LICENSE)
