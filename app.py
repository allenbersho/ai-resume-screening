import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_skills(text):
    keywords = [
        "python", "java", "machine learning", "ml", "nlp",
        "deep learning", "sql", "spring", "data analysis",
        "tensorflow", "pandas"
    ]
    text_lower = text.lower()
    return {kw for kw in keywords if kw in text_lower}

def generate_explanation(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    explanation = "Matched Skills: "
    explanation += ", ".join(matched) if matched else "None"

    if missing:
        explanation += " | Missing Skills: " + ", ".join(missing)

    return explanation


resume_dir = "data/resumes/"
job_text = read_text("data/jobs/job1.txt")

model = SentenceTransformer("all-MiniLM-L6-v2")

job_embedding = model.encode([job_text])

results = []

for file_name in os.listdir(resume_dir):
    file_path = os.path.join(resume_dir, file_name)
    resume_text = read_text(file_path)

    resume_embedding = model.encode([resume_text])
    score = cosine_similarity(resume_embedding, job_embedding)[0][0]

    explanation = generate_explanation(resume_text, job_text)

    results.append((file_name, score, explanation))

results.sort(key=lambda x: x[1], reverse=True)

print("\nRanked Candidates with Explanation:\n")
for rank, (name, score, explanation) in enumerate(results, start=1):
    score *= 100
    print(f"{rank}. {name}")
    print(f"   Match Score: {score:.2f}%")
    print(f"   Reason: {explanation}\n")
