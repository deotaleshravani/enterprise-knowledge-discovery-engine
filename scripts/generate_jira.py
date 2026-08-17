import json
import random
import os
from datetime import datetime, timedelta

from company_data import (
    EMPLOYEE_PROFILES,
    ISSUE_TEMPLATES,
    TEAM_PROJECT_MAPPING
)

NUM_TICKETS = 1000

tickets = []

STATUSES = [
    "Resolved",
    "Closed",
    "Completed"
]

PRIORITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

start_date = datetime(2024, 1, 1)

for i in range(1, NUM_TICKETS + 1):

    # Select a realistic issue template
    template = random.choice(ISSUE_TEMPLATES)

    # Find employees belonging to that team
    team_members = [
        emp
        for emp in EMPLOYEE_PROFILES
        if emp["team"] == template["team"]
    ]

    employee = random.choice(team_members)

    created_date = start_date + timedelta(
        days=random.randint(0, 700)
    )

    updated_date = created_date + timedelta(
        days=random.randint(1, 30)
    )

    ticket = {

        "ticket_id": f"JIRA-{i:04d}",

        # Team determines project
        "project": TEAM_PROJECT_MAPPING[
            template["team"]
        ],

        "team": template["team"],

        "category": template["category"],

        "technology": template["technology"],

        "title": template["problem"],

        "description": (
            f"The team reported a production issue involving "
            f"{template['problem'].lower()}. "
            f"The issue affected systems using "
            f"{template['technology']} and required investigation."
        ),

        "resolution": random.choice(
            template["resolutions"]
        ),

        "status": random.choice(
            STATUSES
        ),

        "priority": random.choice(
            PRIORITIES
        ),

        # Employee information
        "created_by": employee["name"],

        "creator_role": employee["role"],

        "experience_years": employee[
            "experience_years"
        ],

        "created_date": created_date.strftime(
            "%Y-%m-%d"
        ),

        "updated_date": updated_date.strftime(
            "%Y-%m-%d"
        )
    }

    tickets.append(ticket)

# =====================================================
# SAVE FILE
# =====================================================

output_dir = os.path.join(
    "..",
    "datasets",
    "jira"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

output_file = os.path.join(
    output_dir,
    "jira_tickets.json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        tickets,
        f,
        indent=4
    )

print(
    f"Successfully generated "
    f"{NUM_TICKETS} Jira tickets."
)