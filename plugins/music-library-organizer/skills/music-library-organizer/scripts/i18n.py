"""
Messages and folder names in English, Spanish and Dutch.

All the logic lives in the other scripts. This module only holds the texts,
so a bug is fixed once and a new language is a new column, not a new copy
of the code.

Language: --lang en|es|nl on the command line, or the MLO_LANG environment
variable. Default: English.
"""
import os
import sys

# On Windows, output read through a pipe (as an AI agent reads it) uses the
# legacy code page, so "vacías" arrives as "vac?as". Every script imports this
# module, so forcing UTF-8 here fixes all of them at once.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

LANGUAGES = ("en", "es", "nl")
DEFAULT = "en"

# Folders the user sees after organizing. Internal files (CSVs, journal) keep
# fixed English names so the scripts always find them, whatever the language.
FOLDERS = {
    "library":    {"en": "Library",         "es": "Biblioteca",   "nl": "Bibliotheek"},
    "playlists":  {"en": "Playlists",       "es": "Listas",       "nl": "Afspeellijsten"},
    "quarantine": {"en": "_Quarantine",     "es": "_Cuarentena",  "nl": "_Quarantaine"},
    "lossy":      {"en": "_Missing lossless", "es": "_Pendiente FLAC", "nl": "_Lossless ontbreekt"},
    "redownload": {"en": "_To redownload",  "es": "_Pendiente redescargar", "nl": "_Opnieuw downloaden"},
}

MESSAGES = {
    # inventory.py
    "files_read":      {"en": "  {n} files read...",
                        "es": "  {n} archivos leídos...",
                        "nl": "  {n} bestanden gelezen..."},
    "metadata_done":   {"en": "Metadata: {n} files in {s} s",
                        "es": "Metadatos: {n} archivos en {s} s",
                        "nl": "Metadata: {n} bestanden in {s} s"},
    "hashing":         {"en": "Hashing {n} files that share a size...",
                        "es": "Calculando hash de {n} archivos con tamaño repetido...",
                        "nl": "Hash berekenen van {n} bestanden met dezelfde grootte..."},
    "hash_progress":   {"en": "  hash {i}/{n}",
                        "es": "  hash {i}/{n}",
                        "nl": "  hash {i}/{n}"},
    "inventory_done":  {"en": "\nDone -> {path}",
                        "es": "\nListo -> {path}",
                        "nl": "\nKlaar -> {path}"},
    "inventory_total": {"en": "Total: {n} | Broken: {broken} | Truncated: {truncated} | Time: {s} s",
                        "es": "Total: {n} | Rotos: {broken} | Truncados: {truncated} | Tiempo: {s} s",
                        "nl": "Totaal: {n} | Kapot: {broken} | Afgekapt: {truncated} | Tijd: {s} s"},
    # duplicates.py
    "to_redownload":   {"en": "To redownload: {n}",
                        "es": "Para volver a descargar: {n}",
                        "nl": "Opnieuw downloaden: {n}"},
    "unique_tracks":   {"en": "Unique tracks: {n}",
                        "es": "Canciones únicas: {n}",
                        "nl": "Unieke nummers: {n}"},
    "extra_files":     {"en": "Extra copies: {n} ({gb} GB)",
                        "es": "Archivos sobrantes: {n} ({gb} GB)",
                        "nl": "Overbodige kopieën: {n} ({gb} GB)"},
    "doubtful":        {"en": "Doubtful, to review: {n}",
                        "es": "Dudosos a revisar: {n}",
                        "nl": "Twijfelgevallen om te controleren: {n}"},
    "lossy_only":      {"en": "Lossy only (AAC/MP3): {n}",
                        "es": "Solo en calidad baja (AAC/MP3): {n}",
                        "nl": "Alleen lossy (AAC/MP3): {n}"},
    "reason_duration": {"en": "different durations",
                        "es": "duraciones distintas",
                        "nl": "verschillende duur"},
    "reason_names":    {"en": "same audio, different names",
                        "es": "mismo audio con nombres distintos",
                        "nl": "zelfde audio, andere namen"},
    # organize.py
    "unknown_artist":  {"en": "Unknown", "es": "Desconocido", "nl": "Onbekend"},
    "untitled":        {"en": "Untitled", "es": "Sin titulo", "nl": "Zonder titel"},
    "missing_entry":   {"en": "# MISSING (redownload): {file}",
                        "es": "# FALTA (volver a descargar): {file}",
                        "nl": "# ONTBREEKT (opnieuw downloaden): {file}"},
    "dry_run":         {"en": "DRY RUN (nothing has been moved):",
                        "es": "SIMULACIÓN (no se ha movido nada):",
                        "nl": "PROEFDRAAI (er is niets verplaatst):"},
    "review_plan":     {"en": "Review {path}",
                        "es": "Revisa {path}",
                        "nl": "Controleer {path}"},
    "already_run":     {"en": "A move log already exists: it looks like this already ran. Use --undo first.",
                        "es": "Ya existe un registro: parece que ya se ejecutó. Usa --undo primero.",
                        "nl": "Er bestaat al een logboek: dit lijkt al uitgevoerd. Gebruik eerst --undo."},
    "plan_stale":      {"en": "{n} files in the plan no longer exist (e.g. {example}). Run inventory.py and duplicates.py again.",
                        "es": "{n} archivos del plan ya no existen (ej.: {example}). Vuelve a lanzar inventory.py y duplicates.py.",
                        "nl": "{n} bestanden uit het plan bestaan niet meer (bijv. {example}). Voer inventory.py en duplicates.py opnieuw uit."},
    "skipped_exists":  {"en": "  SKIPPED, already exists: {path}",
                        "es": "  OMITIDO, ya existe: {path}",
                        "nl": "  OVERGESLAGEN, bestaat al: {path}"},
    "moved_progress":  {"en": "  {i}/{n} moved...",
                        "es": "  {i}/{n} movidos...",
                        "nl": "  {i}/{n} verplaatst..."},
    "organize_done":   {"en": "Done: {n} files moved, {lists} playlists in {path}",
                        "es": "Hecho: {n} archivos movidos, {lists} playlists en {path}",
                        "nl": "Klaar: {n} bestanden verplaatst, {lists} afspeellijsten in {path}"},
    "undo_done":       {"en": "Undid {n} moves. (Empty folders and the playlists folder stay; delete them by hand.)",
                        "es": "Deshechos {n} movimientos. (Las carpetas vacías y la de listas quedan; bórralas a mano.)",
                        "nl": "{n} verplaatsingen ongedaan gemaakt. (Lege mappen en de afspeellijstmap blijven staan; verwijder ze zelf.)"},
    "no_log":          {"en": "There is no move log to undo.",
                        "es": "No hay registro de movimientos que deshacer.",
                        "nl": "Er is geen logboek om ongedaan te maken."},
}


def detect_language(argv=None) -> str:
    """--lang xx wins over MLO_LANG; anything unknown falls back to English."""
    argv = sys.argv if argv is None else argv
    lang = os.environ.get("MLO_LANG", DEFAULT)
    if "--lang" in argv:
        i = argv.index("--lang")
        if i + 1 < len(argv):
            lang = argv[i + 1]
    lang = lang.lower()[:2]
    return lang if lang in LANGUAGES else DEFAULT


LANG = detect_language()


def t(key: str, **values) -> str:
    """Text for `key` in the current language, with {placeholders} filled in."""
    return MESSAGES[key][LANG].format(**values)


def folder(key: str) -> str:
    return FOLDERS[key][LANG]
