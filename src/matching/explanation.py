def extract_skills(text):
    skills = [
        "python", "java", "machine learning", "ml", "nlp",
        "deep learning", "sql", "spring", "data analysis",
        "tensorflow", "pandas", "docker", "kubernetes"
    ]
    text_lower = text.lower()
    return {skill for skill in skills if skill in text_lower}

def rule_based_explanation(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    explanation = {
        "matched_skills": list(matched),
        "missing_skills": list(missing)
    }

    return explanation
