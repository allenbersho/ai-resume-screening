SKILL_ONTOLOGY = {
    "machine learning": [
        "ml",
        "machine learning",
        "supervised learning",
        "unsupervised learning"
    ],
    "deep learning": [
        "deep learning",
        "dl",
        "tensorflow",
        "pytorch",
        "keras",
        "tf"
    ],
    "data analysis": [
        "data analysis",
        "pandas",
        "numpy",
        "data analytics"
    ],
    "natural language processing": [
        "nlp",
        "natural language processing",
        "text mining"
    ],
    "database": [
        "sql",
        "mysql",
        "postgresql",
        "mongodb"
    ],
    "python": [
        "python"
    ],
    "java": [
        "java"
    ]
}

def normalize_skills(skill_list):
    normalized = set()
    lower_skills = [s.lower() for s in skill_list]

    for canonical, variants in SKILL_ONTOLOGY.items():
        for v in variants:
            if v in lower_skills:
                normalized.add(canonical)

    return sorted(list(normalized))
