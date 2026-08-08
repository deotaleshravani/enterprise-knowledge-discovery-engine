import json
import random
import os
from datetime import datetime, timedelta

from company_data import (
    EMPLOYEE_PROFILES,
    MEETING_TYPES,
    MEETING_DECISIONS_BY_TECHNOLOGY
)

NUM_MEETINGS = 750

meetings = []

# =====================================
# LOAD JIRA
# =====================================

jira_file = os.path.join(
    "..",
    "datasets",
    "jira",
    "jira_tickets.json"
)

with open(
    jira_file,
    "r",
    encoding="utf-8"
) as f:
    jira_tickets = json.load(f)

start_date = datetime(2024, 1, 1)

# =====================================
# GENERATE
# =====================================

for i in range(1, NUM_MEETINGS + 1):

    ticket = random.choice(
        jira_tickets
    )

    team = ticket["team"]

    technology = ticket["technology"]

    team_members = [
        emp
        for emp in EMPLOYEE_PROFILES
        if emp["team"] == team
    ]

    attendees = random.sample(
        team_members,
        min(3, len(team_members))
    )

    meeting_date = start_date + timedelta(
        days=random.randint(0, 700)
    )

    decision_options = (
        MEETING_DECISIONS_BY_TECHNOLOGY.get(
            technology,
            [
                "Continue monitoring the issue.",
                "Perform additional testing.",
                "Schedule a follow-up review."
            ]
        )
    )

    decision = random.choice(
        decision_options
    )

    summary = (
        f"The team discussed "
        f"{ticket['title'].lower()} "
        f"and agreed to "
        f"{decision.lower()}"
    )

    meeting = {

        "meeting_id": f"MTG-{i:04d}",

        "meeting_type": random.choice(
            MEETING_TYPES
        ),

        "project": ticket["project"],

        "team": team,

        "technology": technology,

        "attendees": [
            attendee["name"]
            for attendee in attendees
        ],

        "topic": ticket["title"],

        "decision": decision,

        "summary": summary,

        "related_ticket": ticket[
            "ticket_id"
        ],

        "date": meeting_date.strftime(
            "%Y-%m-%d"
        )
    }

    meetings.append(meeting)

# =====================================
# SAVE
# =====================================

output_dir = os.path.join(
    "..",
    "datasets",
    "meetings"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

output_file = os.path.join(
    output_dir,
    "meeting_notes.json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        meetings,
        f,
        indent=4
    )

print(
    f"Successfully generated "
    f"{NUM_MEETINGS} meeting notes."
)