from fastapi import FastAPI
from pydantic import BaseModel

from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation
from src.matching.llm_explainer import llm_explanation

from typing import List
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="AI Resume Screening & Job Matching API",
    description="Hybrid AI system using embeddings + LLM explainability",
    version="1.0"
)



class ResumeItem(BaseModel):
    candidate_id: str
    resume_text: str

class BatchMatchRequest(BaseModel):
    job_text: str
    resumes: List[ResumeItem]

class CandidateResult(BaseModel):
    candidate_id: str
    match_score: float
    rule_based_explanation: dict
    llm_explanation: str

class BatchMatchResponse(BaseModel):
    ranked_candidates: List[CandidateResult]

class MatchRequest(BaseModel):
    resume_text: str
    job_text: str

class MatchResponse(BaseModel):
    match_score: float
    rule_based_explanation: dict
    llm_explanation: str

@app.post("/match", response_model=MatchResponse)
def match_resume_to_job(request: MatchRequest):
    resume_text = request.resume_text
    job_text = request.job_text

    score = compute_similarity(resume_text, job_text)

    rule_exp = rule_based_explanation(resume_text, job_text)

    llm_exp = llm_explanation(
        rule_exp["matched_skills"] + rule_exp["missing_skills"],
        rule_exp["matched_skills"]
    )

    return {
        "match_score": round(score * 100, 2),
        "rule_based_explanation": rule_exp,
        "llm_explanation": llm_exp
    }
    
@app.post("/match/batch", response_model=BatchMatchResponse)
def batch_match_resumes(request: BatchMatchRequest):
    job_text = request.job_text
    results = []

    for resume in request.resumes:
        score = compute_similarity(resume.resume_text, job_text)

        rule_exp = rule_based_explanation(resume.resume_text, job_text)

        llm_exp = llm_explanation(
            rule_exp["matched_skills"] + rule_exp["missing_skills"],
            rule_exp["matched_skills"]
        )

        results.append({
            "candidate_id": resume.candidate_id,
            "match_score": round(score * 100, 2),
            "rule_based_explanation": rule_exp,
            "llm_explanation": llm_exp
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return {"ranked_candidates": results}

