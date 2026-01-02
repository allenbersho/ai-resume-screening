import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

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
    results.append((file_name, score))

results.sort(key=lambda x: x[1], reverse=True)

print("Ranked Candidates:")
for rank, (name, score) in enumerate(results, start=1):
    score *= 100
    print(f"{rank}. {name} → Match Score: {score:.2f}%")
