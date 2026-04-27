from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.routes import router

app = FastAPI(title="AI Resume Analyzer API")

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# PATH SETUP (IMPORTANT)
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

# -----------------------
# STATIC FILES
# -----------------------
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -----------------------
# ROUTES
# -----------------------
app.include_router(router)

# -----------------------
# ROOT → SERVE UI
# -----------------------
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/favicon.ico")
def favicon():
    file_path = os.path.join(FRONTEND_DIR, "assets", "favicon.png")

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return {"error": "favicon not found"}

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))


@app.get("/result")
def serve_result():
    return FileResponse(os.path.join(FRONTEND_DIR, "result.html"))