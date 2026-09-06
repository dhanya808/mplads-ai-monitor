"""
MPLADS AI Monitor - Primary Command Center & Dashboard
Ministry of Statistics and Programme Implementation (MoSPI)
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.dataset_generator import generate_mplads_dataset
from backend.ml_engine import process_mplads_anomalies

st.set_page_config(page_title="MPLADS AI Monitor | Command Center", page_icon="🏛️", layout="wide")

# Check authentication
if not st.session_state.get('logged_in', False):
    st.switch_page("app.py")

DATA_FILE = os.path.join(BASE_DIR, "data", "mplads_processed.csv")

@st.cache_data
def get_dashboard_data():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        raw_df = generate_mplads_dataset(200)
        processed_df = process_mplads_anomalies(raw_df)
        processed_df.to_csv(DATA_FILE, index=False)
        return processed_df
    return pd.read_csv(DATA_FILE)

df = get_dashboard_data()
role = st.session_state.get('user_role', 'MoSPI')

# Styling
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
    .kpi-sub { font-size: 11px; color: #64748B; margin-top: 2px; }
    
    .constituency-banner {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .tag-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .tag-parliament {
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
    }
    .tag-live {
        color: #475569;
        font-size: 12px;
        font-weight: 500;
    }
    .feed-card {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        background: #FFFFFF;
        transition: transform 0.1s ease;
    }
    .feed-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .badge-delayed {
        border: 1px solid #FCA5A5;
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# TOP NAVIGATION BAR
# ----------------------------------------------------------------------
nav_col1, nav_col2 = st.columns([4, 1])
with nav_col1:
    st.markdown(f"## **MPLADS AI Monitor** | {role} Portal")
    if role == "District Authority":
        st.caption("Active Scope: **Coimbatore District Jurisdiction**")
    elif role == "Member of Parliament":
        st.caption("Active Scope: **Varanasi Parliamentary Constituency (PC-77)**")
    elif role == "State Nodal Authority":
        st.caption("Active Scope: **Tamil Nadu State Division**")
    else:
        st.caption("Active Scope: **National Oversight (All States & UTs)**")

with nav_col2:
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.switch_page("app.py")

# ----------------------------------------------------------------------
# CONSTITUENCY BANNER (Images 4 & 1)
# ----------------------------------------------------------------------
if role == "Member of Parliament":
    st.markdown("""
    <div class="constituency-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span class="tag-badge tag-parliament">CONSTITUENCY MONITORING PORTAL</span>
                <span style="color: #64748b; font-size: 12px; margin-left: 8px; font-weight: 600;">18th Lok Sabha • 2024–2029</span>
                <h2 style="margin: 8px 0 2px 0; color: #0f172a; font-size: 22px; font-weight: 800;">Varanasi Parliamentary Constituency (PC-77)</h2>
                <span style="color: #475569; font-size: 13px;"><b>Member of Parliament:</b> Hon. Rajeshwar Verma • <b>District:</b> Varanasi, Uttar Pradesh</span>
            </div>
            <div style="text-align: right;">
                <span class="tag-live">Last Synchronized <b>Today, 06:00 IST (Live)</b></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SCOPE DATASET FILTERING
# ----------------------------------------------------------------------
if role == "District Authority":
    scope_df = df[df['district'] == "Coimbatore"].copy()
elif role == "Member of Parliament":
    scope_df = df[df['district'] == "Varanasi"].copy()
elif role == "State Nodal Authority":
    scope_df = df[df['state'] == "Tamil Nadu"].copy()
else:
    scope_df = df.copy()

# ----------------------------------------------------------------------
# TOP KPI METRICS ROW
# ----------------------------------------------------------------------
if role == "Member of Parliament":
    total_projects = len(scope_df)
    sanctioned_lakhs = scope_df['sanction_amount'].sum() / 1e5
    expenditure_lakhs = scope_df['expenditure'].sum() / 1e5
    completed = len(scope_df[scope_df['status'] == 'Completed'])
    ongoing = len(scope_df[scope_df['status'] == 'Ongoing'])
    high_risk = len(scope_df[scope_df['risk_tier'].isin(['Critical', 'High'])])
    delayed = len(scope_df[scope_df['delay_flag'] == 'Stagnant / Delayed'])

    k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">TOTAL PROJECTS</div><div class="kpi-val">{total_projects}</div><div class="kpi-sub">Recommended 2024-25</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">SANCTIONED</div><div class="kpi-val" style="color: #1d4ed8;">₹{sanctioned_lakhs:.2f} L</div><div class="kpi-sub" style="color: #16a34a;">100% entitlement drawn</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">EXPENDITURE</div><div class="kpi-val">₹{expenditure_lakhs:.2f} L</div><div class="kpi-sub">{expenditure_lakhs/max(1, sanctioned_lakhs)*100:.1f}% fund utilization</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">COMPLETED</div><div class="kpi-val" style="color: #16a34a;">{completed}</div><div class="kpi-sub">Handed over & geo-tagged</div></div>', unsafe_allow_html=True)
    with k5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">ONGOING</div><div class="kpi-val" style="color: #2563eb;">{ongoing}</div><div class="kpi-sub">Under civil execution</div></div>', unsafe_allow_html=True)
    with k6:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">HIGH-RISK</div><div class="kpi-val" style="color: #dc2626;">{high_risk}</div><div class="kpi-sub" style="color: #ea580c;">Inspection advised</div></div>', unsafe_allow_html=True)
    with k7:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">DELAYED (&gt;30D)</div><div class="kpi-val" style="color: #d97706;">{delayed}</div><div class="kpi-sub" style="color: #dc2626;">1 Critical anomalies</div></div>', unsafe_allow_html=True)
else:
    # National / State / District Overview Cards (Image 3)
    total_projects = len(scope_df)
    sanctioned_cr = scope_df['sanction_amount'].sum() / 1e7
    critical_count = len(scope_df[scope_df['risk_tier'] == 'Critical'])
    delayed_count = len(scope_df[scope_df['delay_flag'] == 'Stagnant / Delayed'])

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">TOTAL ACTIVE PROJECTS</div><div class="kpi-val">{total_projects}</div><div class="kpi-sub">Monitored Nationwide</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">SANCTIONED OUTLAY</div><div class="kpi-val">₹{sanctioned_cr:.2f} Cr</div><div class="kpi-sub">Central Sector Outlay</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">CRITICAL RISK WORKS</div><div class="kpi-val" style="color: #DC2626;">{critical_count}</div><div class="kpi-sub" style="color: #DC2626;">Immediate Audit Required</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">STAGNANT / DELAYED</div><div class="kpi-val" style="color: #D97706;">{delayed_count}</div><div class="kpi-sub" style="color: #D97706;">Exceeding Statutory Limits</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 4-COLUMN HORIZONTAL FILTER BAR COMPONENT (Image 4)
# ----------------------------------------------------------------------
st.markdown('<div class="kpi-card" style="margin-bottom: 20px;">', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown('<b>Project Status</b>', unsafe_allow_html=True)
    status_choices = ["All Statuses (Ongoing & Completed)"] + sorted(scope_df['status'].unique().tolist())
    selected_status = st.selectbox("Status", status_choices, label_visibility="collapsed")

with f2:
    st.markdown('<b>Block / Location</b>', unsafe_allow_html=True)
    location_choices = ["All Locations"] + sorted(scope_df['block'].unique().tolist())
    selected_location = st.selectbox("Location", location_choices, label_visibility="collapsed")

with f3:
    st.markdown('<b>Sector / Project Type</b>', unsafe_allow_html=True)
    sector_choices = ["All Sectors"] + sorted(scope_df['category'].unique().tolist())
    selected_sector = st.selectbox("Sector", sector_choices, label_visibility="collapsed")

with f4:
    st.markdown('<b>AI Risk Level</b>', unsafe_allow_html=True)
    risk_choices = ["All Risk Tiers", "Critical", "High", "Medium", "Low"]
    selected_risk = st.selectbox("Risk Tier", risk_choices, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# Apply Filters
filtered_df = scope_df.copy()
if selected_status != "All Statuses (Ongoing & Completed)":
    filtered_df = filtered_df[filtered_df['status'] == selected_status]
if selected_location != "All Locations":
    filtered_df = filtered_df[filtered_df['block'] == selected_location]
if selected_sector != "All Sectors":
    filtered_df = filtered_df[filtered_df['category'] == selected_sector]
if selected_risk != "All Risk Tiers":
    filtered_df = filtered_df[filtered_df['risk_tier'] == selected_risk]

# ----------------------------------------------------------------------
# ANALYTICS SECTION (Financial Utilization & Sector Donut) (Image 1)
# ----------------------------------------------------------------------
c_left, c_right = st.columns(2)

with c_left:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown("### **Financial Utilization vs Allocation**")
    st.caption("Sanctioned vs Actual Expenditure across Key Works (₹ in Lakhs)")
    
    # Financial bar chart data
    total_sanct_lakhs = filtered_df['sanction_amount'].sum() / 1e5
    total_rev_lakhs = filtered_df['revised_estimate'].sum() / 1e5
    total_act_lakhs = filtered_df['expenditure'].sum() / 1e5
    
    fin_df = pd.DataFrame({
        "Allocation Metric": ["Sanctioned Allocation", "Revised Estimate", "Actual Expenditure"],
        "Amount (₹ Lakhs)": [round(total_sanct_lakhs, 2), round(total_rev_lakhs, 2), round(total_act_lakhs, 2)]
    })
    st.bar_chart(data=fin_df, x="Allocation Metric", y="Amount (₹ Lakhs)", color="Allocation Metric")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown("### **Constituency Sector Distribution**")
    st.caption("Share of MPLADS funds by sector category")
    
    sector_summary = filtered_df.groupby('category')['sanction_amount'].sum().reset_index()
    sector_summary['Sanctioned (₹ Lakhs)'] = round(sector_summary['sanction_amount'] / 1e5, 1)
    
    # Render interactive sector bar / donut summary
    st.bar_chart(data=sector_summary, x="category", y="Sanctioned (₹ Lakhs)", color="category")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# AUTOMATED AUDIT FEED & MILESTONE DEADLINES (Image 1)
# ----------------------------------------------------------------------
f_left, f_right = st.columns(2)

with f_left:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown("### 🔔 **Recent AI Anomaly Detections**")
    st.caption("Automated Audit Feed")
    
    feed_items = [
        {
            "id": "MPLADS-UP-VAR-1023",
            "title": "Expenditure/Physical Progress Mismatch",
            "desc": "Disbursement of 91% funds with only 38% physical work done. 142 days delayed past targeted milestone.",
            "date": "2025-02-18",
            "status": "New",
            "badge_color": "#DC2626",
            "proj_ref": "MPLAD-1023"
        },
        {
            "id": "MPLADS-UP-VAR-6088",
            "title": "Possible Duplicate Project",
            "desc": "High spatial proximity (35m) with State Gram Sadak road project #UP-RD-2023-901 on same alignment.",
            "date": "2025-02-05",
            "status": "New",
            "badge_color": "#EA580C",
            "proj_ref": "MPLAD-1002"
        },
        {
            "id": "MPLADS-UP-VAR-2211",
            "title": "Premature Billing",
            "desc": "96.8% funds billed, but 4 plants lack power and remain un-commissioned.",
            "date": "2025-01-28",
            "status": "Under Investigation",
            "badge_color": "#D97706",
            "proj_ref": "MPLAD-1018"
        },
        {
            "id": "MPLADS-UP-VAR-3045",
            "title": "Cost Revision Claim",
            "desc": "20.9% budget increase claimed for foundation excavation without geological soil proof.",
            "date": "2025-01-20",
            "status": "New",
            "badge_color": "#EA580C",
            "proj_ref": "MPLAD-1038"
        }
    ]

    for item in feed_items:
        st.markdown(f"""
        <div class="feed-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 700; color: #0F172A;"><span style="color: {item['badge_color']};">●</span> {item['id']}</span>
                <span style="font-size: 11px; color: #64748B;">{item['date']}</span>
            </div>
            <div style="font-weight: 600; color: #1E293B; margin-top: 4px; font-size: 14px;">{item['title']}</div>
            <div style="color: #64748B; font-size: 12px; margin-top: 2px;">{item['desc']}</div>
            <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 600; background: #F1F5F9; padding: 2px 8px; border-radius: 4px; color: #475569;">Status: {item['status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Investigate → ({item['id']})", key=f"inv_btn_{item['id']}"):
            st.session_state.selected_project = item['proj_ref']
            st.switch_page("pages/2_Investigation.py")

    st.markdown('</div>', unsafe_allow_html=True)

with f_right:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown("### 📅 **Milestone Schedule & Target Deadlines**")
    st.caption("Upcoming Completion Targets & Delay Flags")
    
    milestones = [
        {
            "name": "Construction of 2.4 km CC Road with RCC Drain & Solar Lighting",
            "target": "2025-02-15",
            "contractor": "Ganga Valley Engineering Associates",
            "delay": "142d Delayed",
            "done": "38% Done"
        },
        {
            "name": "Installation of 8 High-Capacity RO Water Purification Plants with Chillers",
            "target": "2025-01-30",
            "contractor": "M/s पूर्वांचल इन्फ्राटेक Pvt Ltd",
            "delay": "78d Delayed",
            "done": "52% Done"
        },
        {
            "name": "Community Hall & Multi-Skill Youth Training Facility at Sevapuri",
            "target": "2025-03-15",
            "contractor": "Kashi Construction & Civil Works",
            "delay": "95d Delayed",
            "done": "45% Done"
        },
        {
            "name": "Construction of Solar Mini-Grid & LED Illumination for Ramnagar Ghats",
            "target": "2025-05-30",
            "contractor": "Kashi Jal Shuddhikkaran Solutions",
            "delay": "14d Delayed",
            "done": "50% Done"
        }
    ]

    for m in milestones:
        st.markdown(f"""
        <div class="feed-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-weight: 600; color: #0F172A; font-size: 14px; max-width: 75%;">{m['name']}</div>
                <span class="badge-delayed">{m['delay']}</span>
            </div>
            <div style="color: #64748B; font-size: 12px; margin-top: 4px;">
                Target Date: <b>{m['target']}</b> • Contractor: {m['contractor']}
            </div>
            <div style="text-align: right; font-weight: 700; color: #1E293B; font-size: 13px; margin-top: 4px;">
                {m['done']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# PRIORITY ANOMALY DETECTION QUEUE (Images 2 & 3)
# ----------------------------------------------------------------------
st.subheader("Priority Anomaly Detection Queue")
st.caption("Projects prioritized by the AI Risk Scoring Engine (incorporating cost variance, semantic duplication, and timeline metrics).")

sorted_df = filtered_df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)

for idx, row in sorted_df.head(15).iterrows():
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([1.5, 3.5, 1.5, 2.0, 1.5])
        
        score_color = "#DC2626" if row['risk_score'] >= 85 else ("#EA580C" if row['risk_score'] >= 60 else "#16A34A")
        
        with c1:
            st.markdown(f"""
                <div style="padding-top: 4px;">
                    <b style="font-size: 15px; color: #0F172A;">{row['project_id']}</b><br>
                    <span style="color: {score_color}; font-weight: 700; font-size: 13px;">Score: {row['risk_score']}/100</span>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div>
                    <b style="font-size: 15px; color: #0F172A;">{row['work_name']}</b><br>
                    <span style="color: #64748B; font-size: 12px;">{row['district']}, {row['state']} • Category: {row['category']}</span>
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div>
                    <b style="font-size: 15px; color: #0F172A;">₹{row['sanction_amount']:,.1f}</b><br>
                    <span style="font-size: 12px; color: #64748B;">Progress: {row['physical_progress_pct']}%</span>
                </div>
            """, unsafe_allow_html=True)
            
        with c4:
            badges = []
            if row['cost_anomaly_flag'] == "High Outlier" or row.get('cost_deviation_pct', 0) > 40:
                badges.append(f"<div style='background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; border: 1px solid #FCA5A5; margin-bottom: 4px; display: inline-block;'>Cost Deviation: +{row['cost_deviation_pct']}%</div>")
            if row['duplicate_flag'] == "Duplicate Alert" or row.get('duplicate_similarity_pct', 0) >= 70:
                badges.append(f"<div style='background-color: #F3E8FF; color: #6B21A8; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; border: 1px solid #D8B4FE; margin-bottom: 4px; display: inline-block;'>Duplicate Match: {row['duplicate_similarity_pct']}%</div>")
            if row['delay_flag'] == "Stagnant / Delayed" or row.get('days_since_sanction', 0) >= 365:
                badges.append(f"<div style='background-color: #FEF3C7; color: #92400E; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; border: 1px solid #FCD34D; margin-bottom: 4px; display: inline-block;'>Timeline Delay: &gt;365d</div>")
            if not badges:
                badges.append(f"<div style='background-color: #DCFCE7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; border: 1px solid #86EFAC; margin-bottom: 4px; display: inline-block;'>Status: Nominal</div>")
                
            st.markdown("<br>".join(badges), unsafe_allow_html=True)
            
        with c5:
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Inspect Audit", key=f"inspect_queue_{row['project_id']}", use_container_width=True):
                st.session_state.selected_project = row['project_id']
                st.switch_page("pages/2_Investigation.py")
                
        st.divider()
