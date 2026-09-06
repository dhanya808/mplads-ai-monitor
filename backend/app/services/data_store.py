import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/varanasi_pc77_dataset.json'))

class DataStore:
    def __init__(self):
        self._load_data()
        self.audit_log = []

    def _load_data(self):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.constituency = self.raw_data.get('constituency', {})
        self.sector_distribution = self.raw_data.get('sector_distribution', [])
        self.financial_summary = self.raw_data.get('financial_summary', {})
        self.projects = self.raw_data.get('projects', [])
        self.contractors = self.raw_data.get('contractors', [])
        self.external_schemes = self.raw_data.get('external_schemes', [])

    def get_constituency(self) -> Dict[str, Any]:
        return self.constituency

    def get_sector_distribution(self) -> List[Dict[str, Any]]:
        return self.sector_distribution

    def get_financial_summary(self) -> Dict[str, Any]:
        return self.financial_summary

    def get_contractors(self) -> List[Dict[str, Any]]:
        return self.contractors

    def get_external_schemes(self) -> List[Dict[str, Any]]:
        return self.external_schemes

    def get_projects(self, 
                     block: Optional[str] = None, 
                     sector: Optional[str] = None, 
                     risk_level: Optional[str] = None, 
                     status: Optional[str] = None,
                     search: Optional[str] = None) -> List[Dict[str, Any]]:
        filtered = self.projects
        
        if block and block.lower() not in ['all', 'all blocks']:
            filtered = [p for p in filtered if p.get('block', '').lower() == block.lower()]
            
        if sector and sector.lower() not in ['all', 'all sectors']:
            filtered = [p for p in filtered if p.get('sector', '').lower() == sector.lower()]
            
        if risk_level and risk_level.lower() not in ['all', 'all risk tiers', 'all risks']:
            if 'high' in risk_level.lower():
                filtered = [p for p in filtered if p.get('risk_level', '').lower() == 'high-risk']
            elif 'medium' in risk_level.lower():
                filtered = [p for p in filtered if p.get('risk_level', '').lower() == 'medium']
            elif 'low' in risk_level.lower():
                filtered = [p for p in filtered if p.get('risk_level', '').lower() in ['low', 'clean']]

        if status and status.lower() not in ['all', 'all statuses', 'all statuses (ongoing & completed)']:
            if 'ongoing' in status.lower():
                filtered = [p for p in filtered if p.get('status', '').lower() == 'ongoing']
            elif 'completed' in status.lower():
                filtered = [p for p in filtered if p.get('status', '').lower() == 'completed']

        if search:
            q = search.lower()
            filtered = [p for p in filtered if q in p.get('id', '').lower() or q in p.get('title', '').lower() or q in p.get('contractor', '').lower()]

        return filtered

    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        for p in self.projects:
            if p.get('id') == project_id:
                return p
        return None

    def update_investigation(self, project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        project = self.get_project_by_id(project_id)
        if not project:
            return None
        
        if 'status' in updates:
            project['anomaly']['status'] = updates['status']
            
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project_id': project_id,
            'status': updates.get('status'),
            'officer': updates.get('assigned_officer', 'District Planning Officer (DPO)'),
            'notes': updates.get('notes', 'Routine audit review step triggered.'),
            'freeze_payment': updates.get('freeze_payment', False),
            'require_geotagged_proof': updates.get('require_geotagged_proof', False),
            'issue_show_cause_notice': updates.get('issue_show_cause_notice', False)
        }
        self.audit_log.append(log_entry)
        project['investigation_history'] = project.get('investigation_history', [])
        project['investigation_history'].append(log_entry)
        return project

    def get_kpis(self, block: Optional[str] = None, sector: Optional[str] = None, risk_level: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        filtered_projects = self.get_projects(block=block, sector=sector, risk_level=risk_level, status=status)
        
        total = len(filtered_projects)
        sanctioned = round(sum(p.get('sanctioned_amount_lakhs', 0.0) for p in filtered_projects), 2)
        expenditure = round(sum(p.get('expenditure_lakhs', 0.0) for p in filtered_projects), 2)
        completed = sum(1 for p in filtered_projects if p.get('status', '').lower() == 'completed')
        ongoing = sum(1 for p in filtered_projects if p.get('status', '').lower() == 'ongoing')
        high_risk = sum(1 for p in filtered_projects if p.get('risk_level', '').lower() == 'high-risk')
        delayed = sum(1 for p in filtered_projects if p.get('delay_days', 0) > 30)
        critical = sum(1 for p in filtered_projects if p.get('anomaly', {}).get('severity', '').lower() == 'critical')
        
        utilization_pct = round((expenditure / sanctioned * 100) if sanctioned > 0 else 0, 1)

        return {
            'total_projects': total,
            'sanctioned_lakhs': sanctioned,
            'expenditure_lakhs': expenditure,
            'utilization_pct': utilization_pct,
            'completed_projects': completed,
            'ongoing_projects': ongoing,
            'high_risk_projects': high_risk,
            'delayed_projects': delayed,
            'critical_anomalies': critical,
            'is_filtered': (total != len(self.projects))
        }

db = DataStore()
