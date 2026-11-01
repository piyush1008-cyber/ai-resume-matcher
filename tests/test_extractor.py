"""Unit tests for resume skill extraction and metadata parsing."""

from src.extractor import extract_education, extract_profile_metadata, extract_skills, extract_years_experience


def test_extract_skills():
    sample_text = "Proficient in Python, C++, Docker, FastAPI, and PostgreSQL with Redis caching."
    skills = extract_skills(sample_text)

    assert "python" in skills
    assert "c++" in skills
    assert "docker" in skills
    assert "fastapi" in skills
    assert "postgresql" in skills
    assert "redis" in skills
    assert "rust" not in skills


def test_extract_years_experience():
    text1 = "Senior engineer with 5 years of experience building microservices."
    text2 = "Looking for candidate with 3+ yrs experience."
    text3 = "Fresh graduate with enthusiasm."

    assert extract_years_experience(text1) == 5.0
    assert extract_years_experience(text2) == 3.0
    assert extract_years_experience(text3) == 0.0


def test_extract_metadata():
    text = """
    Piyush Kangle
    Email: test@example.com
    Phone: (555) 123-4567
    Education: B.Tech in Computer Science
    5 years of experience in Python and AWS.
    """
    meta = extract_profile_metadata(text)
    assert meta["email"] == "test@example.com"
    assert meta["years_experience"] == 5.0
    assert "B.TECH" in meta["education"]
    assert "python" in meta["skills"]
    assert "aws" in meta["skills"]
