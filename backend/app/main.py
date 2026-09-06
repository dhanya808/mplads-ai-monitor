import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from .api import analytics, projects, anomalies, reports, auth

app = FastAPI(
    title="MPLADS AI Monitor — Explainable AI Risk & Anomaly Detection Platform",
    description="MoSPI DIID Smart Automation Layer for MPLADS / eSAKSHI Monitoring",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(analytics.router)
app.include_router(projects.router)
app.include_router(anomalies.router)
app.include_router(reports.router)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "MPLADS AI Monitor API", "version": "1.0.0"}

# Frontend static files mounting
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_root():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_file)

    @app.get("/login")
    def serve_login():
        login_file = os.path.join(FRONTEND_DIR, "login.html")
        return FileResponse(login_file)

    @app.get("/dashboard")
    def serve_dashboard():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_file)
