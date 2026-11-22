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

**Latest report and history:** `docs/informes/` holds only the latest report (every format plus its `.md` sources). Every version is also archived in `docs/informes/historicos/`, renamed with its version, with dots turned into hyphens as `normalize-names` does: `<skill-name>-v0-1-0.pdf`, `.docx`, `.odt`, `.md` and `<skill-name>-v0-1-0-en.pdf`, `-en.md`. When a new version is closed, copy its files into `historicos/` as well; never overwrite or delete an older version there. History starts at the first report the skill had (0.1.0 when it exists).

**Structure:** the same for every skill. Every section carries its emoji **after** its title (`# Idea 💡`), so it shows the same way in the table of contents; drop a section only if it truly has nothing (say so in one line instead of leaving it empty), never reorder them.
- **Cover:** skill name, one line of what it does, author (José Antonio Pastor Rivera), date and version.
- **Table of contents with links** that jump to each section (internal bookmarks, not only page numbers).
1. **Idea** 💡: where the skill comes from and what it is for (and what it is not).
2. **Design** 🧩: flow (ASCII diagram), structure and the decisions taken.
3. **Implementation** 🛠️: files, scripts and how they work.
4. **Tests** ✅: automated tests, tests with real material and cold tests.
5. **Incidents** 🐞: one table with No. (I-01…), incident, cause, fix and status (Resuelta / No resuelta / Sin impacto). The other sections cite them as **I-0N**; there is no second incident table.
6. **Changes after testing** ✏️: what was rewritten because of the tests, before → after.
7. **Integration with other skills** 🔗: which skills it calls or is called by, and why those.
8. **Linux review** 🐧: step 1 of this checklist.
9. **Lessons learned** 🎓: each one as a short paragraph that says what happened in this skill and what it teaches for the next one. Concrete, with the example; no slogans the reader has to decode.
10. **Use of AI** 🤖: say that it was developed with **Claude Code** (Anthropic), with the model used, under the author's direction and review. List the tools and their use, and summarise the main instructions in formal, correct wording: never transcribe the user's prompts literally.
11. **Proposed improvements** 🚀: the proposals of step 5, so they stay in the report.
12. **References** 📚

Sections follow the order of the work **without repeating content** between them.

**How to generate it:** preferably with the `styled-docs` skill (private repo), which does steps 1 to 3 below: `python <styled-docs>/scripts/build.py <report>.md --type assignment --set cover=true --no-save --out-dir docs/informes` and, for English, `--set language=en-US --formats pdf`. Keep the `.md` sources next to the reports so they can be regenerated. By hand (tools already on the laptop; on a failure, note it here):
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

## 5. Proposed improvements 🚀

Propose 2 to 4 improvements of yours for the next version, each with what it changes and why. They go in the report (section 11) and are also listed in the chat. The user decides which ones to accept.

## Versions

Every closing that changes the skill gets a new version in `plugin.json` and on the cover: patch (0.1.0 → 0.1.1) for fixes and documentation only, minor (0.1.0 → 0.2.0) when the skill gains or changes behaviour.

## Commits

When the user asks for commit and push, make **one commit per change**, each with its own message, and push after each one: the skill, its report, its README, a rule in CLAUDE.md… never everything in one mixed commit. That way the history stays ordered and every change can be found and reverted on its own.

## Not done here

- Commit and push: only if the user asks.
- Uploading the reports to a website or marketplace: the user decides.
