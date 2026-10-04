import pymupdf
import re


def extract_text_from_pdf(pdf_bytes):
    """Extract readable text from an uploaded PDF."""

    document = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages


def create_chunks(pages):
    """Split extracted PDF text into useful contract sections."""

    chunks = []

    for page in pages:
        text = page["text"]

        sections = re.split(r"\n(?=\d+\.\s)", text)

        for section in sections:
            section = section.strip()

            if section:
                chunks.append({
                    "page": page["page"],
                    "text": section
                })

    return chunks