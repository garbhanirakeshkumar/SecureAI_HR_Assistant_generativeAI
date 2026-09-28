from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_file(file_path):
    """
    Extract text from PDF, DOCX, TXT, or MD files.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    # PDF
    if extension == ".pdf":
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    # DOCX
    elif extension == ".docx":
        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    # TXT
    elif extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    # Markdown
    elif extension == ".md":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF, DOCX, TXT, and MD files are supported."
        )