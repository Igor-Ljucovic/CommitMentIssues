from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text_from_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(paragraphs).strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PdfReader(BytesIO(file_bytes))
    pages_text: list[str] = []

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            pages_text.append(extracted)

    return "\n".join(pages_text).strip()


def extract_text_by_extension(file_name: str, file_bytes: bytes) -> str:
    lower_name = file_name.lower()

    if lower_name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)

    if lower_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    raise ValueError(f"Unsupported file type: {file_name}")