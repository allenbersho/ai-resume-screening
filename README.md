# AI Resume Screening

AI Resume Screening is an intelligent system that automates the process of screening job applicants’ resumes using Natural Language Processing (NLP) and Machine Learning techniques. The project helps recruiters and HR teams efficiently shortlist candidates by matching resumes against job descriptions and ranking them based on relevance.

---

## 📌 Project Overview

In traditional hiring processes, recruiters manually screen hundreds of resumes, which is time-consuming and error-prone. This project aims to reduce that effort by using AI techniques to automatically analyze resumes and identify the most suitable candidates.

The system extracts text from resumes, processes it using NLP techniques, compares it with job descriptions, and produces similarity scores to rank candidates effectively.

---

## 🚀 Features

- Automated resume text extraction and preprocessing  
- Job description and resume similarity matching  
- Candidate ranking based on relevance score  
- Modular project structure for scalability  
- Sample resumes and job descriptions included for testing  

---

## 📂 Project Structure

ai-resume-screening/
├── api/ # Backend API logic
├── data/
│ └── jobs/ # Job descriptions
├── frontend/ # Frontend UI files
├── samples/ # Sample resumes
├── src/ # Core resume screening logic
├── app.py # Main application file
├── structure.md # Architecture documentation
├── test.py # Testing script
├── requirements.txt # Project dependencies
└── .gitignore

yaml
Copy code

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **NLP Techniques:** TF-IDF, Cosine Similarity  
- **Machine Learning:** scikit-learn  
- **Backend:** Flask / FastAPI  
- **Frontend:** HTML, CSS, JavaScript  

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/allenbersho/ai-resume-screening.git
cd ai-resume-screening
Step 2: Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Usage
Run the Application
bash
Copy code
python app.py
This starts the backend server responsible for resume screening.

Run Tests
bash
Copy code
python test.py
This script tests resume-to-job matching using sample data.

🔄 Workflow
Add resumes to the samples/ folder

Add job descriptions to the data/jobs/ folder

Run the application

The system processes resumes and computes similarity scores

Candidates are ranked based on job relevance

📊 Example
If the job description requires Python, Machine Learning, and SQL, resumes containing similar skills and keywords will receive higher scores and appear at the top of the ranking.

🤝 Contribution
Contributions are welcome. You can improve this project by:

Adding support for more resume formats (PDF, DOCX)

Enhancing NLP accuracy

Building an advanced recruiter dashboard

Integrating deep learning models

📝 License
This project is open-source and available for educational and research purposes.
