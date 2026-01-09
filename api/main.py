from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import shutil
import tempfile

import pdfplumber
import docx

from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation
from src.matching.llm_explainer import llm_explanation
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# APP INITIALIZATION (MUST BE AT TOP LEVEL)
# -------------------------------------------------

app = FastAPI(
    title="AI Resume Screening API",
    description="Resume screening with PDF/DOCX upload support",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# FILE TEXT EXTRACTION
# -------------------------------------------------

def extract_text_from_file(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.lower().endswith(".docx"):
        document = docx.Document(file_path)
        return "\n".join(p.text for p in document.paragraphs)

    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file format")

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@app.get("/")
def root():
    return {"message": "AI Resume Screening API is running"}

@app.post("/analyze/upload")
async def analyze_uploaded_files(
    job_file: UploadFile = File(...),
    resumes: List[UploadFile] = File(...)
):
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # -----------------------------
            # SAVE & READ JOB FILE
            # -----------------------------
            job_path = os.path.join(tmpdir, job_file.filename)
            with open(job_path, "wb") as buffer:
                shutil.copyfileobj(job_file.file, buffer)

            job_text = extract_text_from_file(job_path)

            results = []

            # -----------------------------
            # PROCESS RESUMES
            # -----------------------------
            for resume in resumes:
                resume_path = os.path.join(tmpdir, resume.filename)

                with open(resume_path, "wb") as buffer:
                    shutil.copyfileobj(resume.file, buffer)

                resume_text = extract_text_from_file(resume_path)

                # ---- Similarity (FORCE PYTHON FLOAT) ----
                raw_score = compute_similarity(resume_text, job_text)
                score_percent = float(round(float(raw_score) * 100, 2))

                # ---- Rule-based explanation ----
                rule_exp = rule_based_explanation(resume_text, job_text)

                # ---- LLM explanation (FORCE STRING) ----
                llm_exp = str(
                    llm_explanation(
                        rule_exp["matched_skills"] + rule_exp["missing_skills"],
                        rule_exp["matched_skills"]
                    )
                )

                results.append({
                    "resume_id": os.path.splitext(resume.filename)[0],
                    "match_score": score_percent,
                    "matched_skills": rule_exp["matched_skills"],
                    "missing_skills": rule_exp["missing_skills"],
                    "llm_explanation": llm_exp
                })

            # -----------------------------
            # RANK RESULTS
            # -----------------------------
            results.sort(key=lambda x: x["match_score"], reverse=True)

            return {
                "job_file": job_file.filename,
                "ranked_resumes": results
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
