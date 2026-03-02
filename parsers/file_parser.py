"""Parse PDF, DOCX, and TXT files to extract text content."""

import os
from PyPDF2 import PdfReader
from docx import Document


def parse_file(file_path: str) -> str:
    """Extract text from a file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _parse_pdf(file_path)
    elif ext == ".docx":
        return _parse_docx(file_path)
    elif ext == ".txt":
        return _parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)


def _parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())


def _parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
