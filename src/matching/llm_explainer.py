import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

client = Groq(api_key=GROQ_API_KEY)

def llm_explanation(resume_skills, job_skills):
    prompt = f"""
You are an AI assistant used in an automated resume screening system.

Resume skills :{resume_skills}

Job required skills :{job_skills}

Rules:
- Do NOT invent skills.
- Do NOT estimate experience.
- Do NOT change any match score.
- Only reason using the given skills.

Tasks:
1. Normalize skill names to standard industry terms.
2. Explain why the candidate matches or does not match the job.
3. List missing skills clearly.
4. Suggest improvements concisely.

Return output strictly in this format:
Normalized Resume Skills:
Normalized Job Skills:
Explanation:
Skill Gaps:
Suggestions:
Make sure to follow the format exactly and do not add any extra information. Add the detail in brief yet comprehensive manner.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict resume screening assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )

    return response.choices[0].message.content
