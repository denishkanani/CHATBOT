import csv
import json
import os
import zipfile
from pathlib import Path


def _read_text_file(path):
    try:
        return Path(path).read_text(encoding="utf-8"), {"file_type": "text"}
    except Exception:
        return "", {"file_type": "text"}


def _read_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return json.dumps(data, indent=2), {"file_type": "json"}
    except Exception:
        return "", {"file_type": "json"}


def _read_csv_file(path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        return "\n".join([",".join(row) for row in rows]), {"file_type": "csv"}
    except Exception:
        return "", {"file_type": "csv"}


def _read_zip_file(path):
    try:
        with zipfile.ZipFile(path) as archive:
            parts = []
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                content = archive.read(name).decode("utf-8", errors="ignore")
                parts.append(f"[{name}]\n{content}")
        return "\n\n".join(parts), {"file_type": "zip"}
    except Exception:
        return "", {"file_type": "zip"}


def extract_text_from_file(path, filename=None):
    filename = (filename or path).lower()
    if filename.endswith(".json"):
        return _read_json_file(path)
    if filename.endswith(".csv"):
        return _read_csv_file(path)
    if filename.endswith(".zip"):
        return _read_zip_file(path)
    if filename.endswith((".txt", ".md", ".log")):
        return _read_text_file(path)
    if filename.endswith((".docx", ".doc", ".pdf", ".ppt", ".pptx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".mp3", ".mp4", ".wav", ".webm", ".mov")):
        return "", {"file_type": "binary", "supported": False}
    return _read_text_file(path)
