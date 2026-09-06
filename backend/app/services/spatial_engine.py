import math
from typing import Dict, Any, List, Tuple

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)

class SpatialEngine:
    def __init__(self, threshold_meters: float = 100.0):
        self.threshold_meters = threshold_meters

    def detect_duplicates(self, project: Dict[str, Any], external_schemes: List[Dict[str, Any]]) -> Dict[str, Any]:
        p_coords = project.get('coordinates', {})
        p_lat = p_coords.get('lat')
        p_lng = p_coords.get('lng')

        if p_lat is None or p_lng is None:
            return {'has_duplicate': False, 'matches': []}

        matches = []
        for ext in external_schemes:
            e_coords = ext.get('coordinates', {})
            e_lat = e_coords.get('lat')
            e_lng = e_coords.get('lng')
            if e_lat is None or e_lng is None:
                continue

            dist = haversine_distance_meters(p_lat, p_lng, e_lat, e_lng)
            if dist <= self.threshold_meters:
                # Proximity confidence formula: 100% at 0m, 50% at 100m
                confidence = max(10.0, round((1.0 - (dist / self.threshold_meters)) * 100.0, 1))
                matches.append({
                    'external_project_id': ext.get('id'),
                    'scheme_name': ext.get('scheme_name'),
                    'work_name': ext.get('work_name'),
                    'sanction_date': ext.get('sanction_date'),
                    'sanctioned_amount_lakhs': ext.get('sanctioned_amount_lakhs'),
                    'distance_meters': dist,
                    'confidence_score': confidence,
                    'risk_level': 'Critical' if dist < 50 else 'High'
                })

        return {
            'has_duplicate': len(matches) > 0,
            'match_count': len(matches),
            'matches': matches
        }

spatial_engine = SpatialEngine(threshold_meters=100.0)
