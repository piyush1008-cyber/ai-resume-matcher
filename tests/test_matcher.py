"""Unit tests for NLP matching, Cosine similarity, and gap analysis."""

from src.matcher import ResumeMatcher


def test_resume_matcher_high_alignment():
    resume = "Python backend developer with 3 years of experience in FastAPI, Docker, and PostgreSQL."
    jd = "Seeking backend engineer with 3+ years experience in Python, FastAPI, Docker, and PostgreSQL."

    matcher = ResumeMatcher()
    result = matcher.match(resume, jd)

    assert result.composite_score_pct >= 75.0
    assert result.skill_coverage_pct == 100.0
    assert len(result.missing_skills) == 0
    assert "python" in result.matched_skills
    assert "fastapi" in result.matched_skills


def test_resume_matcher_skill_gap():
    resume = "Frontend engineer with 2 years experience in React, JavaScript, HTML, CSS."
    jd = "Machine learning engineer with 3 years experience in Python, PyTorch, Scikit-Learn, and Docker."

    matcher = ResumeMatcher()
    result = matcher.match(resume, jd)

    assert result.composite_score_pct < 50.0
    assert len(result.missing_skills) >= 3
    assert any("Upskill in required target skills" in rec for rec in result.recommendations)
