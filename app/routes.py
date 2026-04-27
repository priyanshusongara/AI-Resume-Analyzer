from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
import shutil
import os

from app.database import SessionLocal, engine
from app.models import Base, User
from app.schemas import UserCreate, UserLogin
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.pdf_parser import extract_text_from_pdf, extract_skills
from app.rag_engine import compute_similarity

from app.rag_engine import store_skills


Base.metadata.create_all(bind=engine)

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": existing_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    extracted_text = extract_text_from_pdf(file_path)

    resume_skills = extract_skills(extracted_text)
    store_skills(resume_skills, "resume")

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "extracted_text": extracted_text,
        "message": "Resume uploaded and analyzed successfully"
    }



class JobDescriptionRequest(BaseModel):
    resume_skills: list
    job_description: str


@router.post("/analyze-job")
def analyze_job(
    data: JobDescriptionRequest,
    current_user=Depends(get_current_user)
):

    jd_skills = extract_skills(data.job_description)

    resume_skills = data.resume_skills or []

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched_skills = list(resume_set & jd_set)
    missing_skills = list(jd_set - resume_set)
    store_skills(jd_skills, "job")
    
    
    if len(jd_set) == 0:
        keyword_score = 0
    else:
        keyword_score = len(matched_skills) / len(jd_set)
    semantic_score = compute_similarity(
        resume_skills,
        jd_skills)
    final_score = round((keyword_score * 0.6 + semantic_score * 0.4) * 100, 2)

  
    def generate_suggestions(missing_skills):
        suggestions = []
        for skill in missing_skills:
            if skill in ["python", "django", "fastapi"]:
                suggestions.append(f"Build 2-3 real projects using {skill}")
            elif skill in ["docker", "aws"]:
                suggestions.append(f"Deploy a project using {skill} to production")
            elif skill in ["sql", "postgresql", "mysql"]:
                suggestions.append(f"Practice complex queries and database design in {skill}")
            elif skill in ["redis", "celery"]:
                suggestions.append(f"Learn background job processing using {skill}")
            elif skill in ["git", "github"]:
                suggestions.append(f"Maintain active repositories showcasing your work on {skill}")
            else:
                suggestions.append(f"Gain practical experience in {skill} through projects")
        return suggestions
    suggestions = generate_suggestions(missing_skills)
    return {
    "ats_score": final_score,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "suggestions": suggestions,
    "resume_skills": resume_skills,
    "jd_skills": jd_skills,
    "insight": f"You match {len(matched_skills)} out of {len(jd_set)} required skills",
    "note": "Fixed ATS pipeline with consistent skill extraction + scoring"
}