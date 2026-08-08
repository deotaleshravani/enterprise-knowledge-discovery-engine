import json
from pathlib import Path


def fetch_meetings():
    dataset_path = (
        Path(__file__).resolve().parents[3]
        / "datasets"
        / "meetings"
        / "meeting_notes.json"
    )

    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)