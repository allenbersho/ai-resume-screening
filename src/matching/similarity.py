from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text, job_text):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])
    score = cosine_similarity(resume_embedding, job_embedding)[0][0]
    return score
