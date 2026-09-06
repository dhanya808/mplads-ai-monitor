import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MPLADS AI Monitor — SIH Master Guide & Presentation Deck</title>
<style>
  @page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-after: always;
  }
  .cover-page {
    text-align: center;
    padding-top: 60px;
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .emblem {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background-color: #0f172a;
    color: #f59e0b;
    border: 3px solid #f59e0b;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 20pt;
    font-weight: bold;
    font-family: Georgia, serif;
    margin-bottom: 15px;
  }
  h1.title {
    font-size: 26pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 10px 0;
  }
  p.subtitle {
    font-size: 13pt;
    color: #475569;
    font-weight: 600;
    margin: 0 0 25px 0;
  }
  .sih-badge {
    display: inline-block;
    background-color: #f0fdf4;
    color: #166534;
    border: 1.5px solid #86efac;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 10pt;
    margin-bottom: 30px;
  }
  .meta-box {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    max-width: 500px;
    margin: 0 auto;
    text-align: left;
    font-size: 10pt;
  }
  .meta-box table {
    width: 100%;
    border-collapse: collapse;
  }
  .meta-box td {
    padding: 6px 4px;
  }
  .meta-box td.label {
    font-weight: bold;
    color: #475569;
    width: 40%;
  }
  .meta-box td.val {
    color: #0f172a;
  }
  h2.section-header {
    font-size: 16pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 25px;
    margin-bottom: 12px;
  }
  h3.sub-header {
    font-size: 12pt;
    font-weight: 700;
    color: #0369a1;
    margin-top: 16px;
    margin-bottom: 6px;
  }
  .callout {
    background-color: #f0fdfa;
    border-left: 4px solid #0d9488;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 10pt;
  }
  .callout-alert {
    background-color: #fef2f2;
    border-left: 4px solid #ef4444;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 10pt;
  }
  .callout-amber {
    background-color: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 10pt;
  }
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
  }
  table.data-table th {
    background-color: #f1f5f9;
    color: #334155;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 8pt;
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    text-align: left;
  }
  table.data-table td {
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }
  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }
  .speaker-script {
    background-color: #f8fafc;
    border: 1px dashed #64748b;
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 8px;
    font-size: 9.5pt;
    color: #1e293b;
    font-style: italic;
  }
  .speaker-badge {
    font-weight: bold;
    color: #0284c7;
    font-style: normal;
    text-transform: uppercase;
    font-size: 8pt;
    display: block;
    margin-bottom: 4px;
  }
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 8pt;
    font-weight: bold;
  }
  .badge-red { background-color: #fee2e2; color: #b91c1c; }
  .badge-blue { background-color: #e0f2fe; color: #0369a1; }
  .badge-green { background-color: #dcfce7; color: #15803d; }
  .badge-amber { background-color: #fef3c7; color: #b45309; }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page page-break">
  <div>
    <div style="text-align: center;">
      <div class="emblem">GOI</div>
    </div>
    <div style="font-size: 11pt; font-weight: bold; color: #64748b; letter-spacing: 2px; text-transform: uppercase;">
      Ministry of Statistics and Programme Implementation (MoSPI)
    </div>
    <h1 class="title">MPLADS AI MONITOR</h1>
    <p class="subtitle">Explainable AI-Based Project Risk & Anomaly Detection Platform</p>
    <div class="sih-badge">SMART INDIA HACKATHON 2025/2026 — MASTER PROJECT & PITCH MANUAL</div>
  </div>

  <div class="meta-box">
    <table>
      <tr><td class="label">Problem Statement:</td><td class="val">MPLADS AI Anomaly & Risk Monitoring</td></tr>
      <tr><td class="label">Nodal Organization:</td><td class="val">MoSPI — DIID (Data Informatics & Innovation Division)</td></tr>
      <tr><td class="label">Theme:</td><td class="val">Smart Governance & Public Accountability</td></tr>
      <tr><td class="label">Category:</td><td class="val">Software Edition (GovTech / Explainable AI)</td></tr>
      <tr><td class="label">Pilot Jurisdiction:</td><td class="val">Varanasi Parliamentary Constituency (PC-77)</td></tr>
      <tr><td class="label">Repository:</td><td class="val">github.com/dhanya808/mplads-ai-monitor</td></tr>
    </table>
  </div>

  <div style="font-size: 9pt; color: #94a3b8; text-align: center; margin-bottom: 20px;">
    Comprehensive Reference Handbook for Team Pitch, Jury Q&A Defense, and Technical Verification
  </div>
</div>

<!-- CHAPTER 1: PROBLEM STATEMENT & THE 3 LEAKS -->
<div>
  <h2 class="section-header">CHAPTER 1: Problem Statement & Ground Realities</h2>
  
  <h3 class="sub-header">1. What is MPLADS?</h3>
  <p>The <strong>Member of Parliament Local Area Development Scheme (MPLADS)</strong> is a Central Sector Scheme through which each Member of Parliament (543 in Lok Sabha and 245 in Rajya Sabha) is allocated <strong>₹5.00 Crore annually</strong> to recommend capital works addressing local developmental needs (drinking water, roads, school classrooms, healthcare facilities, and solar lighting). Nationally, this accounts for over <strong>₹4,000+ Crores of public funds every year</strong>.</p>

  <h3 class="sub-header">2. The Root Cause of Governance Failure</h3>
  <p>Currently, civil progress is entered by local implementing agencies on the <strong>eSAKSHI portal</strong>, while financial releases occur via the <strong>Public Financial Management System (PFMS)</strong>. Because these two systems operate as disconnected silos with no real-time cross-verification, massive irregularities occur.</p>

  <h3 class="sub-header">3. The Three Critical Governance Leaks</h3>
  <div class="callout-alert">
    <strong>1. The Phantom Asset (Duplicate Civil Works / Double Billing):</strong><br>
    A village road was already constructed under <em>State Gram Sadak Yojana</em> or <em>PMGSY</em>. A dishonest agency files the exact same road under MPLADS, claims it as a fresh work, and draws ₹50 Lakhs from the treasury for work that was already completed!
  </div>

  <div class="callout-amber">
    <strong>2. The ₹50,000 Pencil (Financial–Physical Mismatch & Premature Billing):</strong><br>
    A contractor receives approval for a ₹78.50 Lakh road and drain. They perform preliminary excavation (38% physical work done), but collude to withdraw <strong>91% (₹71.44 Lakhs) of funds</strong>! Work then halts completely, leaving public funds locked up.
  </div>

  <div class="callout">
    <strong>3. The Forgotten Piggy Bank (Stagnant Funds & Contractor Cartels):</strong><br>
    A single favored contractor wins 5 different contracts across adjacent blocks. Because they lack adequate machinery and labor forces, all works stall for <strong>over 140 days</strong>. Money sits idle in implementing agency bank accounts while citizens wait for clean water.
  </div>

  <h3 class="sub-header">4. Why Manual Auditing Fails</h3>
  <p>Traditional manual audits by the Comptroller & Auditor General (CAG) take place <strong>2 to 3 years after money has already left the bank</strong>. It is a "post-mortem." <strong>MPLADS AI Monitor</strong> shifts governance from post-mortem audits to <strong>real-time, proactive AI prevention</strong> before subsequent tranches are disbursed.</p>
</div>

<div class="page-break"></div>

<!-- CHAPTER 2: DATA ORIGIN -->
<div>
  <h2 class="section-header">CHAPTER 2: Data Origin & Authenticity</h2>

  <div class="callout">
    <strong>Exact Jury Answer: "Where did you get your dataset?"</strong><br>
    <em>"eSAKSHI is an official Government of India intranet portal run by NIC (National Informatics Centre). Accessing live government databases requires official government officer credentials (Parichay SSO), so direct third-party write access is restricted for cybersecurity.<br><br>
    Therefore, we studied the <strong>official eSAKSHI and PFMS data dictionary and reporting standards</strong> issued under MoSPI's 2023 Guidelines. We modeled an authentic, realistic dataset for <strong>Varanasi Parliamentary Constituency (PC-77)</strong>. It includes authentic administrative blocks (Rohania, Sevapuri, Cholapur, Kashi Vidyapeeth), authentic civil works (CC roads, RO plants, school ramps), real contractor PAN structures, and GPS coordinates."</em>
  </div>

  <h3 class="sub-header">Dataset Schema & Key Parameters</h3>
  <table class="data-table">
    <thead>
      <tr>
        <th>Data Category</th>
        <th>Source Portal</th>
        <th>Parameters Captured</th>
        <th>Audit Significance</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Project Master</strong></td>
        <td>eSAKSHI</td>
        <td>Project ID, Title, Block, Sector, Sanction Date</td>
        <td>Baseline identification & sector share tracking</td>
      </tr>
      <tr>
        <td><strong>Financial Flow</strong></td>
        <td>PFMS</td>
        <td>Sanctioned Budget, Revised Estimate, Disbursed Tranches</td>
        <td>Detects unapproved cost escalation and drawdown speed</td>
      </tr>
      <tr>
        <td><strong>Physical Execution</strong></td>
        <td>eSAKSHI</td>
        <td>Physical Progress %, Milestone Targets, Delay Days</td>
        <td>Compares real civil work against financial expenditure</td>
      </tr>
      <tr>
        <td><strong>Contractor Profile</strong></td>
        <td>eSAKSHI / GST</td>
        <td>Company Name, PAN / Tax ID, Works Awarded</td>
        <td>Detects contractor monopolies & capacity overstretch</td>
      </tr>
      <tr>
        <td><strong>Geospatial Data</strong></td>
        <td>GIS / Survey of India</td>
        <td>Latitude & Longitude coordinates, elevation</td>
        <td>Haversine distance calculation to catch duplicate works</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- CHAPTER 3: NON-TECHNICAL TECH DICTIONARY -->
<div>
  <h2 class="section-header">CHAPTER 3: The Complete Non-Technical Tech Dictionary</h2>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 22%;">Technology / Term</th>
        <th style="width: 28%;">Simple Analogy</th>
        <th style="width: 50%;">Role in MPLADS AI Monitor</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>FastAPI</strong></td>
        <td>A super-fast waiter in a restaurant</td>
        <td>Modern, high-performance Python web framework delivering sub-15ms calculations between the screen and AI engine.</td>
      </tr>
      <tr>
        <td><strong>PostgreSQL</strong><br><em>("progestrate")</em></td>
        <td>An indestructible bank-grade digital filing cabinet</td>
        <td>Enterprise relational database safely organizing project tables, contractor PAN records, and payment tranches across 543 constituencies.</td>
      </tr>
      <tr>
        <td><strong>React</strong></td>
        <td>Interactive Lego blocks on screen</td>
        <td>Component-based frontend architecture ensuring numbers, charts, and alert tags update smoothly without full-page reloads.</td>
      </tr>
      <tr>
        <td><strong>Tailwind CSS</strong></td>
        <td>A professional designer toolbox</td>
        <td>Utility CSS framework providing official Government of India slate-blue headers, gold badges, and responsive metric cards.</td>
      </tr>
      <tr>
        <td><strong>REST API</strong></td>
        <td>A secure telephone wire</td>
        <td>Standardized communication protocol connecting website button clicks to backend Python analytics.</td>
      </tr>
      <tr>
        <td><strong>scikit-learn</strong></td>
        <td>A high-tech scientific toolbox</td>
        <td>Premier Python machine learning library powering Isolation Forest anomaly clustering and statistical outlier screening.</td>
      </tr>
      <tr>
        <td><strong>SHAP</strong></td>
        <td>Fair credit-sharing formula in a team</td>
        <td>Game-theory mathematical formula breaking down the 0–100 Explainable Risk Index into exact, auditable points per factor.</td>
      </tr>
      <tr>
        <td><strong>Image-Hash</strong></td>
        <td>A digital fingerprint for photos</td>
        <td>Converts photos into 64-bit perceptual hashes to detect recycled/fake completion photos submitted from past years.</td>
      </tr>
      <tr>
        <td><strong>RBAC</strong></td>
        <td>Government security ID badges</td>
        <td>Role-Based Access Control enforcing legal powers: MP recommendations, DM payment freezes, State benchmarking, MoSPI national oversight.</td>
      </tr>
      <tr>
        <td><strong>Haversine Formula</strong></td>
        <td>Spherical GPS distance formula</td>
        <td>Calculates the exact curved distance between two GPS coordinates to catch duplicate roads within 50 meters of existing schemes.</td>
      </tr>
      <tr>
        <td><strong>HHI Index</strong></td>
        <td>Monopoly & cartel detector</td>
        <td>Herfindahl-Hirschman Index used by the Competition Commission of India. Flags when one contractor corners $>35\%$ of block tenders.</td>
      </tr>
      <tr>
        <td><strong>S-Curve</strong></td>
        <td>Construction timeline graph</td>
        <td>Compares planned milestone baseline vs physical work vs money disbursed. Exposes when payments surge while work flatlines.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="page-break"></div>

<!-- CHAPTER 4: SLIDE-BY-SLIDE CONTENT & SCRIPTS -->
<div>
  <h2 class="section-header">CHAPTER 4: Complete Slide-by-Slide Presentation Deck & Scripts</h2>

  <!-- Slide 1 -->
  <h3 class="sub-header">SLIDE 1: Title Slide</h3>
  <p><strong>Title:</strong> MPLADS AI Monitor — Explainable AI-Based Project Risk & Anomaly Detection Platform<br>
  <strong>Nodal Organization:</strong> Ministry of Statistics and Programme Implementation (MoSPI) — DIID<br>
  <strong>Theme:</strong> Smart Governance, Public Financial Management & Anti-Corruption</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (30 Seconds):</span>
    "Respected jury members, every year the Government of India entrusts over ₹4,000 Crores to Members of Parliament under the MPLADS scheme to construct schools, community halls, roads, and drinking water plants. We are Team [Name], and we present <strong>MPLADS AI Monitor</strong>—a centralized, Explainable AI platform built for MoSPI to detect duplicate projects, inflated estimates, stalled funds, and contractor cartels in real-time."
  </div>

  <!-- Slide 2 -->
  <h3 class="sub-header">SLIDE 2: Problem Statement & Ground Realities</h3>
  <ul>
    <li><strong>Scale:</strong> ₹4,000+ Crore annual budget across 543 Lok Sabha and 245 Rajya Sabha constituencies.</li>
    <li><strong>The 3 Critical Leaks:</strong> The Phantom Asset (duplicate works), The ₹50,000 Pencil (financial-physical divergence), and The Forgotten Piggy Bank (stagnant idle funds).</li>
    <li><strong>The Core Flaw:</strong> eSAKSHI and PFMS operate in silos with no automated cross-verification. Manual CAG audits happen 2 to 3 years after money is spent.</li>
  </ul>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "Why does public money leak? Currently, progress is recorded in eSAKSHI, but payments are processed in PFMS. Because these systems don't talk to each other through automated AI checks, three major problems occur: 'The Phantom Asset' where an existing road is billed twice; 'The ₹50,000 Pencil' where 90% of funds are withdrawn for 38% physical work; and 'The Forgotten Piggy Bank' where funds sit idle for years. By the time a manual audit happens, the money is gone."
  </div>

  <!-- Slide 3 -->
  <h3 class="sub-header">SLIDE 3: Innovation & Uniqueness (The 5 Pillars)</h3>
  <ul>
    <li><strong>1. Explainable Risk Index (0–100):</strong> Quantified score with an auditable mathematical evidence trail behind every number.</li>
    <li><strong>2. Zero New Data Entry:</strong> Intelligent overlay on existing eSAKSHI and PFMS databases without creating extra forms.</li>
    <li><strong>3. Multi-Modal AI Engine:</strong> Evaluates Text (NLP), Cost (disbursement gap), Time (S-curve drift), and Image (perceptual hashing).</li>
    <li><strong>4. Role-Based Dashboards:</strong> 4 legally tailored portals for MP, District Authority (DM), State Nodal (SNA), and MoSPI.</li>
    <li><strong>5. 1-Click Investigation Workflow:</strong> Instantly freeze PFMS tranches, depute inspection teams, or generate official audit notices.</li>
  </ul>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "Our solution introduces five core innovations. First, the Explainable Risk Index—not a black-box number, but an auditable 0 to 100 score showing exactly why a project is risky. Second, Zero New Data Entry—we don't force busy officers to fill out more forms; our system ingests what eSAKSHI already captures. Third, Multi-Modal AI combining text, financial velocity, milestone timelines, and photo verification. Fourth, tailored dashboards for all four governance tiers. And fifth, a 1-click legal action workflow to stop payments immediately."
  </div>

  <!-- Slide 4 -->
  <h3 class="sub-header">SLIDE 4: End-to-End System Workflow</h3>
  <p><strong>11-Step Process:</strong> Data Capture $\rightarrow$ Normalization $\rightarrow$ 4 Parallel Checks (Duplicate, Cost, Stagnation, Image) $\rightarrow$ Risk Gate $\rightarrow$ XAI Evidence Modal $\rightarrow$ DM Review $\rightarrow$ PFMS Freeze / Inspection Order $\rightarrow$ Audit Dossier Generated $\rightarrow$ MoSPI & District Dashboards Updated.</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "Here is our closed-loop end-to-end workflow. When an agency files a milestone report in eSAKSHI, our AI immediately runs four parallel checks. If a project crosses the risk threshold, an alert is triggered in the District Magistrate's compliance queue with full evidence. The DM can immediately freeze subsequent tranches on PFMS and dispatch an inspection team. This turns an auditing process that used to take three years into a 30-second automated check."
  </div>

  <!-- Slide 5 -->
  <h3 class="sub-header">SLIDE 5: Technical Approach & Architecture</h3>
  <p><strong>4-Zone Architecture:</strong> Zone 1 (Data Ingestion) $\rightarrow$ Zone 2 (Presentation / UI) $\rightarrow$ Zone 3 (Backend FastAPI Microservices) $\rightarrow$ Zone 4 (AI Pipeline & SHAP Explainability).<br>
  <strong>Tech Stack:</strong> Python, FastAPI, Tailwind CSS, PostgreSQL, scikit-learn, SHAP, REST APIs.</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "Architecturally, our system is divided into four clean zones. Zone 1 ingests data from eSAKSHI and PFMS. Zone 2 is our lightweight, high-performance GovTech user interface. Zone 3 is powered by Python and FastAPI, handling authentication, role boundaries, and reporting microservices. Zone 4 is our AI pipeline calculating the Explainable Risk Index and contractor concentration metrics. The entire backend runs asynchronously, providing sub-15-millisecond response times."
  </div>

  <!-- Slide 6 -->
  <h3 class="sub-header">SLIDE 6: Explainable AI Engine & Mathematical Formulation</h3>
  <p><strong>Formula:</strong> ERI = 40% (Financial Gap) + 30% (Milestone Delay) + 15% (Haversine Duplicate Proximity) + 10% (Contractor HHI Cartel) + 5% (Cost Revision Claim).</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "How does our AI make decisions? We use an Explainable Risk Index composed of five weighted factors. 40% is allocated to the financial-physical mismatch—catching premature billing. 30% evaluates milestone stalling against the baseline S-curve. 15% uses the Haversine distance formula to flag identical road works within 50 meters of state projects. 10% uses the Herfindahl-Hirschman Index to detect contractor monopolies. And 5% flags unapproved budget revisions above the 10% statutory ceiling."
  </div>

  <!-- Slide 7 -->
  <h3 class="sub-header">SLIDE 7: Four Distinct Stakeholder Governance Portals</h3>
  <ul>
    <li><strong>Hon. MP:</strong> 15% SC and 7.5% ST social quota compliance + Gram Panchayat citizen petition inbox with LoR generation.</li>
    <li><strong>District Authority (DM):</strong> Compliance hub, field inspection dispatch, and PFMS payment tranche freezes.</li>
    <li><strong>State Nodal (SNA):</strong> Inter-district benchmarking across all 80 UP constituencies and delay cluster analytics.</li>
    <li><strong>MoSPI Central Ministry:</strong> Macro oversight across all 543 constituencies and national policy exception radar.</li>
  </ul>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "An MP needs different information than a District Magistrate or a Ministry Director. Our platform delivers four tailored views. For the MP, it tracks mandatory SC/ST social quotas and converts citizen petitions into formal recommendation letters. For the District Magistrate, it provides a compliance queue to depute inspection officers and freeze tranches. For the State Nodal Authority, it benchmarks all 80 UP constituencies. And for MoSPI, it provides a 543-constituency nationwide risk radar."
  </div>

  <!-- Slide 8 -->
  <h3 class="sub-header">SLIDE 8: Live Demonstration & Case Study (Varanasi PC-77)</h3>
  <p><strong>Project 1023 (Rohania CC Road):</strong> Sanctioned ₹78.50L $\rightarrow$ Disbursed ₹71.44L (91%) $\rightarrow$ Physical Progress 38% $\rightarrow$ 142 days delayed $\rightarrow$ <strong>ERI: 92/100 (Critical Risk)</strong>. DM freezes payment, orders inspection, and prints official MoSPI Audit Notice.</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (45 Seconds):</span>
    "Let's look at a live case study from our Varanasi pilot. Project 1023 is a CC Road in Rohania Block. PFMS shows that ₹71 Lakhs—91% of the budget—has already been paid out. But eSAKSHI records physical progress at only 38%, and the site is 142 days overdue. Our AI flagged this project with a Critical Risk score of 92. In our investigation modal, the DM can view the S-curve divergence, freeze the next payment tranche on PFMS, and generate an official statutory audit notice in one click."
  </div>

  <!-- Slide 9 -->
  <h3 class="sub-header">SLIDE 9: Feasibility, Economic & Social Impact</h3>
  <ul>
    <li><strong>Zero New Hardware:</strong> Connects existing eSAKSHI APIs and PFMS webhooks.</li>
    <li><strong>Economic Return:</strong> Stops double billing and premature contractor drain before treasury disbursement.</li>
    <li><strong>Social Justice:</strong> Strictly enforces statutory 15% SC and 7.5% ST sub-plan quotas for marginalized communities.</li>
  </ul>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (30 Seconds):</span>
    "What is the impact of our solution? First, zero new hardware—our software works with existing eSAKSHI and PFMS databases. Second, massive financial savings by eliminating duplicate works and stopping premature contractor billing before money leaves the treasury. And third, social accountability—ensuring that mandatory 15% SC and 7.5% ST quotas are genuinely spent on community infrastructure."
  </div>

  <!-- Slide 10 -->
  <h3 class="sub-header">SLIDE 10: Future Roadmap & Conclusion</h3>
  <p>Phase 1 (Varanasi PC-77 Pilot Completed) $\rightarrow$ Phase 2 (Statewide 80 UP PCs with automated SMS alerts) $\rightarrow$ Phase 3 (Pan-India 543 PCs integrated with ISRO / Bhuvan Satellite SAR Imagery).<br>
  <strong>Repository:</strong> github.com/dhanya808/mplads-ai-monitor</p>
  <div class="speaker-script">
    <span class="speaker-badge">Speaker Script (30 Seconds):</span>
    "Looking ahead, Phase 1 is fully functional and ready today. In Phase 2, we will scale across all 80 constituencies of Uttar Pradesh with automated SMS alerts. In Phase 3, we will connect ISRO Bhuvan satellite imagery to automatically verify road completions from orbit across all 543 constituencies. Thank you, and we are now eager to take your questions!"
  </div>
</div>

<div class="page-break"></div>

<!-- CHAPTER 5 & 6: WEBPAGE WALKTHROUGH & JURY DEFENSE -->
<div>
  <h2 class="section-header">CHAPTER 5: The 2-Minute Winning Live Demo Script</h2>
  <ol>
    <li><strong>(0:00 - 0:20) Step 1: Sign In:</strong> Log into <code>/login</code> using the District Magistrate demo card.</li>
    <li><strong>(0:20 - 0:50) Step 2: Spotting the Anomaly:</strong> Point out 4 High-Risk projects in the KPI cards and show Project <code>#MPLADS-UP-VAR-1023</code> with Critical Risk Score 92 in the Anomaly Feed.</li>
    <li><strong>(0:50 - 1:20) Step 3: Deep Investigation:</strong> Click "Investigate →". Walk through the 5-factor Radar breakdown, show the S-Curve (payments at 91% while physical work flatlined at 38%), and the 35m duplicate proximity alert.</li>
    <li><strong>(1:20 - 1:40) Step 4: Enforcement Action:</strong> Check "Freeze subsequent disbursements in PFMS", depute the Executive Engineer, and click "Print Official Statutory Audit Notice" to show the print-ready MoSPI dossier.</li>
    <li><strong>(1:40 - 2:00) Step 5: The Other Roles:</strong> Switch to the MP's view to demonstrate 15% SC and 7.5% ST quota compliance and citizen LoR dispatch. Switch to MoSPI for national macro oversight.</li>
  </ol>

  <h2 class="section-header">CHAPTER 6: Jury Q&A Defense Master Sheet</h2>

  <div class="callout">
    <strong>Q1: "Why not use a Deep Learning neural network?"</strong><br>
    <em>"In government administration, an administrative officer cannot legally freeze a government payment or issue a contractor show-cause notice based on an unexplainable neural network probability. Courts and tribunals require auditable legal evidence. Our Explainable Risk Index breaks down the exact mathematical points (e.g. 40 pts progress mismatch, 30 pts delay, 15 pts duplicate proximity), which are directly cited in the statutory audit notice."</em>
  </div>

  <div class="callout">
    <strong>Q2: "How do you detect duplicate works?"</strong><br>
    <em>"We ingest GPS coordinates from project proposals and calculate the Haversine distance against external government databases (like PMGSY and State Road packages). If a proposed road or drain is within 50 meters of an existing asset with a matching description, it is flagged as a potential duplicate before funds are sanctioned."</em>
  </div>

  <div class="callout">
    <strong>Q3: "Is this practical to implement in the real world?"</strong><br>
    <em>"Yes, 100% practical because it requires <strong>zero new hardware</strong>. Engineers already enter progress into eSAKSHI, and accountants already disburse money in PFMS. We simply connect these two existing databases with an intelligent API layer that runs automated checks."</em>
  </div>

  <div class="callout">
    <strong>Q4: "What is Contractor Cartel Risk and why does it matter?"</strong><br>
    <em>"When one contractor wins 5 different tenders across adjacent blocks, they run out of concrete mixers, shuttering, and laborers. They take the initial 80% payment and leave the works stalled for 140+ days. Our HHI algorithm detects this monopoly so the District Authority can prevent over-allocation."</em>
  </div>

  <div class="callout">
    <strong>Q5: "What is the difference between eSAKSHI and your platform?"</strong><br>
    <em>"eSAKSHI is a <strong>data-entry portal</strong>; it records what engineers type. <strong>MPLADS AI Monitor is the intelligence layer</strong>; it analyzes what was entered, checks it against financial disbursements on PFMS, detects anomalies, and alerts the DM before public money leaks."</em>
  </div>
</div>

</body>
</html>
"""

with open("master_guide_print.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML document created successfully!")

# Find browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
browser = chrome_path if os.path.exists(chrome_path) else edge_path

html_abs = os.path.abspath("master_guide_print.html")
pdf_out = os.path.abspath("MPLADS_AI_Monitor_SIH_Master_Guide.pdf")

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_out}",
    "--no-pdf-header-footer",
    html_abs
]

print(f"Generating PDF with {browser}...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_out):
    print(f"PDF successfully generated: {pdf_out} (Size: {os.path.getsize(pdf_out)} bytes)")
else:
    print(f"PDF generation failed: {res.stderr}")
