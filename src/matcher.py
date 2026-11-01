"""NLP matching engine utilizing TF-IDF, Cosine Similarity, and Skill Gap Analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.extractor import extract_profile_metadata, extract_skills, extract_years_experience


@dataclass
class MatchResult:
    """Represents candidate-to-job matching scores and gap analysis."""
    composite_score_pct: float
    skill_coverage_pct: float
    semantic_similarity_pct: float
    experience_score_pct: float
    candidate_experience: float
    required_experience: float
    matched_skills: List[str]
    missing_skills: List[str]
    candidate_extra_skills: List[str]
    recommendations: List[str]


class ResumeMatcher:
    """Matches resumes against job descriptions and conducts skill gap analysis."""

    def __init__(
        self,
        skill_weight: float = 0.45,
        semantic_weight: float = 0.35,
        exp_weight: float = 0.20,
    ):
        self.skill_weight = skill_weight
        self.semantic_weight = semantic_weight
        self.exp_weight = exp_weight

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )

    def calculate_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """Computes TF-IDF Cosine Similarity between candidate text and job description."""
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, jd_text])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(sim)
        except Exception:
            return 0.0

    def match(self, resume_text: str, jd_text: str) -> MatchResult:
        """Executes full resume matching and gap analysis pipeline."""
        # 1. Extract Skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        matched_skills = sorted(list(resume_skills & jd_skills))
        missing_skills = sorted(list(jd_skills - resume_skills))
        extra_skills = sorted(list(resume_skills - jd_skills))

        skill_coverage = len(matched_skills) / max(1, len(jd_skills))

        # 2. Semantic Similarity
        semantic_sim = self.calculate_semantic_similarity(resume_text, jd_text)

        # 3. Experience Match
        cand_exp = extract_years_experience(resume_text)
        req_exp = extract_years_experience(jd_text)

        if req_exp > 0:
            exp_score = min(1.0, cand_exp / req_exp)
        else:
            exp_score = 1.0

        # 4. Composite Score
        composite = (
            (skill_coverage * self.skill_weight)
            + (semantic_sim * self.semantic_weight)
            + (exp_score * self.exp_weight)
        )

        # 5. Recommendations
        recommendations = []
        if missing_skills:
            top_missing = missing_skills[:5]
            recommendations.append(
                f"Upskill in required target skills: {', '.join(top_missing)}."
            )
        if req_exp > cand_exp and req_exp > 0:
            recommendations.append(
                f"Highlight production project impact to offset experience gap ({cand_exp} yrs vs {req_exp} yrs requested)."
            )
        if semantic_sim < 0.25:
            recommendations.append(
                "Incorporate more industry-standard technical phrasing and action verbs from the job description."
            )

        if not recommendations:
            recommendations.append("Excellent match! Candidate profile strongly aligns with the target role.")

        return MatchResult(
            composite_score_pct=round(composite * 100, 2),
            skill_coverage_pct=round(skill_coverage * 100, 2),
            semantic_similarity_pct=round(semantic_sim * 100, 2),
            experience_score_pct=round(exp_score * 100, 2),
            candidate_experience=cand_exp,
            required_experience=req_exp,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            candidate_extra_skills=extra_skills,
            recommendations=recommendations,
        )
