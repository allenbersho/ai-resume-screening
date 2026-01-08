import re

def estimate_experience_level(experience_text):
    text = experience_text.lower()

    year_matches = re.findall(r"(\d+)\+?\s*(years|yrs)", text)

    if not year_matches:
        return "unknown"

    max_years = max(int(y[0]) for y in year_matches)

    if max_years < 2:
        return "junior"
    elif max_years < 5:
        return "mid"
    else:
        return "senior"
