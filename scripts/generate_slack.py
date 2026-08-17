import json
import random
import os
from datetime import datetime, timedelta

from company_data import (
    EMPLOYEE_PROFILES,
    TEAM_PROJECT_MAPPING,
    SLACK_MESSAGE_TEMPLATES
)

NUM_MESSAGES = 2000

messages = []

# ==========================================
# LOAD JIRA TICKETS
# ==========================================

jira_file = os.path.join(
    "..",
    "datasets",
    "jira",
    "jira_tickets.json"
)

with open(jira_file, "r", encoding="utf-8") as f:
    jira_tickets = json.load(f)

# ==========================================
# TIMESTAMP RANGE
# ==========================================

start_date = datetime(2024, 1, 1)

# ==========================================
# GENERATE MESSAGES
# ==========================================

for i in range(1, NUM_MESSAGES + 1):

    ticket = random.choice(jira_tickets)

    team = ticket["team"]

    team_members = [
        emp
        for emp in EMPLOYEE_PROFILES
        if emp["team"] == team
    ]

    employee = random.choice(team_members)

    template = random.choice(
        SLACK_MESSAGE_TEMPLATES
    )

    issue_name = ticket["title"]

    message_text = template.format(
        issue=issue_name.lower()
    )

    timestamp = start_date + timedelta(
        days=random.randint(0, 700),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    channel = (
        team.lower()
        .replace(" ", "-")
    )

    message = {

        "message_id": f"SLK-{i:05d}",

        "channel": channel,

        "user": employee["name"],

        "role": employee["role"],

        "team": employee["team"],

        "project": employee["project"],

        "message": message_text,

        "related_ticket": ticket[
            "ticket_id"
        ],

        "technology": ticket[
            "technology"
        ],

        "timestamp": timestamp.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    messages.append(message)

# ==========================================
# SAVE FILE
# ==========================================

output_dir = os.path.join(
    "..",
    "datasets",
    "slack"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

output_file = os.path.join(
    output_dir,
    "slack_messages.json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        messages,
        f,
        indent=4
    )

print(
    f"Successfully generated "
    f"{NUM_MESSAGES} Slack messages."
)