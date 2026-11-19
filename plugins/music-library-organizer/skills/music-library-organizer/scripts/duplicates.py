"""
PHASE 2 - Duplicate detection (READ ONLY: works on inventory.csv).

Usage:
    python duplicates.py "D:\\Music" [--lang en|es|nl]

Writes next to inventory.csv:
    tracks.csv         -> one row per track: chosen copy + which playlists it was in
    files.csv          -> one row per file: KEEP / EXTRA / BROKEN / TRUNCATED
    to_redownload.csv  -> broken downloads with no good copy anywhere
"""
import csv
import re
import unicodedata
from collections import defaultdict

from common import output_dir, parser
from i18n import t

# Letters that are NOT "letter + accent", so NFKD does not split them: map by hand
SPECIAL_LETTERS = str.maketrans({"ø": "o", "æ": "ae", "œ": "oe", "ß": "ss",
                                 "đ": "d", "ł": "l", "þ": "th", "ı": "i"})

CODEC_QUALITY = {"wav": 3, "flac": 3, "alac": 3, "mp3": 1, "mp4a.40.2": 1}


def name_key(file: str) -> str:
    """'149 - Rødhåd - Patient Zero (Original Mix).flac' -> 'rodhadpatientzero'"""
    base = re.sub(r"\.[a-z0-9]+$", "", file.lower())                   # drop extension
    base = re.sub(r"^\s*\d+\s*[.\-_]\s*", "", base)                     # drop track number
    base = re.sub(r"\((explicit|original mix|original|original version)\)", "", base)
    base = base.translate(SPECIAL_LETTERS)                             # ø -> o, ß -> ss
    base = unicodedata.normalize("NFKD", base)                         # å -> a + °, ä -> a + ¨
    base = "".join(c for c in base if not unicodedata.combining(c))    # drop the ¨ ´ ...
    return re.sub(r"[^a-z0-9]", "", base)                              # letters and digits only


class UnionFind:
    """Groups items that are connected, even indirectly."""

    def __init__(self, n):
        self.parent = list(range(n))

    def root(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.root(a)] = self.root(b)


def num(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def main():
    out = output_dir(parser("Phase 2: find duplicates (read only).").parse_args().root)
    with open(out / "inventory.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))

    for row in rows:
        # The playlist is the folder that holds the file (subfolders included)
        row["relative_path"] = row["relative_path"].replace("\\", "/")
        row["playlist"] = row["relative_path"].rsplit("/", 1)[0] if "/" in row["relative_path"] else ""
        row["key"] = name_key(row["file"])
        row["quality"] = CODEC_QUALITY.get(row["codec"], 0)

    # 1) Join files that are the same track by ANY of the 3 signals
    good = [i for i, r in enumerate(rows) if r["status"] == "OK"]
    uf = UnionFind(len(rows))
    for field in ("key", "sha256", "flac_audio_md5"):
        first_with_value = {}
        for i in good:
            value = rows[i][field]
            if not value:
                continue
            if value in first_with_value:
                uf.union(i, first_with_value[value])
            else:
                first_with_value[value] = i

    groups = defaultdict(list)
    for i in good:
        groups[uf.root(i)].append(rows[i])

    # 2) In each group, pick the best copy and flag doubtful cases
    tracks = []
    for n, members in enumerate(groups.values(), 1):
        members.sort(key=lambda r: (r["quality"], num(r["real_kbps"]),
                                    bool(r["artist"]), num(r["size_bytes"])),
                     reverse=True)
        chosen = members[0]
        durations = [num(r["duration_s"]) for r in members]
        keys = {r["key"] for r in members}
        reasons = []
        if max(durations) - min(durations) > 3:
            reasons.append(t("reason_duration"))
        if len(keys) > 1:
            reasons.append(t("reason_names"))
        playlists = sorted({r["playlist"] for r in members},
                           key=lambda p: min(r["modified"] for r in members if r["playlist"] == p))
        track_id = f"T{n:04d}"
        for r in members:
            r["track_id"] = track_id
            r["action"] = "KEEP" if r is chosen else "EXTRA"
        tracks.append({
            "track_id": track_id,
            "chosen_file": chosen["relative_path"],
            "codec": chosen["codec"],
            "real_kbps": chosen["real_kbps"],
            "copies": len(members),
            "extra_mb": round(sum(num(r["size_bytes"]) for r in members[1:]) / 1e6, 1),
            "lossy_only": "YES" if chosen["quality"] < 3 else "",
            "doubtful": "; ".join(reasons),
            "playlist_count": len(playlists),
            "playlists_in_order": " -> ".join(playlists),
        })

    # 3) Broken files: is there a good copy of that track somewhere else?
    key_to_id = {r["key"]: r["track_id"] for r in rows if r.get("track_id")}
    for r in rows:
        if r["status"] != "OK":
            r["action"] = r["status"]
            r["track_id"] = key_to_id.get(r["key"], "")

    track_cols = ["track_id", "chosen_file", "codec", "real_kbps", "copies", "extra_mb",
                  "lossy_only", "doubtful", "playlist_count", "playlists_in_order"]
    with open(out / "tracks.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=track_cols, delimiter=";")
        w.writeheader()
        w.writerows(tracks)
    file_cols = ["track_id", "action", "playlist", "file", "codec", "real_kbps",
                 "duration_s", "size_bytes", "relative_path"]
    with open(out / "files.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=file_cols, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # Broken with NO good copy anywhere = must be downloaded again
    redownload = [r for r in rows if r["status"] != "OK" and not r["track_id"]]
    with open(out / "to_redownload.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["playlist", "file", "status"], delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(redownload)

    extras = [r for r in rows if r.get("action") == "EXTRA"]
    print(t("to_redownload", n=len(redownload)))
    print(t("unique_tracks", n=len(tracks)))
    print(t("extra_files", n=len(extras),
            gb=f"{sum(num(r['size_bytes']) for r in extras) / 1e9:.1f}"))
    print(t("doubtful", n=sum(1 for c in tracks if c["doubtful"])))
    print(t("lossy_only", n=sum(1 for c in tracks if c["lossy_only"])))


if __name__ == "__main__":
    main()
