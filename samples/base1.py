from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

resume_text = read_text("data/resumes/resume1.txt")
job_text = read_text("data/jobs/job1.txt")

model = SentenceTransformer("all-MiniLM-L6-v2")

resume_embedding = model.encode([resume_text])
job_embedding = model.encode([job_text])

similarity_score = cosine_similarity(resume_embedding, job_embedding)[0][0]

print(f"Resume–Job Match Score: {similarity_score:.4f}")