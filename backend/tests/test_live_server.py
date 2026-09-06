import requests

BASE = 'http://127.0.0.1:8000'

print('1. Testing Health Endpoint...')
r = requests.get(f'{BASE}/api/health')
assert r.status_code == 200, f'Status {r.status_code}'
print('Health check passed:', r.json())

print('2. Testing Constituency & KPIs...')
r = requests.get(f'{BASE}/api/analytics/constituency')
assert r.status_code == 200
assert r.json()['id'] == 'PC-77'
print('Constituency:', r.json()['name'])

r = requests.get(f'{BASE}/api/analytics/kpis')
assert r.status_code == 200
kpi = r.json()
assert kpi['total_projects'] == 8
assert kpi['sanctioned_lakhs'] == 443.0
assert kpi['high_risk_projects'] == 4
assert kpi['delayed_projects'] == 6
print(f'KPIs: Total={kpi["total_projects"]}, Sanctioned={kpi["sanctioned_lakhs"]}L, High-Risk={kpi["high_risk_projects"]}, Delayed={kpi["delayed_projects"]}')

print('3. Testing Sector Distribution & Financial Summary...')
r = requests.get(f'{BASE}/api/analytics/sector-distribution')
assert r.status_code == 200
sectors = r.json()
assert len(sectors) == 6
print(f'Sectors: {len(sectors)} categories returned')

r = requests.get(f'{BASE}/api/analytics/financial-summary')
assert r.status_code == 200
fin = r.json()
print(f'Financials: Sanctioned={fin["sanctioned_allocation_lakhs"]}L, Revised={fin["revised_estimate_lakhs"]}L, Actual={fin["actual_expenditure_lakhs"]}L')

print('4. Testing Projects List & Filters...')
r = requests.get(f'{BASE}/api/projects?block=Rohania')
assert r.status_code == 200
assert len(r.json()) > 0
print(f'Projects in Rohania: {len(r.json())}')

print('5. Testing Anomaly Feed & Spatial Duplicates...')
r = requests.get(f'{BASE}/api/anomalies')
assert r.status_code == 200
anomalies = r.json()
print(f'Flagged Anomalies count: {len(anomalies)}')
for a in anomalies:
    print(f'   - {a["project_id"]}: {a["anomaly"]["type"]} (Severity: {a["anomaly"]["severity"]}, ERI: {a["eri_score"]})')

r = requests.get(f'{BASE}/api/anomalies/spatial-duplicates')
assert r.status_code == 200
dups = r.json()
print(f'Spatial Duplicates detected: {len(dups)}')
for d in dups:
    p = d['mplads_project']
    match = d['overlap_result']['matches'][0]
    print(f'   - {p["id"]} overlaps with {match["scheme_name"]} at {match["distance_meters"]}m distance (Confidence: {match["confidence_score"]}%)')

print('6. Testing Project S-Curve Timeline...')
r = requests.get(f'{BASE}/api/projects/MPLADS-UP-VAR-1023/s-curve')
assert r.status_code == 200
assert len(r.json()['timeline']) == 4
print('S-Curve timeline verified')

print('7. Testing Investigation Action POST...')
r = requests.post(f'{BASE}/api/anomalies/MPLADS-UP-VAR-1023/investigate', json={
    'status': 'Under Investigation',
    'assigned_officer': 'Executive Engineer (PWD Rural)',
    'investigation_notes': 'Joint inspection scheduled for physical measurement reconciliation.',
    'freeze_payment': True,
    'require_geotagged_proof': True,
    'issue_show_cause_notice': True
})
assert r.status_code == 200
print('Investigation action saved successfully:', r.json()['message'])

print('8. Testing MoSPI Statutory Audit Notice Dossier...')
r = requests.get(f'{BASE}/api/reports/dossier/MPLADS-UP-VAR-1023/print')
assert r.status_code == 200
assert 'STATUTORY AUDIT NOTICE' in r.text
assert 'GOVERNMENT OF INDIA' in r.text
print('Printable MoSPI Audit Notice generated (length:', len(r.text), 'bytes)')

print('9. Testing Root Frontend Index & Static Assets...')
r = requests.get(f'{BASE}/')
assert r.status_code == 200
assert 'MPLADS AI Monitor' in r.text
assert 'Varanasi Parliamentary Constituency (PC-77)' in r.text
print('Frontend UI delivered with 200 OK')

r = requests.get(f'{BASE}/static/css/styles.css')
assert r.status_code == 200
print('Static CSS delivered with 200 OK')

r = requests.get(f'{BASE}/static/js/app.js')
assert r.status_code == 200
print('Static JS delivered with 200 OK')

print('\n' + '=' * 60)
print('ALL INTEGRATION & E2E TESTS PASSED FLAWLESSLY ON LIVE SERVER!')
print('=' * 60)
