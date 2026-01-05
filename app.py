from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation, extract_skills
from src.matching.llm_explainer import llm_explanation

resume_text = open("data/resumes/resume1.txt").read()
job_text = open("data/jobs/job1.txt").read()

score = compute_similarity(resume_text, job_text)

rule_exp = rule_based_explanation(resume_text, job_text)

llm_exp = llm_explanation(
    rule_exp["matched_skills"] + rule_exp["missing_skills"],
    rule_exp["matched_skills"]
)

print("Match Score:", score, "%")
print("Rule-Based Explanation:", rule_exp)
print("LLM Explanation:", llm_exp)
