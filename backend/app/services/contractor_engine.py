from typing import Dict, Any, List

class ContractorEngine:
    def compute_hhi(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        totals_by_contractor = {}
        total_value = sum(p.get('sanctioned_amount_lakhs', 0.0) for p in projects)

        if total_value == 0:
            return {'hhi': 0, 'classification': 'Competitive', 'contractor_shares': {}}

        for p in projects:
            c_name = p.get('contractor', 'Unknown')
            val = p.get('sanctioned_amount_lakhs', 0.0)
            totals_by_contractor[c_name] = totals_by_contractor.get(c_name, 0.0) + val

        shares = {}
        hhi_sum = 0.0
        for c_name, val in totals_by_contractor.items():
            share_pct = (val / total_value) * 100.0
            shares[c_name] = round(share_pct, 1)
            hhi_sum += (share_pct ** 2)

        hhi = round(hhi_sum, 1)
        if hhi > 2500:
            classification = 'Highly Concentrated (Monopoly / Collusion Risk)'
        elif hhi > 1500:
            classification = 'Moderately Concentrated'
        else:
            classification = 'Competitive / Diversified'

        return {
            'hhi': hhi,
            'classification': classification,
            'contractor_shares': shares
        }

    def assess_contractor_risk(self, contractor_id: str, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        c_projects = [p for p in projects if p.get('contractor_id') == contractor_id]
        if not c_projects:
            return {'risk_score': 0, 'level': 'Unknown'}

        total_awarded = len(c_projects)
        flagged_count = sum(1 for p in c_projects if p.get('risk_level', '').lower() == 'high-risk')
        avg_delay = sum(p.get('delay_days', 0) for p in c_projects) / total_awarded

        risk_score = min(100, int((flagged_count / total_awarded * 60) + (min(avg_delay, 120) / 120 * 40)))
        level = 'Critical' if risk_score > 75 else ('High' if risk_score > 50 else 'Moderate')

        return {
            'contractor_id': contractor_id,
            'total_projects': total_awarded,
            'flagged_projects': flagged_count,
            'average_delay_days': round(avg_delay, 1),
            'risk_score': risk_score,
            'level': level
        }

contractor_engine = ContractorEngine()
