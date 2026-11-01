"""Report generator formatting match results into readable console tables and JSON."""

from __future__ import annotations

import json
from src.matcher import MatchResult


def print_match_report(result: MatchResult, resume_name: str = "Candidate Resume", jd_name: str = "Target Job Description") -> None:
    """Prints a structured ASCII report of candidate-job matching analytics."""
    print("\n" + "=" * 70)
    print("                    AI RESUME & JOB MATCH REPORT                  ")
    print("=" * 70)
    print(f"Resume:  {resume_name}")
    print(f"Target:  {jd_name}")
    print("-" * 70)

    # Score Gauge
    score = result.composite_score_pct
    badge = "[EXCELLENT]" if score >= 80 else ("[STRONG]" if score >= 65 else ("[MODERATE]" if score >= 45 else "[LOW]"))
    print(f"Overall Fit Score:       {score}% {badge}")
    print(f"  |-- Skill Overlap:      {result.skill_coverage_pct}%")
    print(f"  |-- Semantic Sim (NLP): {result.semantic_similarity_pct}%")
    print(f"  +-- Experience Match:   {result.experience_score_pct}% ({result.candidate_experience} yrs / {result.required_experience} yrs req)")

    print("\n--- Skill Gap Analysis ---")
    print(f"Matched Skills ({len(result.matched_skills)}):")
    if result.matched_skills:
        print(f"  [OK] {', '.join(result.matched_skills)}")
    else:
        print("  None")

    print(f"\nMissing Target Skills ({len(result.missing_skills)}):")
    if result.missing_skills:
        print(f"  [MISSING] {', '.join(result.missing_skills)}")
    else:
        print("  None! (All required skills present)")

    if result.candidate_extra_skills:
        print(f"\nBonus Candidate Skills ({len(result.candidate_extra_skills)}):")
        print(f"  [+] {', '.join(result.candidate_extra_skills[:8])}")

    print("\n--- Strategic Recommendations for Candidate ---")
    for idx, rec in enumerate(result.recommendations, 1):
        print(f"  {idx}. {rec}")

    print("=" * 70 + "\n")
