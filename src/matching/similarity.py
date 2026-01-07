from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0

    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    return cosine_similarity(emb1, emb2)[0][0]


def compute_sectionwise_similarity(resume_sections, job_text):
    skill_score = compute_similarity(
        resume_sections.get("skills", ""),
        job_text
    )

    experience_score = compute_similarity(
        resume_sections.get("experience", ""),
        job_text
    )

    education_score = compute_similarity(
        resume_sections.get("education", ""),
        job_text
    )

    final_score = (
        0.4 * skill_score +
        0.4 * experience_score +
        0.2 * education_score
    )

    return {
        "skills_similarity": round(skill_score * 100, 2),
        "experience_similarity": round(experience_score * 100, 2),
        "education_similarity": round(education_score * 100, 2),
        "final_score": round(final_score * 100, 2)
    }
