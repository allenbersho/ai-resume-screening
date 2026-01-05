import os
from datetime import datetime

import pdfplumber
import docx

from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation
from src.matching.llm_explainer import llm_explanation

# =============================
# CONFIGURATION
# =============================

RESUME_DIR = "data/resumes/"
JOB_PATH = "data/jobs/job1.txt"

# Thresholds
MATCH_THRESHOLD = 60.0          # for binary relevance
AUTO_GT_THRESHOLD = 65.0        # automatic ground truth tagging
PRECISION_K_VALUES = [1, 3, 5]

# =============================
# FILE TEXT EXTRACTION
# =============================

def extract_text_from_file(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    elif file_path.lower().endswith(".txt"):
        return open(file_path, encoding="utf-8").read()

    else:
        raise ValueError(f"Unsupported file format: {file_path}")

# =============================
# METADATA
# =============================

def generate_resume_metadata(file_path):
    return {
        "resume_id": os.path.splitext(os.path.basename(file_path))[0],
        "file_name": os.path.basename(file_path),
        "file_type": os.path.splitext(file_path)[1].replace(".", "").lower(),
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# =============================
# EVALUATION METRICS
# =============================

def compute_binary_metrics(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = (2 * precision * recall) / (precision + recall) if precision + recall else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if tp + tn + fp + fn else 0

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "accuracy": round(accuracy, 3),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn
    }

def precision_at_k(results, k):
    top_k = results[:k]
    relevant_count = sum(1 for r in top_k if r["ground_truth"] == 1)
    return round(relevant_count / k, 3)

# =============================
# MAIN PIPELINE
# =============================

def main():
    job_text = extract_text_from_file(JOB_PATH)
    results = []

    # -------- Resume Processing --------
    for file_name in os.listdir(RESUME_DIR):
        file_path = os.path.join(RESUME_DIR, file_name)

        try:
            resume_text = extract_text_from_file(file_path)
            metadata = generate_resume_metadata(file_path)

            score = compute_similarity(resume_text, job_text)
            score_pct = round(score * 100, 2)

            rule_exp = rule_based_explanation(resume_text, job_text)

            llm_exp = llm_explanation(
                rule_exp["matched_skills"] + rule_exp["missing_skills"],
                rule_exp["matched_skills"]
            )

            # ---- Automatic Ground Truth Tagging ----
            ground_truth = 1 if score_pct >= AUTO_GT_THRESHOLD else 0

            results.append({
                "resume_id": metadata["resume_id"],
                "metadata": metadata,
                "match_score": score_pct,
                "rule_based_explanation": rule_exp,
                "llm_explanation": llm_exp,
                "ground_truth": ground_truth
            })

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    # -------- Ranking --------
    results.sort(key=lambda x: x["match_score"], reverse=True)

    print("\n===== RANKED CANDIDATES =====\n")

    for i, r in enumerate(results, 1):
        print(f"Rank {i}")
        print(f"Resume ID   : {r['resume_id']}")
        print(f"Match Score: {r['match_score']}%")
        print(f"GT Label   : {r['ground_truth']}")
        print(f"Matched    : {r['rule_based_explanation']['matched_skills']}")
        print(f"Missing    : {r['rule_based_explanation']['missing_skills']}")
        print("LLM Explanation:")
        print(r["llm_explanation"])
        print("-" * 60)

    # -------- Binary Evaluation --------
    y_true = [r["ground_truth"] for r in results]
    y_pred = [1 if r["match_score"] >= MATCH_THRESHOLD else 0 for r in results]

    metrics = compute_binary_metrics(y_true, y_pred)

    print("\n===== BINARY EVALUATION =====\n")
    print(f"Precision : {metrics['precision']}")
    print(f"Recall    : {metrics['recall']}")
    print(f"F1 Score  : {metrics['f1']}")
    print(f"Accuracy : {metrics['accuracy']}")
    print(f"TP:{metrics['tp']} FP:{metrics['fp']} FN:{metrics['fn']} TN:{metrics['tn']}")

    # -------- Ranking Evaluation --------
    print("\n===== RANKING METRICS =====\n")
    for k in PRECISION_K_VALUES:
        if len(results) >= k:
            print(f"Precision@{k}: {precision_at_k(results, k)}")

# =============================
# ENTRY POINT
# =============================

if __name__ == "__main__":
    main()
