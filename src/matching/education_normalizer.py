EDUCATION_LEVELS = {
    "doctorate": [
        "phd",
        "doctorate"
    ],
    "master": [
        "mtech",
        "m.tech",
        "msc",
        "ms",
        "mba",
        "masters",
        "master"
    ],
    "bachelor": [
        "btech",
        "b.tech",
        "be",
        "b.e",
        "bsc",
        "bachelor"
    ],
    "diploma": [
        "diploma"
    ]
}

def normalize_education(education_text):
    text = education_text.lower()

    for level, keywords in EDUCATION_LEVELS.items():
        for k in keywords:
            if k in text:
                return level

    return "unknown"
