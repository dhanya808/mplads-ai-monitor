from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime
from ..services.data_store import db
from ..services.anomaly_engine import anomaly_engine

router = APIRouter(prefix='/api/reports', tags=['Reports'])

@router.get('/dossier/{project_id}')
def generate_dossier_data(project_id: str):
    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
        
    external = db.get_external_schemes()
    all_projects = db.get_projects()
    risk = anomaly_engine.compute_explainable_risk_index(project, external, all_projects)
    
    suffix = project_id[-4:] if len(project_id) >= 4 else project_id
    report_id = 'MoSPI-AUDIT-' + suffix + '-' + datetime.now().strftime('%Y%m%d')
    
    return {
        'report_id': report_id,
        'generated_at': datetime.now().strftime('%d %B %Y, %H:%M IST'),
        'ministry': 'Ministry of Statistics & Programme Implementation (MoSPI)',
        'division': 'Data Informatics & Innovation Division (DIID)',
        'constituency': 'Varanasi (PC-77), Uttar Pradesh',
        'project': project,
        'risk_analysis': risk,
        'statutory_actions': [
            'Depute Executive Engineer (PWD/REES) for joint physical inspection within 7 days.',
            'Hold subsequent tranche disbursements in PFMS until physical measurement book reconciliation.',
            'Mandate high-resolution geotagged photographs with Bhashini lat-long metadata.',
            'Verify contractor asset declaration against GIS corridor database.'
        ]
    }

@router.get('/dossier/{project_id}/print', response_class=HTMLResponse)
def print_dossier_html(project_id: str):
    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
        
    external = db.get_external_schemes()
    all_projects = db.get_projects()
    risk = anomaly_engine.compute_explainable_risk_index(project, external, all_projects)
    suffix = project_id[-4:] if len(project_id) >= 4 else project_id
    report_id = 'MoSPI-AUDIT-' + suffix + '-' + datetime.now().strftime('%Y%m%d')
    generated_at = datetime.now().strftime('%d %b %Y, %H:%M IST')
    
    ev_items = []
    for k, v in project.get('anomaly', {}).get('evidence', {}).items():
        k_clean = k.replace('_', ' ').title()
        ev_items.append('<li><strong>' + k_clean + ':</strong> ' + str(v) + '</li>')
    ev_html = '\n'.join(ev_items)
    
    badge_class = 'badge-critical' if project.get('eri_score', 0) > 85 else 'badge-high'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>MoSPI Inspection Notice - {project['id']}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #1e293b; line-height: 1.6; max-width: 850px; margin: auto; }}
        .header {{ border-bottom: 3px double #0f172a; padding-bottom: 15px; margin-bottom: 25px; text-align: center; }}
        .emblem {{ font-size: 24px; font-weight: bold; color: #0f172a; letter-spacing: 1px; }}
        .sub-header {{ font-size: 14px; color: #475569; margin-top: 4px; }}
        .meta-bar {{ display: flex; justify-content: space-between; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px 18px; border-radius: 6px; margin-bottom: 25px; font-size: 13px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
        .badge-critical {{ background: #fee2e2; color: #991b1b; }}
        .badge-high {{ background: #ffedd5; color: #9a3412; }}
        .card {{ border: 1px solid #cbd5e1; border-radius: 6px; padding: 16px; margin-bottom: 20px; }}
        .card h3 {{ margin-top: 0; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px; }}
        .evidence-list {{ background: #fff7ed; border-left: 4px solid #f97316; padding: 14px 20px; border-radius: 0 6px 6px 0; }}
        .evidence-list li {{ margin-bottom: 6px; }}
        .orders {{ background: #f0fdf4; border-left: 4px solid #16a34a; padding: 14px 20px; border-radius: 0 6px 6px 0; }}
        .orders li {{ margin-bottom: 6px; }}
        .sign {{ margin-top: 50px; display: flex; justify-content: space-between; font-size: 13px; }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="text-align: right; margin-bottom: 20px;">
        <button onclick="window.print()" style="padding: 8px 16px; background: #0284c7; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Print / Save as PDF</button>
    </div>

    <div class="header">
        <div class="emblem">GOVERNMENT OF INDIA</div>
        <div class="sub-header">MINISTRY OF STATISTICS & PROGRAMME IMPLEMENTATION (MoSPI)</div>
        <div class="sub-header">Data Informatics & Innovation Division (DIID) — MPLADS AI Early Warning Cell</div>
        <h2 style="margin-top: 15px; margin-bottom: 5px; color: #0f172a;">STATUTORY AUDIT NOTICE & FIELD INSPECTION REQUISITION</h2>
    </div>

    <div class="meta-bar">
        <div><strong>Notice Ref:</strong> {report_id}</div>
        <div><strong>Date:</strong> {generated_at}</div>
        <div><strong>Constituency:</strong> Varanasi (PC-77), UP</div>
    </div>

    <div class="card">
        <h3>Project Identification & Financial Profile</h3>
        <div class="grid">
            <div><strong>Project ID:</strong> {project['id']}</div>
            <div><strong>Executing Block:</strong> {project['block']}</div>
            <div style="grid-column: span 2;"><strong>Work Description:</strong> {project['title']}</div>
            <div><strong>Sanctioned Allocation:</strong> ₹{project['sanctioned_amount_lakhs']:.2f} Lakhs</div>
            <div><strong>Revised Estimate:</strong> ₹{project['revised_estimate_lakhs']:.2f} Lakhs</div>
            <div><strong>Amount Disbursed:</strong> ₹{project['expenditure_lakhs']:.2f} Lakhs ({project['expenditure_pct']}%)</div>
            <div><strong>Physical Progress Logged:</strong> {project['physical_progress_pct']}%</div>
            <div><strong>Executing Contractor:</strong> {project['contractor']}</div>
            <div><strong>Target Deadline:</strong> {project['target_date']} ({project['delay_days']} days overdue)</div>
        </div>
    </div>

    <div class="card">
        <h3>AI Anomaly Diagnosis & Risk Score</h3>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div>
                <span style="font-size: 16px; font-weight: bold;">Flagged Anomaly: {project.get('anomaly', {}).get('type')}</span>
                <div style="color: #64748b; font-size: 13px; margin-top: 4px;">{project.get('anomaly', {}).get('description')}</div>
            </div>
            <div style="text-align: right;">
                <span class="badge {badge_class}">
                    Explainable Risk Index: {project['eri_score']} / 100
                </span>
            </div>
        </div>

        <h4>Supporting Algorithmic Evidence:</h4>
        <ul class="evidence-list">
            {ev_html}
        </ul>
    </div>

    <div class="card">
        <h3>Directives to District Magistrate & Implementing Agency</h3>
        <ol class="orders">
            <li><strong>Immediate Site Inspection:</strong> Depute an Executive Engineer along with District Planning Cell representative to conduct joint on-site measurement within 7 calendar days.</li>
            <li><strong>Financial Tranche Hold:</strong> Temporary freeze placed on subsequent voucher payments under PFMS for work ID <code>{project['id']}</code>.</li>
            <li><strong>Mandatory Geo-Verification:</strong> Upload geotagged date-stamped 360-degree imagery directly into the eSAKSHI inspection module.</li>
            <li><strong>Show-Cause Response:</strong> Executing agency and contractor must submit written clarification within 5 working days failing which formal recovery/blacklisting proceedings will initiate.</li>
        </ol>
    </div>

    <div class="sign">
        <div>
            <strong>Generated by:</strong><br>
            MPLADS AI Monitor Intelligence Layer<br>
            MoSPI DIID Automation Engine
        </div>
        <div style="text-align: right;">
            <strong>Approved for Issue:</strong><br>
            Director, Monitoring & Evaluation<br>
            Ministry of Statistics & Programme Implementation
        </div>
    </div>
</body>
</html>"""
    return html
