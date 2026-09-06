from fastapi import APIRouter, Query
from typing import Optional
from ..services.data_store import db
from ..services.contractor_engine import contractor_engine

router = APIRouter(prefix='/api/analytics', tags=['Analytics'])

@router.get('/constituency')
def get_constituency():
    return db.get_constituency()

@router.get('/kpis')
def get_kpis(
    block: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    return db.get_kpis(block=block, sector=sector, risk_level=risk_level, status=status)

@router.get('/sector-distribution')
def get_sector_distribution():
    return db.get_sector_distribution()

@router.get('/financial-summary')
def get_financial_summary():
    return db.get_financial_summary()

@router.get('/contractors')
def get_contractors():
    contractors = db.get_contractors()
    all_projects = db.get_projects()
    hhi_analysis = contractor_engine.compute_hhi(all_projects)
    return {
        'contractors': contractors,
        'market_concentration': hhi_analysis
    }
