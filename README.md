# 🏛️ MPLADS AI Monitor — Intelligent Risk & Anomaly Detection Platform

> **"See Every Anomaly. Protect Every Rupee. Deliver Every Public Asset."**  
> An intelligent early-warning radar built for the **Ministry of Statistics and Programme Implementation (MoSPI) - Data Informatics & Innovation Division (DIID)** to detect ghost billing, duplicate works, project stalling, and contractor cartels under the **Members of Parliament Local Area Development Scheme (MPLADS)**.

---

## 🌐 Live Public Deployment (Instant Access)

Evaluate the live production platform directly in your browser:

- **🏛️ Stakeholder Parichay Sign In**: [https://mplads-ai-monitor-liart.vercel.app/login](https://mplads-ai-monitor-liart.vercel.app/login)
- **📊 Executive Command Dashboard**: [https://mplads-ai-monitor-liart.vercel.app/dashboard](https://mplads-ai-monitor-liart.vercel.app/dashboard)
- **⚡ Interactive REST API Swagger**: [https://mplads-ai-monitor-liart.vercel.app/docs](https://mplads-ai-monitor-liart.vercel.app/docs)
- **📄 Sample Statutory Inspection Notice**: [https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print](https://mplads-ai-monitor-liart.vercel.app/api/reports/dossier/MPLADS-UP-VAR-1023/print)

> **💡 Quick Demo Tour**: On the login screen, simply click any of the 4 demo role cards (**Hon'ble MP**, **District Magistrate**, **State Nodal Authority**, or **MoSPI Ministry**) to instantly impersonate that tier of Indian governance with zero typing!

---

## 🎯 Why This Problem Statement? (The ₹4,000+ Crore Challenge)

Under the MPLAD Scheme, the Government of India allocates **₹5 Crores annually to every Member of Parliament** (543 Lok Sabha + 245 Rajya Sabha MPs), totaling over **₹4,000 Crores of taxpayer funds every single year** to build vital community infrastructure: primary schools, drinking water filtration plants, rural roads, and healthcare centers.

However, monitoring across ~780 District Collectorates faces three critical systemic bottlenecks:
1. **The "Post-Mortem" Audit Delay:** Audits conducted by the Comptroller & Auditor General (CAG) typically occur **2 to 3 years after funds are spent**. By the time anomalies are flagged, rogue contractors have abandoned the sites, and funds are irrecoverable.
2. **Disconnected Data Silos:** e-SAKSHI (sanctions), PFMS (bank transfers), and state engineering registries operate in isolation. A contractor can bill the MPLADS fund for a road already constructed under the State Gram Sadak Yojana without anyone noticing.
3. **Hidden Contractor Cartels:** Without automated market analytics, contractor syndicates quietly monopolize 40% to 60% of works across administrative blocks, leading to chronic execution delays and cost inflation.

---

## 💡 Why We Chose It & How It Helps

### Why We Chose This Problem:
We chose this problem statement because **governance technology should protect the common citizen**. When an MPLADS drinking water RO plant or village connecting road stalls for 180 days or exists only on paper as a ghost asset, it is marginalized rural communities that suffer. We wanted to build a high-impact, deployment-ready solution that transforms passive bureaucratic record-keeping into a **proactive, real-time intelligence radar**.

### How Our Solution Helps:
- **Shift from Post-Audit to Real-Time Prevention:** Detects financial-physical divergence (e.g., 91% funds disbursed with only 38% physical work done) *while construction is ongoing*, allowing the District Magistrate to freeze the next payment tranche before money leaks.
- **Zero New Data Entry:** Field engineers and clerks are already overburdened. Our platform acts as a **smart, non-invasive overlay** that ingests existing e-SAKSHI and PFMS records without requiring new forms.
- **0–100 Explainable Risk Index (ERI):** Eliminates black-box AI mystery. Every flagged project comes with an itemized, mathematically defensible SHAP radar breakdown.
- **1-Click Enforcement:** Equips District Collectors with auto-generated, pre-filled official MoSPI inspection notices and tranche freeze orders in one click.

---

## 🚀 Key Features

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
