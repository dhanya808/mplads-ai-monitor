# MPLADS AI Monitor — Explainable AI-Based Project Risk & Anomaly Detection Platform

An intelligence and early-warning monitoring layer designed for the **Ministry of Statistics and Programme Implementation (MoSPI) - Data Informatics & Innovation Division (DIID)** to detect anomalies, fraud, and inefficiencies in the implementation of the Members of Parliament Local Area Development Scheme (MPLADS).

---

## 🌐 Live Public Deployment (Instant Access)

Anyone can access and evaluate the live platform directly without running local servers:

- **🏛️ Stakeholder Parichay Sign In**: [https://mplads-ai-monitor-liart.vercel.app/login](https://mplads-ai-monitor-liart.vercel.app/login)
- **📊 Executive Command Dashboard**: [https://mplads-ai-monitor-liart.vercel.app/dashboard](https://mplads-ai-monitor-liart.vercel.app/dashboard)
- **⚡ Interactive REST API Swagger**: [https://mplads-ai-monitor-liart.vercel.app/docs](https://mplads-ai-monitor-liart.vercel.app/docs)
- **📄 Sample Statutory Audit Notice**: [https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print](https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print)
- **📑 Master Presentation Guide PDF**: [Download PDF Guide](https://mplads-ai-monitor-liart.vercel.app/MPLADS_AI_Monitor_SIH_Master_Guide.pdf)

> **Demo Tip**: On the login page, click any of the 4 one-click demo role cards (**Member of Parliament**, **District Magistrate**, **State Nodal Authority**, or **MoSPI Ministry**) to instantly impersonate that stakeholder view!

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

### 1. Launch the Server Locally (Optional)
```bash
python run.py
```

### 2. Access the Platform
- **Public Live Access**: [https://mplads-ai-monitor-liart.vercel.app/login](https://mplads-ai-monitor-liart.vercel.app/login)
- **Local Dashboard**: [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
- **Interactive OpenAPI Documentation**: [https://mplads-ai-monitor-liart.vercel.app/docs](https://mplads-ai-monitor-liart.vercel.app/docs)
- **Statutory Audit Dossier**: [https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print](https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print)
