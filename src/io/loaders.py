import os
from datetime import datetime
import pdfplumber
import docx

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    if file_path.lower().endswith(".txt"):
        return open(file_path, encoding="utf-8").read()

    raise ValueError("Unsupported file type")

def generate_metadata(file_path):
    return {
        "resume_id": os.path.splitext(os.path.basename(file_path))[0],
        "file_name": os.path.basename(file_path),
        "file_type": os.path.splitext(file_path)[1][1:],
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
