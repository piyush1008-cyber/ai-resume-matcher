"""Curated skills taxonomy mapping canonical skills and common variants."""

from typing import Dict, List, Set

SKILL_TAXONOMY: Dict[str, List[str]] = {
    # Programming Languages
    "python": ["python", "python3", "py"],
    "c++": ["c++", "cpp", "c plus plus"],
    "java": ["java", "jvm"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "go": ["golang", "go language"],
    "rust": ["rust", "rust-lang"],
    "sql": ["sql", "structured query language"],

    # Backend Frameworks
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django", "drf", "django rest framework"],
    "spring boot": ["spring boot", "springboot", "spring"],
    "express": ["express", "expressjs", "express.js"],
    "node.js": ["node.js", "nodejs", "node"],

    # Databases & Caching
    "postgresql": ["postgresql", "postgres", "psql"],
    "mysql": ["mysql"],
    "sqlite": ["sqlite", "sqlite3"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis", "redis cache"],
    "elasticsearch": ["elasticsearch", "elastic search"],

    # Cloud & DevOps
    "docker": ["docker", "dockerfile", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "ci/cd": ["ci/cd", "continuous integration", "github actions", "jenkins"],
    "git": ["git", "github", "gitlab"],
    "linux": ["linux", "bash", "shell scripting", "unix"],

    # ML & Data Science
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "neural networks"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "nlp": ["nlp", "natural language processing"],

    # Architecture & Concepts
    "rest api": ["rest api", "restful", "restful apis"],
    "graphql": ["graphql"],
    "microservices": ["microservices", "microservice architecture"],
    "websockets": ["websockets", "websocket"],
    "system design": ["system design", "distributed systems", "high availability"],
    "data structures": ["data structures", "algorithms", "dsa"],
}


def get_all_canonical_skills() -> Set[str]:
    """Returns set of canonical skill names."""
    return set(SKILL_TAXONOMY.keys())
