---
name: finalize-skill
description: Finalizes the development or refinement of a Claude Code skill - checks whether it works on Linux, verifies everything passes, generates the final report in PDF, DOCX and ODT (plus a PDF in English) and completes the README. Use it when the user says a skill is finished, asks to "finalize the skill", "close the skill" ("cerrar la skill"), for "the skill report", or before treating a skill as done.
---

# Finalize a skill

Checklist that is **always** run before a skill is treated as finished, whether it lives in the public repo `claude-code-skills` or the private `claude-code-skills-private`. Show each step to the user and wait for their approval before going on. Talk to the user in their own language.

## 1. Linux review 🐧

Before finalizing, answer in writing:
- Does the skill make sense on Linux? If not, say why in one line.
- What changes? Paths, commands (`python3`), permissions (`sudo`), package manager (apt, snap, flatpak), task scheduler (systemd timers or cron) and console encoding.
- Does the code already handle it? If not, propose the smallest change: one table per operating system and `platform.system()`, with a single logic.
- If it needs testing on the Linux virtual machine on the USB drive, add it to the repo's `pendientes.md`.

## 2. Checks ✅

- Tests green (`python -m pytest`) if the skill has code. Code with no tests gets a few now.
- The `SKILL.md` frontmatter is valid: `name` in lowercase with hyphens and a `description` that says what it does and when to use it.
- No personal paths, credentials, tokens or real data.
- If the skill is sold or shipped as a zip, the repo's `build.py` builds the zips without errors.

## 3. Final report 📄

**Name:** the skill's name in lowercase with hyphens, following the `normalize-names` rules (plugin `organize-files`, in the private repo): `<skill-name>.pdf`, `.docx` and `.odt`, plus `<skill-name>-en.pdf` in English. They go in `docs/informes/` inside the skill's or plugin's folder. The report is written in Spanish; only the `-en.pdf` is in English.

**Structure:** the one of the user's practices, which are the model (`C:\dev\Sistemas-Gestion-Empresarial`, folders `ut02-practica-odoo`, `-v2` and `ut03-practica-odoo-v3`):
1. **Cover:** skill name, one line of what it does, author (José Antonio Pastor Rivera), date and version.
2. **Table of contents with links** that jump to each section (internal bookmarks, not only page numbers).
3. **Incident index:** table with No. (I-01…), incident, section and status (Resuelta / No resuelta / Sin impacto).
4. **Sections numbered by phase** of the work: idea, design, implementation, tests, Linux review… As many as needed, **without repeating content** between sections.
5. **Incidents:** the same table, with cause and fix.
6. **Conclusions and lessons learned**, as bullets.
7. **Use of AI:** which tool was used, for what and the main prompts.

**Icons:** each section has a simple icon that sums up the work (🔍 analysis, 🧩 design, 🛠️ code, ✅ tests, 🐧 Linux, ✏️ renaming, 🧹 cleanup…). Draw them as small PNGs (with Pillow, or SVG converted to PNG), because OpenOffice may not render emojis in the PDF. Folder or flow diagrams go in ASCII art, inside a code block.

**How to generate it** (tools already on the laptop; on a failure, note it here):
1. `python-docx` creates the `.docx`: table of contents with hyperlinks to bookmarks, tables and images. Run it with plain `python`, not `python -I` (Pillow and python-docx live in the user site-packages). Level-1 titles use a custom paragraph style, not `Heading 1`: OpenOffice puts `Heading 1` in its numbered outline and prints "2. 2. Design".
2. OpenOffice 4 converts it with `scripts/aoo_convert.py` (in this skill's folder), run with OpenOffice's own Python. Never use `soffice --convert-to`: that is LibreOffice, and Apache OpenOffice opens a window and hangs.
   ```
   "C:\Program Files (x86)\OpenOffice 4\program\python.exe" scripts\aoo_convert.py <file>.docx <file>.odt <file>.pdf
   ```
   The script also restores the bookmark names, which OpenOffice renames to Bookmark, Bookmark1… on import (the table of contents links would otherwise lead nowhere).
3. Check the PDF: every table of contents link has a destination, the images show and no accents are broken.
4. Repeat with the English text only for `<skill-name>-en.pdf`.

Before generating it, show the user the proposed table of contents and wait for their approval.

## 4. README 📘

Once the final PDF is approved, **complete** the skill's or plugin's README with what was finally done: what it does, how to use it, results and the Linux section. Keep its current format (sections, languages, tables); do not rewrite it from scratch. If there is none, create it following the repo's README rules. Add a link to the report.

## 5. Claude's questions 💬

End with a short section «Preguntas de Claude» with 2 to 4 proposals of yours for the next version. The user decides whether to accept them.

## Not done here

- Commit and push: only if the user asks.
- Uploading the reports to a website or marketplace: the user decides.
