from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.data_store import db
from ..services.anomaly_engine import anomaly_engine

router = APIRouter(prefix='/api/projects', tags=['Projects'])

@router.get('')
def list_projects(
    block: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    return db.get_projects(block=block, sector=sector, risk_level=risk_level, status=status, search=search)

@router.get('/{project_id}')
def get_project_details(project_id: str):
    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    external_schemes = db.get_external_schemes()
    all_projects = db.get_projects()
    live_risk = anomaly_engine.compute_explainable_risk_index(project, external_schemes, all_projects)
    
    return {
        'project': project,
        'live_explainability': live_risk
    }

@router.get('/{project_id}/s-curve')
def get_project_s_curve(project_id: str):
    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Generate timeline points for physical progress vs financial disbursement
    exp_pct = project.get('expenditure_pct', 0.0)
    phys_pct = project.get('physical_progress_pct', 0.0)
    
    timeline = [
        {'milestone': 'Sanction & Mobilization', 'planned_pct': 20.0, 'financial_pct': 30.0, 'physical_pct': 15.0},
        {'milestone': 'Foundation / Plinth / Sub-base', 'planned_pct': 50.0, 'financial_pct': min(exp_pct, 65.0), 'physical_pct': min(phys_pct, 25.0)},
        {'milestone': 'Superstructure / Installation', 'planned_pct': 80.0, 'financial_pct': exp_pct, 'physical_pct': phys_pct},
        {'milestone': 'Finishing & Commissioning', 'planned_pct': 100.0, 'financial_pct': 100.0 if phys_pct == 100 else None, 'physical_pct': 100.0 if phys_pct == 100 else None}
    ]
    return {
        'project_id': project_id,
        'timeline': timeline
    }
