from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation, extract_skills
from src.matching.llm_explainer import llm_explanation
import pdfplumber
import docx
import os 

def extract_text_from_file(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_path.lower().endswith(".txt"):
        return open(file_path, encoding="utf-8").read()

    else:
        raise ValueError(f"Unsupported file format: {file_path}")

resume_dir = "data/resumes/"
results = []

job_path = "data/jobs/job1.txt"
job_text = extract_text_from_file(job_path)


for file_name in os.listdir(resume_dir):
    file_path = os.path.join(resume_dir, file_name)

    try:
        resume_text = extract_text_from_file(file_path)

        score = compute_similarity(resume_text, job_text)

        rule_exp = rule_based_explanation(resume_text, job_text)

        llm_exp = llm_explanation(
            rule_exp["matched_skills"] + rule_exp["missing_skills"],
            rule_exp["matched_skills"]
        )

        results.append({
            "resume_file": file_name,
            "match_score": round(score * 100, 2),
            "rule_based_explanation": rule_exp,
            "llm_explanation": llm_exp
        })

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

results.sort(key=lambda x: x["match_score"], reverse=True)

print("\n===== RANKED CANDIDATES =====\n")

for rank, res in enumerate(results, start=1):
    print(f"Rank {rank}: {res['resume_file']}")
    print(f"Match Score: {res['match_score']}%")
    print(f"Matched Skills: {res['rule_based_explanation']['matched_skills']}")
    print(f"Missing Skills: {res['rule_based_explanation']['missing_skills']}")
    print("LLM Explanation:")
    print(res["llm_explanation"])
    print("-" * 50)

