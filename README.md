
#  AI Resume Analyzer (FastAPI + JWT + RAG)  <img width="32" height="32" alt="favicon" src="https://github.com/user-attachments/assets/46d81bc1-b9ed-41c3-8dd0-4bf72777faed" />

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

# API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the main Login + Signup page (`index.html`) |
| `/signup` | POST | Registers a new user with username, email, and hashed password |
| `/login` | POST | Authenticates user credentials and returns JWT access token |
| `/dashboard` | GET | Serves the dashboard page for resume upload and job description analysis |
| `/upload-resume` | POST | Uploads PDF resume, extracts text, detects skills, and stores resume skills for analysis |
| `/analyze-job` | POST | Compares resume skills with job description, calculates ATS score, identifies matched/missing skills, and generates improvement suggestions |
| `/result` | GET | Serves the final ATS analysis result page (`result.html`) |
| `/favicon.ico` | GET | Serves website favicon |
| `/static/*` | GET | Serves frontend static files like CSS, JavaScript, images, and HTML assets |
| `/docs` | GET | FastAPI Swagger UI for testing APIs interactively |
| `/redoc` | GET | FastAPI ReDoc documentation page |

---

# Protected Routes (Require JWT Bearer Token)

- `/upload-resume`
- `/analyze-job`

These endpoints require a valid JWT token after login.

---

# Author
Priyanshu Songara

---

# Screenshots of the API:



<img width="1920" height="1080" alt="Screenshot (3655)" src="https://github.com/user-attachments/assets/1fdd9cf4-f5a8-4ece-803a-644fd5de1621" />
<img width="1920" height="1080" alt="Screenshot (3654)" src="https://github.com/user-attachments/assets/336fded4-cce2-4991-a4fe-6f1bb05c2b64" />

<img width="1920" height="1080" alt="Screenshot (3656)" src="https://github.com/user-attachments/assets/fdbf897b-cef1-4d2b-b0ec-a8fd57bc69a6" />
<img width="1920" height="1080" alt="Screenshot (3658)" src="https://github.com/user-attachments/assets/9dc2a75b-1de3-4281-af6e-4ffecb097dce" />



