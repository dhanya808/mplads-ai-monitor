from typing import Dict, Any, List
from .spatial_engine import spatial_engine
from .contractor_engine import contractor_engine

class AnomalyEngine:
    def compute_explainable_risk_index(self, project: Dict[str, Any], external_schemes: List[Dict[str, Any]] = None, all_projects: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        exp_pct = project.get('expenditure_pct', 0.0)
        phys_pct = project.get('physical_progress_pct', 0.0)
        delay_days = project.get('delay_days', 0)
        sanctioned = project.get('sanctioned_amount_lakhs', 0.0)
        revised = project.get('revised_estimate_lakhs', sanctioned)

        # 1. Financial-Physical Progress Mismatch (Max 40 pts)
        progress_gap = max(0.0, exp_pct - phys_pct)
        if exp_pct >= 85.0 and phys_pct < 45.0:
            mismatch_pts = min(40.0, 20.0 + (progress_gap * 0.4))
        else:
            mismatch_pts = min(40.0, progress_gap * 0.4)

        # 2. Time Stalling Hazard (Max 30 pts)
        time_pts = min(30.0, (max(0, delay_days) / 150.0) * 30.0)

        # 3. Spatial Duplicate Risk (Max 40 pts)
        spatial_pts = 0.0
        spatial_result = None
        if external_schemes:
            spatial_result = spatial_engine.detect_duplicates(project, external_schemes)
            if spatial_result.get('has_duplicate'):
                top_match = spatial_result['matches'][0]
                spatial_pts = min(40.0, top_match['confidence_score'] * 0.42)

        # 4. Contractor Exposure Risk (Max 20 pts)
        contractor_pts = 0.0
        c_id = project.get('contractor_id')
        if c_id and all_projects:
            c_assessment = contractor_engine.assess_contractor_risk(c_id, all_projects)
            contractor_pts = min(20.0, c_assessment.get('risk_score', 0) * 0.20)

        # 5. Cost Revision Escalation (Max 35 pts)
        cost_escalation_pts = 0.0
        if sanctioned > 0 and revised > sanctioned:
            escalation_pct = ((revised - sanctioned) / sanctioned) * 100.0
            if escalation_pct > 10.0:
                cost_escalation_pts = min(35.0, 15.0 + (escalation_pct * 0.9))

        # Billing Anomaly (Max 35 pts)
        billing_pts = 0.0
        if exp_pct > 90.0 and phys_pct < 60.0:
            billing_pts = min(35.0, (exp_pct - 50.0) * 0.7)

        # Aggregate raw score and clamp to 0-100
        raw_score = mismatch_pts + time_pts + spatial_pts + contractor_pts + cost_escalation_pts + billing_pts
        # Scale to realistic 0-100 range
        eri_score = min(98, max(5, int(raw_score * 0.85 if raw_score > 60 else raw_score)))

        if eri_score >= 70:
            risk_tier = 'High-Risk'
        elif eri_score >= 40:
            risk_tier = 'Medium'
        else:
            risk_tier = 'Low'

        breakdown = {
            'progress_mismatch': round(mismatch_pts, 1),
            'time_stalling': round(time_pts, 1),
            'spatial_overlap': round(spatial_pts, 1),
            'contractor_risk': round(contractor_pts, 1),
            'cost_escalation': round(cost_escalation_pts, 1),
            'billing_anomaly': round(billing_pts, 1)
        }

        # Identify primary risk driver
        primary_driver = max(breakdown.items(), key=lambda x: x[1])

        explanations = []
        if mismatch_pts > 15:
            explanations.append(f'Severe financial drawdown discrepancy ({exp_pct}% paid vs {phys_pct}% work complete).')
        if spatial_pts > 15:
            explanations.append('High spatial alignment overlap with external state infrastructure work.')
        if billing_pts > 15:
            explanations.append('Premature billing observed before full public commissioning and validation.')
        if cost_escalation_pts > 15:
            explanations.append('Unjustified cost revision beyond standard statutory 10% ceiling.')
        if time_pts > 15:
            explanations.append(f'Milestone stalling: {delay_days} days past scheduled delivery date.')

        return {
            'eri_score': eri_score,
            'risk_level': risk_tier,
            'primary_driver': primary_driver[0],
            'risk_breakdown': breakdown,
            'explanations': explanations,
            'spatial_result': spatial_result
        }

anomaly_engine = AnomalyEngine()
