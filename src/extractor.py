"""Text extraction module for identifying skills, experience, and education."""

from __future__ import annotations

import re
from typing import Dict, List, Set
from src.taxonomy import SKILL_TAXONOMY


EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
EXP_REGEX = re.compile(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience", re.IGNORECASE)

EDUCATION_KEYWORDS = [
    "b.tech", "btech", "b.e", "bachelor of technology", "bachelor of engineering",
    "m.tech", "mtech", "m.s", "master of science", "b.s", "ph.d", "phd",
    "computer science", "information technology", "data science"
]


def extract_skills(text: str) -> Set[str]:
    """Scans text against skill taxonomy using word boundary matching."""
    text_lower = text.lower()
    found_skills = set()

    for canonical, variants in SKILL_TAXONOMY.items():
        for variant in variants:
            # Word boundary regex with special char escaping
            pattern = r"(?<!\w)" + re.escape(variant) + r"(?!\w)"
            if re.search(pattern, text_lower):
                found_skills.add(canonical)
                break

    return found_skills


def extract_years_experience(text: str) -> float:
    """Estimates years of experience stated in text."""
    matches = EXP_REGEX.findall(text)
    if matches:
        return max(float(m) for m in matches)
    return 0.0


def extract_education(text: str) -> List[str]:
    """Finds referenced education degrees and fields of study."""
    text_lower = text.lower()
    found = []
    for edu in EDUCATION_KEYWORDS:
        if edu in text_lower:
            found.append(edu.upper())
    return sorted(list(set(found)))


def extract_profile_metadata(text: str) -> Dict:
    """Extracts high-level candidate or job profile metadata."""
    emails = EMAIL_REGEX.findall(text)
    phones = PHONE_REGEX.findall(text)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "years_experience": extract_years_experience(text),
        "education": extract_education(text),
        "skills": sorted(list(extract_skills(text))),
    }
