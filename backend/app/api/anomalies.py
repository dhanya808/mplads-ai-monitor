from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from ..services.data_store import db
from ..services.spatial_engine import spatial_engine
from ..models.schemas import InvestigationUpdateRequest

router = APIRouter(prefix='/api/anomalies', tags=['Anomalies'])

@router.get('')
def get_anomalies(
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    projects = db.get_projects()
    anomalies = []
    for p in projects:
        a = p.get('anomaly', {})
        if a and a.get('type') and a.get('type') != 'None':
            anomalies.append({
                'project_id': p['id'],
                'project_title': p['title'],
                'sector': p['sector'],
                'block': p['block'],
                'contractor': p['contractor'],
                'sanctioned_amount_lakhs': p['sanctioned_amount_lakhs'],
                'expenditure_pct': p['expenditure_pct'],
                'physical_progress_pct': p['physical_progress_pct'],
                'delay_days': p['delay_days'],
                'eri_score': p['eri_score'],
                'risk_level': p['risk_level'],
                'anomaly': a
            })
    
    if severity:
        anomalies = [a for a in anomalies if a['anomaly']['severity'].lower() == severity.lower()]
    if status:
        anomalies = [a for a in anomalies if a['anomaly']['status'].lower() == status.lower()]
        
    return anomalies

@router.post('/{project_id}/investigate')
def update_investigation(project_id: str, payload: InvestigationUpdateRequest):
    updated = db.update_investigation(project_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail='Project not found')
    return {
        'message': 'Investigation updated successfully',
        'project': updated
    }

@router.get('/spatial-duplicates')
def get_spatial_duplicates():
    projects = db.get_projects()
    external = db.get_external_schemes()
    duplicates = []
    
    for p in projects:
        res = spatial_engine.detect_duplicates(p, external)
        if res.get('has_duplicate'):
            duplicates.append({
                'mplads_project': p,
                'overlap_result': res
            })
            
    return duplicates
