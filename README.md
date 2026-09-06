# MPLADS AI Monitor — Explainable AI-Based Project Risk & Anomaly Detection Platform

An intelligence and early-warning monitoring layer designed for the **Ministry of Statistics and Programme Implementation (MoSPI) - Data Informatics & Innovation Division (DIID)** to detect anomalies, fraud, and inefficiencies in the implementation of the Members of Parliament Local Area Development Scheme (MPLADS).

---

## Key Features

1. **Explainable Risk Index (ERI: 0–100)**:
   - Multi-factor algorithmic scoring combining financial-physical progress divergence, time stalling hazard, spatial duplicate proximity, contractor exposure, cost escalation, and premature billing.
   - Transparent, auditable factor contribution breakdown (radar charts & natural language explanations).

2. **Multi-Scheme Spatial Duplicate Detection**:
   - Haversine distance and geospatial buffer clustering that detects overlapping civil works (e.g. road alignments within 35 meters of State Gram Sadak Yojana / PMGSY works).

3. **Expenditure–Physical Progress Mismatch Scanner**:
   - Automatically flags red-flag disbursements (e.g. 91% funds disbursed with only 38% physical work logged).

4. **Contractor Cartel & Monopolization Analysis**:
   - Calculates the Herfindahl-Hirschman Index (HHI) to identify market concentration and repetitive contractor awards across administrative blocks.

5. **Role-Based Governance Dashboards**:
   - **Hon. Member of Parliament (MP)**: Constituency entitlement utilization, priority sector distribution, local project progress.
   - **District Magistrate & Planning Officer (DM/DPO)**: Field execution, inspection scheduling, physical milestone verification.
   - **State Nodal Authority (SNA)**: Cross-district comparative performance and fund flow monitoring.
   - **MoSPI Central Review Cell**: National anomaly detection, systemic contractor ring detection, and policy analytics.

6. **Statutory Investigation Workflow & Audit Notice Generator**:
   - Dynamic assignment of verification officers, PFMS disbursement freeze triggers, mandatory 360° geo-tagged photo verification, and print-ready formal MoSPI Audit Notices.

---

## Technology Stack

- **Backend**: Python 3.14, FastAPI, Uvicorn, Pydantic v2, Scikit-learn / NumPy / Pandas.
- **Frontend**: Responsive GovTech SPA with Tailwind CSS, Chart.js (Bar, Donut, Line S-Curve, Radar), Leaflet.js (GIS Map & Duplicate Visualization).
- **Data Layer**: Ingestion schemas modeling MoSPI digigov / eSAKSHI data formats.

---

## Quick Start Guide

### 1. Launch the Server
`ash
python run.py
`

### 2. Access the Platform
- **Dashboard**: Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Statutory Audit Dossier**: [http://127.0.0.1:8000/api/reports/dossier/MPLADS-UP-VAR-1023/print](http://127.0.0.1:8000/api/reports/dossier/MPLADS-UP-VAR-1023/print)
