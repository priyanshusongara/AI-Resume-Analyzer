from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes import router

app = FastAPI(title="AI Resume Analyzer API")

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTES
# -------------------------
app.include_router(router)

# -------------------------
# SERVE FRONTEND
# -------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_home():
    return FileResponse("frontend/index.html")


@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("frontend/dashboard.html")


@app.get("/result")
def serve_result():
    return FileResponse("frontend/result.html")