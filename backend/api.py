"""
FastAPI REST API Service for MPLADS AI Monitor
Provides endpoints for KPI statistics, filtered project lists,
Explainable AI (XAI) project dossiers, and administrative actions.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from typing import Optional, List, Dict, Any

from backend.dataset_generator import generate_mplads_dataset
from backend.ml_engine import process_mplads_anomalies, get_xai_explanations

app = FastAPI(
    title="MPLADS AI Anomaly & Fraud Monitoring API",
    description="MoSPI DIID Automated Risk Triage & Anomaly Detection REST Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global dataset cache & action ledger
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "mplads_processed.csv")
audit_action_log: List[Dict[str, Any]] = []

def get_or_create_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    raw = generate_mplads_dataset(200)
    processed = process_mplads_anomalies(raw)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    processed.to_csv(DATA_FILE, index=False)
    return processed

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "MPLADS AI Monitor REST API"}

@app.get("/api/kpis")
def get_kpis(
    role: str = Query("MoSPI", description="Active user role"),
    state: Optional[str] = None,
    district: Optional[str] = None
):
    df = get_or_create_data()

    # Scope filtering based on role / location
    if role == "District Authority" or district:
        d = district or "Coimbatore"
        df = df[df['district'] == d]
    elif role == "State Nodal Authority" or state:
        s = state or "Tamil Nadu"
        df = df[df['state'] == s]
    elif role == "Member of Parliament":
        df = df[df['district'] == "Varanasi"]

    total_projects = len(df)
    total_sanctioned_cr = round(df['sanction_amount'].sum() / 1e7, 2)
    total_expenditure_cr = round(df['expenditure'].sum() / 1e7, 2)
    critical_risks = len(df[df['risk_tier'] == 'Critical'])
    delayed_projects = len(df[df['delay_flag'] == 'Stagnant / Delayed'])
    completed_projects = len(df[df['status'] == 'Completed'])
    ongoing_projects = len(df[df['status'] == 'Ongoing'])

    return {
        "total_active_projects": total_projects,
        "sanctioned_outlay_cr": total_sanctioned_cr,
        "expenditure_cr": total_expenditure_cr,
        "critical_risk_works": critical_risks,
        "stagnant_delayed": delayed_projects,
        "completed": completed_projects,
        "ongoing": ongoing_projects
    }

@app.get("/api/projects")
def get_projects(
    status: Optional[str] = None,
    district: Optional[str] = None,
    sector: Optional[str] = None,
    risk_tier: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200)
):
    df = get_or_create_data()

    if status and status != "All":
        df = df[df['status'] == status]
    if district and district != "All":
        df = df[df['district'] == district]
    if sector and sector != "All":
        df = df[df['category'] == sector]
    if risk_tier and risk_tier != "All":
        df = df[df['risk_tier'] == risk_tier]

    # Sort descending by risk score
    df = df.sort_values(by="risk_score", ascending=False)
    records = df.head(limit).to_dict(orient="records")
    return {"count": len(records), "projects": records}

@app.get("/api/investigate/{project_id}")
def get_investigation_dossier(project_id: str):
    df = get_or_create_data()
    match = df[df['project_id'] == project_id]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Project ID {project_id} not found")
    
    project_row = match.iloc[0]
    xai = get_xai_explanations(project_row)

    return {
        "project_metadata": project_row.to_dict(),
        "audit_explanations": xai["findings"],
        "recommended_administrative_actions": xai["recommended_actions"]
    }

class ActionRequest(BaseModel):
    project_id: str
    action_type: str # 'inspection', 'freeze_funds', 'clear_record'
    officer_notes: Optional[str] = None

@app.post("/api/actions")
def submit_administrative_action(req: ActionRequest):
    record = {
        "project_id": req.project_id,
        "action_type": req.action_type,
        "officer_notes": req.officer_notes or "Action logged by authorized authority",
        "timestamp": pd.Timestamp.now().isoformat()
    }
    audit_action_log.append(record)
    return {
        "success": True,
        "message": f"Action '{req.action_type}' recorded successfully for {req.project_id}",
        "record": record
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
