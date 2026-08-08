import json
from pathlib import Path


def fetch_slack():
    dataset_path = (
        Path(__file__).resolve().parents[3]
        / "datasets"
        / "slack"
        / "slack_messages.json"
    )

    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)