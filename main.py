"""Command-line interface for the AI Resume Matcher."""

import argparse
import json
import sys
from pathlib import Path
from src.extractor import extract_profile_metadata
from src.matcher import ResumeMatcher
from src.reporter import print_match_report


def print_banner():
    banner = """
===================================================================
     AI RESUME MATCHER - NLP Candidate-to-Job Fit Engine           
===================================================================
    """
    print(banner)


def cmd_skills(args):
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File '{path}' not found.")
        sys.exit(1)

    text = path.read_text(encoding="utf-8", errors="replace")
    meta = extract_profile_metadata(text)

    print(f"\n--- Extracted Profile Metadata for {path.name} ---")
    print(f"Email:        {meta['email'] or 'Not detected'}")
    print(f"Phone:        {meta['phone'] or 'Not detected'}")
    print(f"Experience:   {meta['years_experience']} years")
    print(f"Education:    {', '.join(meta['education']) if meta['education'] else 'Not detected'}")
    print(f"Skills ({len(meta['skills'])}):")
    for s in meta['skills']:
        print(f"  - {s}")
    print("-" * 50 + "\n")


def cmd_match(args):
    resume_path = Path(args.resume)
    jd_path = Path(args.jd)

    if not resume_path.exists():
        print(f"Error: Resume file '{resume_path}' not found.")
        sys.exit(1)
    if not jd_path.exists():
        print(f"Error: JD file '{jd_path}' not found.")
        sys.exit(1)

    resume_text = resume_path.read_text(encoding="utf-8", errors="replace")
    jd_text = jd_path.read_text(encoding="utf-8", errors="replace")

    matcher = ResumeMatcher()
    result = matcher.match(resume_text, jd_text)

    print_match_report(result, resume_name=resume_path.name, jd_name=jd_path.name)

    if args.json:
        out_file = Path(args.json)
        out_data = {
            "composite_score_pct": result.composite_score_pct,
            "skill_coverage_pct": result.skill_coverage_pct,
            "semantic_similarity_pct": result.semantic_similarity_pct,
            "experience_score_pct": result.experience_score_pct,
            "matched_skills": result.matched_skills,
            "missing_skills": result.missing_skills,
            "recommendations": result.recommendations,
        }
        out_file.write_text(json.dumps(out_data, indent=2), encoding="utf-8")
        print(f"[+] Exported match result to {out_file}")


def cmd_demo(args):
    resume_file = Path("samples/backend_resume.txt")
    backend_jd = Path("samples/senior_backend_jd.txt")
    ml_jd = Path("samples/ml_engineer_jd.txt")

    print("[*] Running AI Resume Matcher demonstration...")
    print("\n>>> TEST 1: Piyush Resume vs Backend Software Engineer JD")
    matcher = ResumeMatcher()
    res1 = matcher.match(
        resume_file.read_text(encoding="utf-8"),
        backend_jd.read_text(encoding="utf-8"),
    )
    print_match_report(res1, resume_name="Piyush_Resume.txt", jd_name="Backend_Engineer_JD.txt")

    print("\n>>> TEST 2: Piyush Resume vs Machine Learning Engineer JD")
    res2 = matcher.match(
        resume_file.read_text(encoding="utf-8"),
        ml_jd.read_text(encoding="utf-8"),
    )
    print_match_report(res2, resume_name="Piyush_Resume.txt", jd_name="ML_Engineer_JD.txt")


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="AI Resume Matcher - NLP Candidate Matching & Skill Gap Analysis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # match
    p_match = subparsers.add_parser("match", help="Match resume against job description")
    p_match.add_argument("--resume", required=True, help="Path to resume text file")
    p_match.add_argument("--jd", required=True, help="Path to JD text file")
    p_match.add_argument("--json", help="Path to save JSON report")
    p_match.set_defaults(func=cmd_match)

    # skills
    p_skills = subparsers.add_parser("skills", help="Extract skills and metadata from document")
    p_skills.add_argument("--file", required=True, help="Path to text document")
    p_skills.set_defaults(func=cmd_skills)

    # demo
    p_demo = subparsers.add_parser("demo", help="Run automated demonstration")
    p_demo.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
