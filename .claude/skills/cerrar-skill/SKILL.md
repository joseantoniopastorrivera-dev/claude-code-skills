---
name: cerrar-skill
description: Cierra el desarrollo o refinado de una skill de Claude Code - revisa si sirve en Linux, comprueba que todo funciona, genera el informe final en PDF, DOCX y ODT (y un PDF en inglés) y completa el README. Úsala cuando el usuario diga que una skill está terminada, pida "cerrar la skill", "el informe de la skill" o antes de darla por acabada.
---

# Cerrar una skill

Lista de pasos que se hace **siempre** antes de dar por terminada una skill, sea del repo público `claude-code-skills` o del privado `claude-code-skills-private`. Cada paso se enseña al usuario y se espera su visto bueno antes de seguir.

## 1. Revisión en Linux 🐧

Antes de cerrar, responde por escrito:
- ¿Tiene sentido la skill en Linux? Si no, di por qué en una línea.
- ¿Qué cambia? Rutas, comandos, permisos (`sudo`), gestor de paquetes (apt, snap, flatpak), programador de tareas (systemd timers o cron) y codificación de la consola.
- ¿El código ya lo contempla? Si no, propón el cambio mínimo: una tabla por sistema operativo y `platform.system()`, con una sola lógica.
- Si hace falta probarlo en la máquina virtual Linux del USB, apúntalo en `pendientes.md` del repo.

## 2. Comprobaciones ✅

- Tests en verde (`python -m pytest`) si la skill tiene código.
- El frontmatter del `SKILL.md` es válido: `name` en minúsculas con guiones y una `description` que dice qué hace y cuándo usarla.
- No hay rutas personales, credenciales, tokens ni datos reales.
- Si la skill se vende o se reparte en zip, el `build.py` del repo genera los zips sin errores.

## 3. Informe final 📄

**Nombre:** el nombre de la skill en minúsculas con guiones, con las reglas de `normalize-names` (plugin `organize-files`, en el repo privado): `<nombre-skill>.pdf`, `.docx` y `.odt`, más `<nombre-skill>-en.pdf` en inglés. Van en `docs/informes/` dentro de la carpeta de la skill o del plugin.

**Estructura:** la de las prácticas del usuario, que sirven de modelo (`C:\dev\Sistemas-Gestion-Empresarial`, carpetas `ut02-practica-odoo`, `-v2` y `ut03-practica-odoo-v3`):
1. **Portada:** nombre de la skill, una línea de qué hace, autor (José Antonio Pastor Rivera), fecha y versión.
2. **Índice con enlaces** que saltan a cada apartado (marcadores internos, no solo números de página).
3. **Índice de incidencias:** tabla con Nº (I-01…), incidencia, apartado y estado (Resuelta / No resuelta / Sin impacto).
4. **Apartados numerados por fases** de lo que se ha hecho: idea, diseño, implementación, pruebas, revisión en Linux… Los que hagan falta, **sin repetir contenido** entre apartados.
5. **Incidencias:** la misma tabla, con causa y solución.
6. **Conclusiones y aprendizajes**, en viñetas.
7. **Uso de IA:** qué herramienta se usó, para qué y los prompts principales.

**Iconos:** cada apartado lleva un icono sencillo que resume lo hecho (🔍 análisis, 🧩 diseño, 🛠️ código, ✅ pruebas, 🐧 Linux, ✏️ renombrado, 🧹 limpieza…). Se dibujan como PNG pequeños (con Pillow, o SVG pasado a PNG), porque OpenOffice puede no pintar los emojis en el PDF. Los esquemas de carpetas o flujos van en ASCII art, dentro de un bloque de código.

**Cómo generarlo** (herramientas que ya hay en el portátil; compruébalo la primera vez y anota aquí lo que falle):
1. `python-docx` crea el `.docx`: estilos de título, índice con hipervínculos a marcadores, tablas e imágenes.
2. OpenOffice 4 lo convierte sin abrir ventanas:
   ```
   "C:\Program Files (x86)\OpenOffice 4\program\soffice.exe" --headless --convert-to odt <archivo>.docx
   "C:\Program Files (x86)\OpenOffice 4\program\soffice.exe" --headless --convert-to pdf <archivo>.docx
   ```
3. Revisa el PDF: los enlaces del índice saltan bien, las imágenes salen y no hay tildes rotas.
4. Repite con el texto en inglés solo para `<nombre-skill>-en.pdf`.

Antes de generarlo, enseña al usuario el índice propuesto y espera su visto bueno.

## 4. README 📘

Cuando el PDF final esté aprobado, **completa** el README de la skill o del plugin con lo que finalmente se ha hecho: qué hace, cómo se usa, resultados y la sección de Linux. Respeta su formato actual (secciones, idiomas, tablas); no lo reescribas desde cero. Añade un enlace al informe.

## 5. Preguntas de Claude 💬

Termina con un apartado breve de 2 a 4 propuestas tuyas para la siguiente versión. El usuario decide si las acepta.

## Lo que no se hace aquí

- Commit y push: solo si el usuario lo pide.
- Subir los informes a una web o marketplace: lo decide el usuario.
