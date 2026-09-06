import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from backend.app.services.data_store import db
from backend.app.services.spatial_engine import spatial_engine
from backend.app.services.anomaly_engine import anomaly_engine
from backend.app.services.contractor_engine import contractor_engine

def run_tests():
    print('Testing DataStore...')
    constituency = db.get_constituency()
    assert constituency['id'] == 'PC-77', f'Expected PC-77, got {constituency.get("id")}'
    projects = db.get_projects()
    assert len(projects) == 8, f'Expected 8 projects, got {len(projects)}'
    print(f'DataStore loaded {len(projects)} projects for {constituency["name"]}')

    print('Testing SpatialEngine...')
    p_6088 = db.get_project_by_id('MPLADS-UP-VAR-6088')
    ext_schemes = db.get_external_schemes()
    dup_res = spatial_engine.detect_duplicates(p_6088, ext_schemes)
    assert dup_res['has_duplicate'] is True, 'Spatial duplicate expected'
    dist = dup_res['matches'][0]['distance_meters']
    assert dist < 50, f'Expected distance < 50m, got {dist}m'
    print(f'Spatial duplicate correctly flagged at {dist}m distance')

    print('Testing AnomalyEngine...')
    p_1023 = db.get_project_by_id('MPLADS-UP-VAR-1023')
    risk_res = anomaly_engine.compute_explainable_risk_index(p_1023, ext_schemes, projects)
    assert risk_res['eri_score'] >= 80, f'Expected high ERI >= 80, got {risk_res["eri_score"]}'
    assert 'progress_mismatch' in risk_res['risk_breakdown'], 'Missing progress mismatch breakdown'
    print(f'Explainable Risk Index calculated: {risk_res["eri_score"]}/100 with breakdown')

    print('Testing ContractorEngine...')
    hhi = contractor_engine.compute_hhi(projects)
    assert hhi['hhi'] > 0, 'Expected positive HHI score'
    print(f'Contractor HHI Market Concentration: {hhi["hhi"]} ({hhi["classification"]})')

    print('Testing Investigation workflow...')
    update_res = db.update_investigation('MPLADS-UP-VAR-1023', {
        'status': 'Under Investigation',
        'assigned_officer': 'Executive Engineer PWD',
        'notes': 'Site inspection team deployed for cross-measurement.'
    })
    assert update_res['anomaly']['status'] == 'Under Investigation'
    print('Investigation workflow and audit logging verified')

    print('ALL BACKEND ENGINE TESTS PASSED!')

if __name__ == '__main__':
    run_tests()
