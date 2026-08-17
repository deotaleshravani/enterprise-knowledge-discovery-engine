import os
import random

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from company_data import (
    ARCHITECTURE_DOCUMENTS,
    SECURITY_DOCUMENTS,
    INCIDENT_DOCUMENTS,
    RUNBOOK_DOCUMENTS,
    API_DOCUMENTS,
    EMPLOYEE_PROFILES,
    PROJECTS,
    DOCUMENT_VERSIONS,
    DOCUMENT_STATUS
)

# =====================================================
# OUTPUT DIRECTORIES
# =====================================================

BASE_DIR = os.path.join(
    "..",
    "datasets",
    "pdfs"
)

ARCH_DIR = os.path.join(BASE_DIR, "architecture")
SECURITY_DIR = os.path.join(BASE_DIR, "security")
INCIDENT_DIR = os.path.join(BASE_DIR, "incidents")
RUNBOOK_DIR = os.path.join(BASE_DIR, "runbooks")
API_DIR = os.path.join(BASE_DIR, "api_docs")

for directory in [
    ARCH_DIR,
    SECURITY_DIR,
    INCIDENT_DIR,
    RUNBOOK_DIR,
    API_DIR
]:
    os.makedirs(directory, exist_ok=True)

styles = getSampleStyleSheet()

# =====================================================
# HELPERS
# =====================================================

def random_intro():

    intros = [

        "This document was prepared by the engineering team to support operational excellence.",

        "This document defines enterprise standards and implementation guidance.",

        "The following information reflects current architectural and operational practices.",

        "This document serves as an internal reference for engineering teams.",

        "The recommendations described here were approved during architecture reviews."
    ]

    return random.choice(intros)


def get_document_metadata():

    author = random.choice(
        EMPLOYEE_PROFILES
    )

    return {

        "author": author["name"],

        "role": author["role"],

        "project": random.choice(
            PROJECTS
        ),

        "version": random.choice(
            DOCUMENT_VERSIONS
        ),

        "status": random.choice(
            DOCUMENT_STATUS
        ),

        "created_date":
            f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    }


def add_metadata(
    content,
    metadata,
    doc_id
):

    content.append(
        Paragraph(
            f"<b>Document ID:</b> {doc_id}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Version:</b> {metadata['version']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Author:</b> {metadata['author']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Role:</b> {metadata['role']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Project:</b> {metadata['project']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Status:</b> {metadata['status']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Created Date:</b> {metadata['created_date']}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

# =====================================================
# ARCHITECTURE PDF
# =====================================================

def generate_architecture_pdf(index):

    data = random.choice(
        ARCHITECTURE_DOCUMENTS
    )

    doc_id = f"ARCH-{index:04d}"

    filename = os.path.join(
        ARCH_DIR,
        f"{doc_id}.pdf"
    )

    metadata = get_document_metadata()

    doc = SimpleDocTemplate(
        filename
    )

    content = []

    content.append(
        Paragraph(
            data["title"],
            styles["Title"]
        )
    )

    add_metadata(
        content,
        metadata,
        doc_id
    )

    content.append(
        Paragraph(
            random_intro(),
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "System Components",
            styles["Heading2"]
        )
    )

    for component in data["components"]:

        content.append(
            Paragraph(
                f"• {component}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Technologies",
            styles["Heading2"]
        )
    )

    for tech in data["technologies"]:

        content.append(
            Paragraph(
                f"• {tech}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    recommendations = random.sample(
        data["recommendations"],
        len(data["recommendations"])
    )

    for recommendation in recommendations:

        content.append(
            Paragraph(
                f"• {recommendation}",
                styles["BodyText"]
            )
        )

    doc.build(content)

# =====================================================
# SECURITY PDF
# =====================================================

def generate_security_pdf(index):

    data = random.choice(
        SECURITY_DOCUMENTS
    )

    doc_id = f"SEC-{index:04d}"

    filename = os.path.join(
        SECURITY_DIR,
        f"{doc_id}.pdf"
    )

    metadata = get_document_metadata()

    doc = SimpleDocTemplate(
        filename
    )

    content = []

    content.append(
        Paragraph(
            data["title"],
            styles["Title"]
        )
    )

    add_metadata(
        content,
        metadata,
        doc_id
    )

    content.append(
        Paragraph(
            "Security Requirements",
            styles["Heading2"]
        )
    )

    requirements = random.sample(
        data["requirements"],
        len(data["requirements"])
    )

    for req in requirements:

        content.append(
            Paragraph(
                f"• {req}",
                styles["BodyText"]
            )
        )

    doc.build(content)

# =====================================================
# INCIDENT PDF
# =====================================================

def generate_incident_pdf(index):

    data = random.choice(
        INCIDENT_DOCUMENTS
    )

    doc_id = f"INC-{index:04d}"

    filename = os.path.join(
        INCIDENT_DIR,
        f"{doc_id}.pdf"
    )

    metadata = get_document_metadata()

    doc = SimpleDocTemplate(
        filename
    )

    content = []

    content.append(
        Paragraph(
            data["title"],
            styles["Title"]
        )
    )

    add_metadata(
        content,
        metadata,
        doc_id
    )

    content.append(
        Paragraph(
            "Impact",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            data["impact"],
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "Root Cause",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            data["root_cause"],
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "Resolution",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            data["resolution"],
            styles["BodyText"]
        )
    )

    doc.build(content)

# =====================================================
# RUNBOOK PDF
# =====================================================

def generate_runbook_pdf(index):

    data = random.choice(
        RUNBOOK_DOCUMENTS
    )

    doc_id = f"RUN-{index:04d}"

    filename = os.path.join(
        RUNBOOK_DIR,
        f"{doc_id}.pdf"
    )

    metadata = get_document_metadata()

    doc = SimpleDocTemplate(
        filename
    )

    content = []

    content.append(
        Paragraph(
            data["title"],
            styles["Title"]
        )
    )

    add_metadata(
        content,
        metadata,
        doc_id
    )

    content.append(
        Paragraph(
            "Procedure",
            styles["Heading2"]
        )
    )

    for step_number, step in enumerate(
        data["steps"],
        start=1
    ):

        content.append(
            Paragraph(
                f"{step_number}. {step}",
                styles["BodyText"]
            )
        )

    doc.build(content)

# =====================================================
# API PDF
# =====================================================

def generate_api_pdf(index):

    data = random.choice(
        API_DOCUMENTS
    )

    doc_id = f"API-{index:04d}"

    filename = os.path.join(
        API_DIR,
        f"{doc_id}.pdf"
    )

    metadata = get_document_metadata()

    doc = SimpleDocTemplate(
        filename
    )

    content = []

    content.append(
        Paragraph(
            data["title"],
            styles["Title"]
        )
    )

    add_metadata(
        content,
        metadata,
        doc_id
    )

    content.append(
        Paragraph(
            "Endpoints",
            styles["Heading2"]
        )
    )

    for endpoint in data["endpoints"]:

        content.append(
            Paragraph(
                endpoint,
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Authentication",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "JWT Bearer Token required for access.",
            styles["BodyText"]
        )
    )

    doc.build(content)

# =====================================================
# GENERATE PDFS
# =====================================================

NUM_PDFS_PER_TYPE = 25

for i in range(1, NUM_PDFS_PER_TYPE + 1):
    generate_architecture_pdf(i)

for i in range(1, NUM_PDFS_PER_TYPE + 1):
    generate_security_pdf(i)

for i in range(1, NUM_PDFS_PER_TYPE + 1):
    generate_incident_pdf(i)

for i in range(1, NUM_PDFS_PER_TYPE + 1):
    generate_runbook_pdf(i)

for i in range(1, NUM_PDFS_PER_TYPE + 1):
    generate_api_pdf(i)

print(
    f"Successfully generated "
    f"{NUM_PDFS_PER_TYPE * 5} PDFs."
)