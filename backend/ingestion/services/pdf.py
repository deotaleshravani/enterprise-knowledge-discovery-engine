import pdfplumber
from pathlib import Path


def fetch_pdfs():
    pdf_root = (
        Path(__file__).resolve().parents[3]
        / "datasets"
        / "pdfs"
    )

    documents = []

    pdf_files = pdf_root.rglob("*.pdf")

    for pdf_file in pdf_files:
        text = ""

        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            documents.append({
                "id": pdf_file.stem,
                "source_folder": pdf_file.parent.name,
                "text": text
            })

        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

    return documents