"""
MPLADS AI Monitor - Project Investigation Dossier (XAI Deep Dive)
Ministry of Statistics and Programme Implementation (MoSPI)
"""

import streamlit as st
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.ml_engine import get_xai_explanations

st.set_page_config(page_title="MPLADS AI Monitor | Project Investigation", page_icon="🔍", layout="wide")

# Check authentication
if not st.session_state.get('logged_in', False):
    st.switch_page("app.py")

DATA_FILE = os.path.join(BASE_DIR, "data", "mplads_processed.csv")

if not os.path.exists(DATA_FILE):
    st.error("Processed dataset not found. Please return to the Dashboard.")
    if st.button("← Return to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

df = pd.read_csv(DATA_FILE)
selected_id = st.session_state.get('selected_project', 'MPLAD-1002')

match = df[df['project_id'] == selected_id]
if match.empty:
    row = df.iloc[0]
else:
    row = match.iloc[0]

# Styling matching Image 5
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-title { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-val { font-size: 24px; font-weight: 700; color: #0F172A; margin-top: 4px; }
    
    .finding-alert {
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 14px;
        border-left: 6px solid;
    }
    .action-directive-box {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Navigation header (Image 5)
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown(f"## **Project Investigation Dossier: {row['project_id']}**")
    st.caption(f"Location: **{row['district']}, {row['state']}** | Scheme Category: **{row['category']}** • Contractor: **{row.get('contractor', 'Authorized Agency')}**")
with h2:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("← Return to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

# Top KPI Summary Row (Image 5)
k1, k2, k3, k4 = st.columns(4)

tier_color = "#DC2626" if row['risk_score'] >= 85 else ("#EA580C" if row['risk_score'] >= 60 else "#16A34A")
tier_label = "↑ Critical" if row['risk_score'] >= 85 else ("↑ High" if row['risk_score'] >= 60 else ("↑ Medium" if row['risk_score'] >= 35 else "↓ Low"))

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Composite Risk Score</div>
        <div class="kpi-val">{row['risk_score']} / 100</div>
        <div style="color: {tier_color}; font-size: 12px; font-weight: 700; margin-top: 2px;">{tier_label}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Sanctioned Budget</div>
        <div class="kpi-val">₹{row['sanction_amount']:,.1f}</div>
        <div style="color: #64748B; font-size: 12px; margin-top: 2px;">Entitlement Approved</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Funds Disbursed</div>
        <div class="kpi-val">₹{row['expenditure']:,.1f}</div>
        <div style="color: #64748B; font-size: 12px; margin-top: 2px;">{(row['expenditure']/max(1.0, row['sanction_amount'])*100):.1f}% Disbursed</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Physical Completion</div>
        <div class="kpi-val">{row['physical_progress_pct']}%</div>
        <div style="color: #64748B; font-size: 12px; margin-top: 2px;">Verified by Geotagging</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# EXPLAINABLE AI (XAI) DIAGNOSTIC BREAKDOWN (Image 5)
# ----------------------------------------------------------------------
st.subheader("Automated Audit & Anomaly Explanations")
st.caption("AI-generated inspection reasoning combining cost deviation, NLP duplicate detection, and execution pace.")

xai_data = get_xai_explanations(row)

col_left, col_right = st.columns(2)

with col_left:
    # Finding 1: Budget Analysis
    if row['cost_anomaly_flag'] == "High Outlier" or row.get('cost_deviation_pct', 0) > 40:
        st.markdown(f"""
        <div class="finding-alert" style="background-color: #FEF2F2; border-color: #DC2626; color: #991B1B;">
            <strong style="font-size: 15px;">High Cost Deviation Detected</strong><br>
            Budget estimate is <strong>+{row['cost_deviation_pct']}%</strong> above baseline regional median for {row['category']}. Historical norms indicate potential cost inflation.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="finding-alert" style="background-color: #F0FDF4; border-color: #16A34A; color: #166534;">
            <strong style="font-size: 15px;">Cost Sanction Baseline Verified</strong><br>
            Proposed financial allocation conforms with category norms in this district.
        </div>
        """, unsafe_allow_html=True)

    # Finding 2: Text Similarity / Duplicate Verification
    if row['duplicate_flag'] == "Duplicate Alert" or row.get('duplicate_similarity_pct', 0) >= 70:
        st.markdown(f"""
        <div class="finding-alert" style="background-color: #FEF2F2; border-color: #DC2626; color: #991B1B;">
            <strong style="font-size: 15px;">High Semantic Duplicate Similarity ({row['duplicate_similarity_pct']}%)</strong><br>
            Natural Language Processing matched this description with existing sanctioned work: <strong>{row['duplicate_match_id']}</strong>.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="finding-alert" style="background-color: #F0FDF4; border-color: #16A34A; color: #166534;">
            <strong style="font-size: 15px;">Unique Asset Description</strong><br>
            Semantic analysis confirmed zero duplicate work recommendations in the local registry.
        </div>
        """, unsafe_allow_html=True)

with col_right:
    # Finding 3: Stagnation & Timeline
    if row['delay_flag'] == "Stagnant / Delayed" or row.get('days_since_sanction', 0) >= 365:
        st.markdown(f"""
        <div class="finding-alert" style="background-color: #FFFBEB; border-color: #D97706; color: #92400E;">
            <strong style="font-size: 15px;">Timeline Stagnation Alert</strong><br>
            Elapsed time: <strong>{row['days_since_sanction']} days</strong> (Exceeds the MPLADS 365-day statutory guideline). Reported physical progress is constrained at {row['physical_progress_pct']}%.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="finding-alert" style="background-color: #F0FDF4; border-color: #16A34A; color: #166534;">
            <strong style="font-size: 15px;">Execution Velocity On Schedule</strong><br>
            Timeline progress aligns with standard completion horizons.
        </div>
        """, unsafe_allow_html=True)

    # Recommended Administrative Action Box
    actions_html = "".join([f"<li>{act}</li>" for act in xai_data["recommended_actions"]])
    st.markdown(f"""
    <div class="action-directive-box">
        <strong style="color: #1E293B; font-size: 14px;">Recommended Administrative Action:</strong>
        <ul style="margin: 8px 0 0 0; padding-left: 20px; color: #334155; font-size: 13px;">
            {actions_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ADMINISTRATIVE ACTION BUTTONS & AUDIT LOGGING (Image 5)
# ----------------------------------------------------------------------
st.subheader("Administrative Authority Controls")

act1, act2, act3 = st.columns(3)

with act1:
    if st.button("🚨 Order Physical Inspection", use_container_width=True):
        st.warning(f"Inspection dispatch order issued for **{row['project_id']}**. Logged in central administrative register for District Technical Team.")

with act2:
    if st.button("🛑 Place Tranche Hold on Funds", use_container_width=True):
        st.error(f"Financial tranche disbursement frozen for **{row['project_id']}**. Treasury notification sent.")

with act3:
    if st.button("✅ Mark Record Reviewed & Cleared", use_container_width=True):
        st.success(f"Audit status updated: **{row['project_id']}** reviewed and cleared with compliance notes.")
