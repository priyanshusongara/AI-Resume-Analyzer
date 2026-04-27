import PyPDF2
import re
from rapidfuzz import fuzz



SKILL_ALIASES = {
    "python": ["python"],
    "django": ["django"],
    "fastapi": ["fastapi"],
    "sql": ["sql", "database", "mysql", "postgresql", "db"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "redis": ["redis", "cache"],
    "docker": ["docker", "container", "containerization"],
    "celery": ["celery"],
    "jwt": ["jwt", "authentication", "auth token"],
    "rest api": ["rest", "rest api", "restful", "api development"],
    "git": ["git"],
    "github": ["github"],
    "aws": ["aws", "amazon web services", "cloud deployment"],
    "linux": ["linux", "ubuntu"],
    "nginx": ["nginx", "web server"],
    "gunicorn": ["gunicorn"],
    "ci/cd": ["ci", "cd", "cicd", "pipeline", "deployment"]
}



def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()



def extract_text_from_pdf(file_path):
    text = ""

    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "

    return clean_text(text)



def extract_skills(text: str):
    text = clean_text(text)
    words = set(text.split())

    found_skills = set()

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            alias_words = alias.split()

            if all(word in words for word in alias_words):
                found_skills.add(skill)
                break

    return list(found_skills)