#  AI Resume Analyzer (FastAPI + JWT + RAG)

An end-to-end AI-powered Resume Analyzer that evaluates how well a candidate's resume matches a job description using ATS-style scoring, semantic similarity, and skill gap analysis.

---

##  Features

-  JWT Authentication (Signup/Login)
-  Resume Upload (PDF Parsing)
-  Smart Skill Extraction (Fuzzy Matching)
-  AI Matching Engine (RAG-inspired)
-  ATS Score Calculation
-  Missing Skills Detection
-  Smart Suggestions Engine
-  Full Stack App (FastAPI + HTML/CSS/JS)
-  Deployed on Railway

---

##  How It Works

1. User logs in/signup
2. Uploads resume (PDF)
3. System extracts text from resume
4. Skills are identified using fuzzy matching
5. Job description is analyzed similarly
6. System compares:
   - Resume Skills vs Job Skills
7. Outputs:
   - ATS Score (%)
   - Matched Skills
   - Missing Skills
   - Suggestions for improvement

---

##  Tech Stack

### Backend
- FastAPI
- JWT Authentication
- SQLAlchemy (SQLite)
- Pydantic

### AI / NLP
- RapidFuzz (Skill Matching)
- Sentence Transformers (Local Embeddings)
- Cosine Similarity

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Railway

---

## 📁 Project Structure
