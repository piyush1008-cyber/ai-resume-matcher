"""Streamlit Interactive Application for AI Resume & Job Description Matching."""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))

from extractor import extract_profile_metadata
from matcher import ResumeMatcher

st.set_page_config(
    page_title="AI Resume Matcher & Skill Gap Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume Matcher & Skill Gap Analyzer")
st.markdown(
    """
    **NLP-powered Candidate-to-Job Fit Engine.**  
    Computes TF-IDF Cosine Similarity, technical skill overlap across 150+ keywords, experience alignment, and generates targeted career upskilling recommendations.
    """
)

# Load sample files if available
backend_resume_sample = ""
backend_jd_sample = ""

samples_dir = Path(__file__).parent / "samples"
if (samples_dir / "backend_resume.txt").exists():
    backend_resume_sample = (samples_dir / "backend_resume.txt").read_text(encoding="utf-8")
if (samples_dir / "senior_backend_jd.txt").exists():
    backend_jd_sample = (samples_dir / "senior_backend_jd.txt").read_text(encoding="utf-8")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📝 Candidate Resume")
    use_sample_res = st.checkbox("Use Piyush Kangle's Sample Resume", value=True)
    if use_sample_res and backend_resume_sample:
        resume_text = st.text_area("Resume Text", value=backend_resume_sample, height=350)
    else:
        resume_text = st.text_area("Paste Resume Text Here", height=350)

with col_right:
    st.subheader("🎯 Job Description (JD)")
    use_sample_jd = st.checkbox("Use Senior Backend Engineer JD", value=True)
    if use_sample_jd and backend_jd_sample:
        jd_text = st.text_area("Job Description Text", value=backend_jd_sample, height=350)
    else:
        jd_text = st.text_area("Paste Target Job Description Here", height=350)

st.markdown("---")

if st.button("🚀 Analyze Candidate Fit & Skill Gaps", type="primary", use_container_width=True):
    if not resume_text.strip() or not jd_text.strip():
        st.warning("Please provide both Resume and Job Description text.")
    else:
        matcher = ResumeMatcher()
        with st.spinner("Analyzing NLP semantic vectors and skill taxonomies..."):
            result = matcher.match(resume_text, jd_text)
            meta = extract_profile_metadata(resume_text)

        st.subheader("📊 Match Diagnostics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Overall Fit Score", f"{result.composite_score_pct}%")
        m2.metric("Skill Overlap", f"{result.skill_coverage_pct}%")
        m3.metric("Semantic NLP Match", f"{result.semantic_similarity_pct}%")
        m4.metric("Experience Match", f"{result.experience_score_pct}%")

        st.progress(float(result.composite_score_pct) / 100.0)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("##### ✅ Matched Skills")
            if result.matched_skills:
                for s in result.matched_skills:
                    st.success(f"✓ {s}")
            else:
                st.write("None detected.")

        with c2:
            st.markdown("##### ❌ Missing Skills Required by JD")
            if result.missing_skills:
                for s in result.missing_skills:
                    st.error(f"✗ {s}")
            else:
                st.write("None! All required skills matched.")

        with c3:
            st.markdown("##### 🌟 Bonus Candidate Skills")
            if result.candidate_extra_skills:
                for s in result.candidate_extra_skills[:8]:
                    st.info(f"+ {s}")

        st.markdown("---")
        st.subheader("💡 Strategic Upskilling Recommendations")
        for idx, rec in enumerate(result.recommendations, 1):
            st.markdown(f"**{idx}.** {rec}")
