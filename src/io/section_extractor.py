import re

SECTION_HEADERS = {
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "skill set",
        "technologies"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "industry experience"
    ],
    "education": [
        "education",
        "academic background",
        "educational qualifications",
        "qualifications"
    ]
}

def normalize_line(line):
    line = line.lower()
    line = re.sub(r"[^a-z0-9\s]", "", line)
    return line.strip()

def detect_section_header(line):
    for section, headers in SECTION_HEADERS.items():
        for header in headers:
            if line == header:
                return section
    return None

def extract_resume_sections(resume_text):
    sections = {
        "skills": [],
        "experience": [],
        "education": []
    }

    current_section = None

    lines = resume_text.splitlines()

    for raw_line in lines:
        line = normalize_line(raw_line)

        if not line:
            continue

        detected_section = detect_section_header(line)

        if detected_section:
            current_section = detected_section
            continue

        if current_section:
            sections[current_section].append(raw_line.strip())

    for key in sections:
        sections[key] = "\n".join(sections[key]).strip()

    return sections
