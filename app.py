import os

from src.config.settings import *
from src.io.loaders import extract_text, generate_metadata
from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation
from src.matching.llm_explainer import llm_explanation
from src.evaluation.metrics import binary_metrics, precision_at_k
from src.io.section_extractor import extract_resume_sections
from src.matching.similarity import compute_sectionwise_similarity




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

    rule_exp = rule_based_explanation(
        resume_sections["skills"],
        job_text
    )

    llm_exp = llm_explanation(
        rule_exp["matched_skills"],
        rule_exp["missing_skills"]
    )

    ground_truth = 1 if score >= AUTO_GT_THRESHOLD else 0

    results.append({
        "resume_id": metadata["resume_id"],
        "score": score,
        "section_scores": section_scores,
        "ground_truth": ground_truth,
        "rule_exp": rule_exp,
        "llm_exp": llm_exp
    })


    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n================ RANKED RESUMES ================\n")

    for rank, r in enumerate(results, start=1):
        print(f"Rank {rank}")
        print(f"Resume ID    : {r['resume_id']}")
        print(f"Match Score : {r['score']}%")
        print(f"GT Label    : {r['ground_truth']}")
        print(f"Matched     : {r['rule_exp']['matched_skills']}")
        print(f"Missing     : {r['rule_exp']['missing_skills']}")
        print("Explanation :")
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
