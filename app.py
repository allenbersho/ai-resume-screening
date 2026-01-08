import os

from src.config.settings import *
from src.io.loaders import extract_text, generate_metadata
from src.io.section_extractor import extract_resume_sections

from src.matching.similarity import compute_sectionwise_similarity
from src.matching.explanation import rule_based_explanation
from src.matching.skill_normalizer import normalize_skills
from src.matching.education_normalizer import normalize_education
from src.matching.experience_estimator import estimate_experience_level
from src.matching.llm_explainer import llm_explanation

from src.evaluation.metrics import binary_metrics, precision_at_k


def main():
    job_text = extract_text(JOB_PATH)
    results = []

    for file in os.listdir(RESUME_DIR):
        path = os.path.join(RESUME_DIR, file)

        resume_text = extract_text(path)
        resume_sections = extract_resume_sections(resume_text)
        metadata = generate_metadata(path)

        section_scores = compute_sectionwise_similarity(
            resume_sections,
            job_text
        )

        score = section_scores["final_score"]

        education_level = normalize_education(
            resume_sections["education"]
        )

        experience_level = estimate_experience_level(
            resume_sections["experience"]
        )

        if experience_level == "senior":
            score += 3
        elif experience_level == "mid":
            score += 1

        if education_level == "master":
            score += 2
        elif education_level == "doctorate":
            score += 3

        score = min(score, 100.0)

        rule_exp = rule_based_explanation(
            resume_sections["skills"],
            job_text
        )

        normalized_resume_skills = normalize_skills(
            rule_exp["matched_skills"]
        )

        normalized_missing_skills = normalize_skills(
            rule_exp["missing_skills"]
        )

        llm_exp = llm_explanation(
            normalized_resume_skills,
            normalized_missing_skills
        )

        ground_truth = 1 if score >= AUTO_GT_THRESHOLD else 0

        results.append({
            "resume_id": metadata["resume_id"],
            "score": score,
            "section_scores": section_scores,
            "education_level": education_level,
            "experience_level": experience_level,
            "ground_truth": ground_truth,
            "rule_exp": rule_exp,
            "llm_exp": llm_exp
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n================ RANKED RESUMES ================\n")

    for rank, r in enumerate(results, start=1):
        print(f"Rank {rank}")
        print(f"Resume ID        : {r['resume_id']}")
        print(f"Final Score     : {r['score']}%")
        print(f"Education Level : {r['education_level']}")
        print(f"Experience Level: {r['experience_level']}")
        print(f"Matched Skills  : {r['rule_exp']['matched_skills']}")
        print(f"Missing Skills  : {r['rule_exp']['missing_skills']}")
        print("Explanation:")
        print(r["llm_exp"])
        print("-" * 60)

    y_true = [r["ground_truth"] for r in results]
    y_pred = [1 if r["score"] >= MATCH_THRESHOLD else 0 for r in results]

    precision, recall, f1, accuracy = binary_metrics(y_true, y_pred)

    print("\n================ BINARY METRICS ================\n")
    print("Precision :", round(precision, 3))
    print("Recall    :", round(recall, 3))
    print("F1 Score  :", round(f1, 3))
    print("Accuracy  :", round(accuracy, 3))

    print("\n================ RANKING METRICS ================\n")
    for k in PRECISION_K_VALUES:
        if len(results) >= k:
            print(f"Precision@{k} :", round(precision_at_k(results, k), 3))


if __name__ == "__main__":
    main()
