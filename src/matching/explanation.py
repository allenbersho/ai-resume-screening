def extract_skills(text):
    skills = [
        "python", "java", "machine learning", "ml", "nlp",
        "deep learning", "sql", "spring",
        "tensorflow", "docker", "kubernetes"
    ]
    text = text.lower()
    return {s for s in skills if s in text}

def rule_based_explanation(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    return {
        "matched_skills": sorted(list(resume_skills & job_skills)),
        "missing_skills": sorted(list(job_skills - resume_skills))
    }
