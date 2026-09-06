from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Coordinates(BaseModel):
    lat: float
    lng: float

class RiskBreakdown(BaseModel):
    progress_mismatch: Optional[float] = 0.0
    time_stalling: Optional[float] = 0.0
    contractor_risk: Optional[float] = 0.0
    billing_anomaly: Optional[float] = 0.0
    spatial_overlap: Optional[float] = 0.0
    cost_escalation: Optional[float] = 0.0

class Anomaly(BaseModel):
    type: str
    date: str
    severity: str
    status: str
    description: str
    evidence: Dict[str, Any] = {}

class Project(BaseModel):
    id: str
    title: str
    sector: str
    block: str
    location: str
    contractor: str
    contractor_id: str
    status: str
    sanctioned_amount_lakhs: float
    revised_estimate_lakhs: float
    expenditure_lakhs: float
    expenditure_pct: float
    physical_progress_pct: float
    target_date: str
    delay_days: int
    coordinates: Coordinates
    eri_score: int
    risk_level: str
    risk_breakdown: RiskBreakdown
    anomaly: Anomaly

class Constituency(BaseModel):
    id: str
    name: str
    state: str
    district: str
    mp_name: str
    lok_sabha: str
    financial_year: str
    last_sync: str
    entitlement_crores: float
    sanctioned_lakhs: float
    expenditure_lakhs: float
    utilization_pct: float
    total_projects: int
    completed_projects: int
    ongoing_projects: int
    high_risk_projects: int
    delayed_projects: int
    critical_anomalies: int

class SectorItem(BaseModel):
    sector: str
    share_pct: float
    amount_lakhs: float
    color: str

class FinancialSummary(BaseModel):
    sanctioned_allocation_lakhs: float
    revised_estimate_lakhs: float
    actual_expenditure_lakhs: float

class Contractor(BaseModel):
    id: str
    name: str
    pan: str
    projects_awarded: int
    total_value_lakhs: float
    concentration_hhi_risk: str
    average_delay_days: int
    anomalies_flagged: int
    blacklisted_status: str

class InvestigationUpdateRequest(BaseModel):
    status: str
    investigation_notes: Optional[str] = None
    assigned_officer: Optional[str] = None
    freeze_payment: Optional[bool] = False
    require_geotagged_proof: Optional[bool] = False
    issue_show_cause_notice: Optional[bool] = False

class AuditReportResponse(BaseModel):
    report_id: str
    generated_at: str
    project_id: str
    project_title: str
    constituency: str
    eri_score: int
    anomaly_type: str
    severity: str
    evidence: Dict[str, Any]
    investigation_status: str
    recommended_orders: List[str]
