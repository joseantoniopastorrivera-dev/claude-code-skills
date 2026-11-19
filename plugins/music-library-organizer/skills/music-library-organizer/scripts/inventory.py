"""
PHASE 1 - Library inventory (READ ONLY: moves and deletes nothing).

Usage:
    pip install mutagen
    python inventory.py "D:\\Music" [--lang en|es|nl]

Output: <root>/_mlo/output/inventory.csv (opens in Excel or LibreOffice)
"""
import csv
import hashlib
import os
import time
from collections import defaultdict
from pathlib import Path

from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

from common import output_dir, parser
from i18n import t

AUDIO_EXTENSIONS = {".flac", ".wav", ".m4a", ".mp3", ".aiff", ".aif"}
MIN_SIZE = 100 * 1024          # < 100 KB = empty or almost empty download
MIN_DURATION = 30              # seconds; anything shorter is not a track
MIN_LOSSLESS_KBPS = 250        # a real FLAC/WAV never goes below this
CHUNK = 1024 * 1024            # read 1 MB at a time when hashing

COLUMNS = ["playlist", "relative_path", "file", "extension", "size_bytes", "modified",
           "status", "codec", "bitrate_kbps", "sample_rate", "bits", "real_kbps",
           "duration_s", "artist", "title", "flac_audio_md5", "sha256", "error"]


def read_metadata(path: Path) -> dict:
    """Opens the file with mutagen and reads technical quality and tags."""
    data = {"duration_s": "", "codec": "", "bitrate_kbps": "", "sample_rate": "",
            "bits": "", "artist": "", "title": "", "flac_audio_md5": "", "error": ""}
    try:
        audio = MutagenFile(path, easy=False)
        if audio is None:
            data["error"] = "unrecognized format"
            return data
        info = audio.info
        data["duration_s"] = round(getattr(info, "length", 0) or 0, 2)
        data["bitrate_kbps"] = round((getattr(info, "bitrate", 0) or 0) / 1000)
        data["sample_rate"] = getattr(info, "sample_rate", "") or ""
        data["bits"] = getattr(info, "bits_per_sample", "") or ""

        if isinstance(audio, FLAC):
            data["codec"] = "flac"
            md5 = info.md5_signature            # fingerprint of the DECODED audio
            data["flac_audio_md5"] = f"{md5:032x}" if md5 else ""
            tags = audio.tags or {}
            data["artist"] = "; ".join(tags.get("artist", []))
            data["title"] = "; ".join(tags.get("title", []))
        elif isinstance(audio, MP4):
            data["codec"] = getattr(info, "codec", "")   # 'alac' or 'mp4a.40.2' (AAC)
            tags = audio.tags or {}
            data["artist"] = "; ".join(tags.get("\xa9ART", []))
            data["title"] = "; ".join(tags.get("\xa9nam", []))
        else:
            data["codec"] = path.suffix.lower().lstrip(".")
            easy = MutagenFile(path, easy=True)
            if easy is not None and easy.tags:
                data["artist"] = "; ".join(easy.tags.get("artist", []))
                data["title"] = "; ".join(easy.tags.get("title", []))
    except Exception as e:                      # corrupt or truncated file
        data["error"] = f"{type(e).__name__}: {e}"
    return data


def file_status(row: dict) -> str:
    """OK, BROKEN (empty/unreadable) or TRUNCATED (half-finished download)."""
    if row["error"] or row["size_bytes"] < MIN_SIZE:
        return "BROKEN"
    duration = row["duration_s"] or 0
    if duration < MIN_DURATION:
        return "BROKEN"
    real_kbps = row["size_bytes"] * 8 / duration / 1000
    row["real_kbps"] = round(real_kbps)
    if row["codec"] in ("flac", "wav", "alac") and real_kbps < MIN_LOSSLESS_KBPS:
        return "TRUNCATED"
    return "OK"


def sha256_file(path: Path) -> str:
    """Fingerprint of ALL the bytes of the file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = parser("Phase 1: read-only inventory of a music library.").parse_args().root
    out = output_dir(root)

    # 1) Walk the folders and read metadata
    rows = []
    start = time.time()
    for current, subfolders, files in os.walk(root):
        subfolders[:] = [d for d in subfolders if not d.startswith("_")]
        for name in files:
            path = Path(current) / name
            if path.suffix.lower() not in AUDIO_EXTENSIONS:
                continue
            stat = path.stat()
            row = {
                "playlist": path.parent.relative_to(root).as_posix(),
                "relative_path": path.relative_to(root).as_posix(),   # "/" on every OS
                "file": name,
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified": time.strftime("%Y-%m-%d %H:%M", time.localtime(stat.st_mtime)),
            }
            row.update(read_metadata(path))
            row["status"] = file_status(row)
            rows.append(row)
            if len(rows) % 200 == 0:
                print(t("files_read", n=len(rows)))
    print(t("metadata_done", n=len(rows), s=f"{time.time() - start:.0f}"))

    # 2) SHA-256 only where exact copies are possible (same size)
    by_size = defaultdict(list)
    for row in rows:
        if row["status"] == "OK":
            by_size[row["size_bytes"]].append(row)
    candidates = [r for group in by_size.values() if len(group) > 1 for r in group]
    print(t("hashing", n=len(candidates)))
    for i, row in enumerate(candidates, 1):
        row["sha256"] = sha256_file(root.joinpath(*row["relative_path"].split("/")))
        if i % 100 == 0:
            print(t("hash_progress", i=i, n=len(candidates)))

    # 3) Save the CSV (";" and utf-8-sig so Excel opens it correctly)
    target = out / "inventory.csv"
    with open(target, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, delimiter=";")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in COLUMNS})

    broken = sum(1 for r in rows if r["status"] == "BROKEN")
    truncated = sum(1 for r in rows if r["status"] == "TRUNCATED")
    print(t("inventory_done", path=target))
    print(t("inventory_total", n=len(rows), broken=broken, truncated=truncated,
            s=f"{time.time() - start:.0f}"))


if __name__ == "__main__":
    main()
