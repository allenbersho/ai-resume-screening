from src.matching.similarity import compute_similarity
from src.matching.explanation import rule_based_explanation, extract_skills
from src.matching.llm_explainer import llm_explanation
import pdfplumber
import docx
import os 
from datetime import datetime

# Function to generate metadata about the file
def generate_resume_metadata(file_path):
    return {
        "resume_id": os.path.splitext(os.path.basename(file_path))[0],
        "file_name": os.path.basename(file_path),
        "file_type": os.path.splitext(file_path)[1].replace(".", "").lower(),
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Function to handle different file types
def extract_text_from_file(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file format: {file_path}")

# Configuration
resume_dir = "data/resumes/"
job_path = "data/jobs/job1.txt"
results = []

# Load Job Description once
job_text = extract_text_from_file(job_path)

# Process each resume in the directory
for file_name in os.listdir(resume_dir):
    file_path = os.path.join(resume_dir, file_name)

    try:
        resume_text = extract_text_from_file(file_path)
        
        # 1. Generate the metadata
        metadata = generate_resume_metadata(file_path)

        # 2. Run AI Analysis
        score = compute_similarity(resume_text, job_text)
        rule_exp = rule_based_explanation(resume_text, job_text)
        llm_exp = llm_explanation(
            rule_exp["matched_skills"] + rule_exp["missing_skills"],
            rule_exp["matched_skills"]
        )

        # 3. Store EVERYTHING in the results list (FIXED: added metadata)
        results.append({
            "resume_file": file_name,
            "metadata": metadata,  # Storing the metadata dictionary here
            "match_score": round(score * 100, 2),
            "rule_based_explanation": rule_exp,
            "llm_explanation": llm_exp
        })

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Rank results by score
results.sort(key=lambda x: x["match_score"], reverse=True)

# Print Results
print("\n===== RANKED CANDIDATES WITH METADATA =====\n")

for rank, res in enumerate(results, start=1):
    # FIXED: Accessing nested metadata keys correctly
    meta = res['metadata']
    
    print(f"Rank {rank}")
    print(f"Resume ID: {meta['resume_id']}")
    print(f"File Name: {meta['file_name']}")
    print(f"File Type: {meta['file_type']}")
    print(f"File Size: {meta['file_size_kb']} KB")
    print(f"Processed At: {meta['processed_at']}")
    print(f"Match Score: {res['match_score']}%")
    print(f"Matched Skills: {res['rule_based_explanation']['matched_skills']}")
    print(f"Missing Skills: {res['rule_based_explanation']['missing_skills']}")
    print("LLM Explanation:")
    print(res["llm_explanation"])
    print("-" * 60)