import json
from pathlib import Path


def fetch_jira():
    dataset_path = (
        Path(__file__).resolve().parents[3]
        / "datasets"
        / "jira"
        / "jira_tickets.json"
    )

    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)