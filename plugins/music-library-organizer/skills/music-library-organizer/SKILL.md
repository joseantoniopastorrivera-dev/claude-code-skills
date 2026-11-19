---
name: music-library-organizer
description: Read-only health check of a music library of any genre (DJ libraries included). Detects broken or half-finished downloads and finds duplicates by name, file hash and FLAC audio fingerprint, then reports how much space the extra copies take. Moves and deletes nothing. Use when the user wants to know how many duplicates or broken files their music collection has.
license: Free to use. Redistribution not allowed. See LICENSE.txt.
metadata:
  version: "2.0.0"
  author: José Antonio Pastor Rivera
---

# Music Library Organizer

A **read-only** analysis: it tells the user what is wrong with their library without touching a single file.

Scripts: the `scripts/` folder next to this file (`inventory.py`, `duplicates.py`). They need Python 3.8+ and `pip install mutagen`. Add `--lang en` (or `es`, `nl`) to every command.

## Rules

1. **Read only.** Never move, rename or delete audio files. The scripts only write CSVs inside `<root>/_mlo/output/`.
2. **Explain every step** and what each figure means.
3. **Never publish real data** (CSVs, folder names with people's names). Aggregate figures only.

## Phase 0 — Reconnaissance

- List the top-level folders (folder by folder if a listing is cut off).
- **Playlists inside subfolders** (`X/Playlist/Y`): the "playlist" is the folder that holds the file.
- Ask whether Python is installed and which player or DJ software the user uses.

## Phase 1 — Inventory

`python scripts/inventory.py "<root>" --lang en` → `<root>/_mlo/output/inventory.csv`.

- `BROKEN`: read error, < 100 KB or < 30 s.
- `TRUNCATED`: lossless with real_kbps (`size·8/duration`) < 250; a half-finished download keeps a header with the full duration.
- SHA-256 only for files that share a size. Folders starting with `_` are skipped.

## Phase 2 — Duplicates

`python scripts/duplicates.py "<root>" --lang en` → `tracks.csv`, `files.csv`, `to_redownload.csv`.

- Union-Find over three signals: normalized name, SHA-256 and FLAC audio MD5.
- Best copy: lossless > real_kbps > has tags > size.
- Doubtful groups (same audio, different names; different durations) are listed for the user to review.

## Report

Summarize for the user: total files, unique tracks, extra copies and the GB they take, broken and truncated files, tracks to download again, tracks only available in lossy quality, and the doubtful groups worth checking by ear. Point them to `tracks.csv` (one row per track, with the playlists it appears in) and `files.csv` (KEEP / EXTRA / BROKEN / TRUNCATED per file).

If the user wants to act on the report (one clean library, playlists rebuilt from the old folders, quarantine instead of deletion, full undo), that is what **Music Library Organizer Pro** does.
