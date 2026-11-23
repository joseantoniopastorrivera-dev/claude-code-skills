---
title: finalize-skill
subtitle: Claude Code skill that closes the development of a skill · version 0.1.0
author: José Antonio Pastor Rivera
date: 23 November 2026
---

# Idea 💡

When the first skills were finished, each one was treated as done in a different way: some had a complete README and others did not, none had a report of the work and nobody had checked whether they worked on Linux. `finalize-skill` is the checklist that is **always** run before a skill is treated as finished, both in the public `claude-code-skills` repository and in the private one.

What it does, in five steps the author approves one by one:

1. Linux review;
2. checks (tests, `SKILL.md` frontmatter, no personal data, packaging);
3. final report in PDF, DOCX and ODT, plus a PDF in English;
4. a complete README with what was finally done;
5. proposed improvements for the next version.

> **What it is not:** it does not commit or publish anything. Uploading changes or publishing the reports is always the author's decision.

# Design 🧩

## Flow

```
   finished skill
        |
        v
   1. Linux review --> pendientes.md if it must
        |              be tested on the VM
        v
   2. Checks: tests, frontmatter,
      personal data, zip
        |
        v
   3. Proposed contents --> approval
        |
        v
      Report .md --> styled-docs --> PDF, DOCX,
        |                            ODT and English PDF
        v
      docs/informes/ (latest)
      docs/informes/historicos/ (every version)
        |
        v
   4. Complete README, linking the report
        |
        v
   5. Proposed improvements --> author decides
```

## Decisions

| Decision | Reason |
|---|---|
| Repository skill (`.claude/skills/`), not a plugin | It is a working rule of the repository itself, not something to sell |
| Author approval at every step | A report with the wrong contents has to be rebuilt from scratch |
| Common contents for every skill, emoji after the title | Reports can be compared and the emoji shows the same in the contents |
| One single incident table (I-01…) | The other sections cite it; two tables ended up telling the same story |
| Latest report in `docs/informes/`, every version in `historicos/` | Full tracking of each skill's evolution without losing versions |
| Semantic versioning | Patch for fixes or documentation, minor when the skill does something new |

# Implementation 🛠️

| File | Content |
|---|---|
| `SKILL.md` | The five steps, the report structure, versions, commits and what is not done here |
| `scripts/aoo_convert.py` | DOCX to ODT and PDF conversion with Apache OpenOffice 4 over UNO |

`aoo_convert.py` runs with OpenOffice's own Python (2.7). It starts OpenOffice without a window, opens the DOCX, gives the bookmarks back their real names (OpenOffice renames them to `Bookmark`, `Bookmark1`… on import) and saves the ODT and the PDF. Without that step, the table of contents links would lead nowhere.

The preferred way to build the report is the `styled-docs` skill (private repository), which bundles DOCX creation, conversion and the PDF link check. The manual steps remain in `SKILL.md` in case `styled-docs` is not available.

# Tests ✅

- **Real use.** The checklist was applied when closing `styled-docs`, `explain-repo` and the exam preparation skill. Their three reports were built following step 3 and checked with 0 broken links.
- **This report** was built with `styled-docs` following the skill itself, like the reports of the other plugins closed the same day.
- The skill has no code of its own apart from `aoo_convert.py`, which was tested by converting the earlier reports.

# Incidents 🐞

| No. | Incident | Cause | Fix | Status |
|---|---|---|---|---|
| I-01 | PDF contents led nowhere | OpenOffice renames DOCX bookmarks to `Bookmark`, `Bookmark1`… | `aoo_convert.py` restores the real names | Solved |
| I-02 | Conversion hung | `soffice --convert-to` is LibreOffice; Apache OpenOffice opens a window and waits | Conversion over UNO with a windowless OpenOffice | Solved |
| I-03 | Titles printed as "2. 2. Design" | OpenOffice numbers the `Heading 1` style in its outline | Custom paragraph style for titles | Solved |
| I-04 | `python -I` could not find python-docx or Pillow | They live in the user site-packages | Run with plain `python` | Solved |
| I-05 | Every report had different sections | The first version copied the SGE practice structure without fixing it | Common 12-section contents | Solved |
| I-06 | Each version's report was overwritten | Only `docs/informes/` existed | `historicos/` folder with the version in the name | Solved |
| I-07 | Windows paths hard-coded in `aoo_convert.py` | The script was written only for the laptop | `styled-docs` already fixed its own copy; still pending here | Not solved |

# Changes after testing ✏️

| Before | After |
|---|---|
| `cerrar-skill`, in Spanish | `finalize-skill`, in English like every new skill |
| SGE practice structure with a separate incident index (I-05) | Common 12-section contents with one incident table |
| Final "Claude's questions" section only in the chat | Section 🚀 inside the report and also in the chat |
| Report built by hand with python-docx and OpenOffice | `styled-docs` as the preferred path, manual steps as backup |
| One report per skill, overwritten (I-06) | Latest report plus a history per version |
| No version rule | Patch or minor version at each closing |
| No commit rule | One commit per change, each pushed |

# Integration with other skills 🔗

| Skill | Relation | Why |
|---|---|---|
| `styled-docs` | Builds the report | Contents with checked links, two-way notes, DOCX and ODT |
| `normalize-names` (`organize-files`) | Sets the names of the report and history files | Same rule in every repository: lowercase, hyphens and version `v0-1-0` |
| `write-skill` (gstack) | Used earlier, when writing the skill | `finalize-skill` checks the result, not how it was written |
| Every skill in both repositories | Goes through here before being treated as finished | It is the closing rule in `CLAUDE.md` |

# Linux review 🐧

- **Does it make sense on Linux?** Yes: the checklist does not depend on the system.
- **What changes:** `python3` instead of `python`, and the OpenOffice path (`/opt/openoffice4/program`). `aoo_convert.py` has the Windows paths hard-coded (I-07).
- **Does the code handle it?** On the preferred path yes, because `styled-docs` looks for OpenOffice on both systems. On the manual path, no.
- **Pending:** test the manual path on the Linux virtual machine on the USB drive.

# Lessons learned 🎓

**Fix the structure before the second report.** The first report copied the SGE practice structure and the second adapted it its own way. With two different reports they could no longer be compared. Since then the contents are common and a section is only dropped if it truly has nothing.

**Keep every version from the start.** The first reports were overwritten when a new version was closed, and the previous one only survived in the git history. With `historicos/`, the evolution of each skill can be seen by opening a folder.

**One change, one commit.** Mixing the skill, its report and a `CLAUDE.md` rule in a single commit made it hard to find or revert any of them. Now each change goes separately, with its push.

**Reuse the tool that already exists.** The manual python-docx and OpenOffice path worked, but every report repeated the same fixes. When `styled-docs` appeared, the skill switched to it and kept the manual steps only as a backup.

# Use of AI 🤖

The skill was developed with **Claude Code**, Anthropic's assisted development tool, with the Claude Opus 5.5 model, under the author's direction and review at every step.

| Tool | Use |
|---|---|
| Claude Code | Writing the skill, `aoo_convert.py` and this report |
| `styled-docs` | Building this report in PDF, DOCX and ODT |
| Apache OpenOffice 4 | Conversion to ODT and PDF |

## Main instructions

1. **Initial brief.** Define a mandatory closing process for every skill: Linux review, a report in several formats following the structure of the author's practices, and a complete README.
2. **English name.** Rename the skill to `finalize-skill` and write it in English, like every new skill.
3. **Common contents.** Unify the contents of every report, with the emoji after the title and the proposed improvements inside the report, and add a version rule.
4. **History.** Keep the latest report in `docs/informes/` and a renamed copy of every version in `docs/informes/historicos/`, and apply it to every skill.
5. **Commits.** Make one commit per change, each pushed, so the history stays ordered.

# Proposed improvements 🚀

Proposals for the next version. The author decides which ones are accepted.

1. **Archive script.** A script `archive_report.py <skill> <version>` that copies the report files to `historicos/` with the right name and refuses to overwrite an archived version. Today it is done by hand.
2. **Drop the copy of `aoo_convert.py`.** Always use the one in `styled-docs`, which already works on Linux (I-07), instead of keeping two copies.
3. **Automatic contents check.** A script that verifies the report `.md` has the 12 sections in order, with their emoji, before building it.
4. **Version in `plugin.json`.** Check that the version on the cover matches `plugin.json` and the history file name.

# References 📚

- `CLAUDE.md` of the `claude-code-skills` repository: skill closing rule.
- `styled-docs` (private repository): document generation with a checked table of contents.
- `normalize-names` (`organize-files` plugin, private repository): naming rules.
- Apache OpenOffice 4, UNO API: document conversion.
