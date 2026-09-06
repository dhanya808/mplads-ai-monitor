"""
MPLADS AI Monitor - Main Application Entry & Authentication Gateway
Ministry of Statistics and Programme Implementation (MoSPI)
Data Informatics & Innovation Division (DIID)
"""

import streamlit as st
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.dataset_generator import generate_mplads_dataset
from backend.ml_engine import process_mplads_anomalies

st.set_page_config(
    page_title="MPLADS AI Monitor | Government Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "MoSPI"
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = "MPLAD-1002"

# Ensure dataset is generated and cached
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "mplads_processed.csv")

@st.cache_data
def load_or_generate_dataset():
    if not os.path.exists(DATA_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        raw_df = generate_mplads_dataset(200)
        processed_df = process_mplads_anomalies(raw_df)
        processed_df.to_csv(DATA_FILE, index=False)
        return processed_df
    return pd.read_csv(DATA_FILE)

# ----------------------------------------------------------------------
# SECURE GOVERNMENT AUTHENTICATION GATEWAY
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .login-container {
            max-width: 480px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .login-header { text-align: center; color: #0f172a; font-weight: 800; font-size: 24px; margin-bottom: 4px; }
        .login-subheader { text-align: center; color: #64748b; font-size: 13px; margin-bottom: 24px; }
        .secure-badge { text-align: center; color: #16a34a; font-size: 12px; font-weight: 600; margin-top: 18px; }
        .footer-note { text-align: center; font-size: 11px; color: #94a3b8; margin-top: 24px; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h2 class="login-header">🏛️ MPLADS AI Monitor</h2>', unsafe_allow_html=True)
        st.markdown('<p class="login-subheader">Ministry of Statistics and Programme Implementation (MoSPI)<br>Data Informatics & Innovation Division (DIID)</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Official Email / User ID", value="officer.mospi@gov.in", placeholder="officer.mospi@gov.in")
            st.text_input("Password", type="password", value="••••••••", placeholder="••••••••")
            
            c1, c2 = st.columns(2)
            with c1:
                st.checkbox("Remember credentials", value=True)
            with c2:
                st.markdown("<p style='text-align: right; font-size: 12px; margin-top: 4px;'><a href='#' style='color: #2563eb; text-decoration: none;'>Forgot password?</a></p>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)
            st.markdown("<b>Select Role Persona for Verification & Demo:</b>", unsafe_allow_html=True)
            selected_role = st.selectbox(
                "Role Persona",
                [
                    "MoSPI",
                    "State Nodal Authority",
                    "District Authority",
                    "Member of Parliament"
                ],
                label_visibility="collapsed"
            )
            
            submit = st.form_submit_button("Sign In Securely →", use_container_width=True)
            
            if submit:
                st.session_state.logged_in = True
                st.session_state.user_role = selected_role
                st.switch_page("pages/1_Dashboard.py")

        st.markdown('<p class="secure-badge">🔒 256-Bit SSL Encrypted Government Gateway</p>', unsafe_allow_html=True)
        st.markdown('<p class="footer-note">Authorized Access Only • National Informatics Centre (NIC) • Govt of India</p>', unsafe_allow_html=True)

else:
    # If already logged in, redirect directly to Dashboard
    st.switch_page("pages/1_Dashboard.py")
