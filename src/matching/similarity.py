from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text, job_text):
    resume_emb = model.encode([resume_text])
    job_emb = model.encode([job_text])
    return cosine_similarity(resume_emb, job_emb)[0][0]
