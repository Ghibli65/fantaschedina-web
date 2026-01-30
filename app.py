import streamlit as st
from supabase import create_client

# Configurazione iniziale
st.set_page_config(page_title="FantaSchedina - Login", layout="wide")

# Collegamento Supabase
if "supabase" not in st.session_state:
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        st.session_state.supabase = create_client(url, key)
    except Exception as e:
        st.error("Errore configurazione Database. Controlla i Secrets!")

# CSS per pulizia e bottoni gialli [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    .login-box {
        max-width: 450px;
        margin: auto;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR [cite: 2026-01-29]
with st.sidebar:
    st.title("🏆 FantaSchedina")
    st.button("🏠 Home / Login", use_container_width=True, type="primary")
    if st.button("⚽ Vai al Palinsesto", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

# CORPO CENTRALE
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col_mid, col3 = st.columns([1, 1.5, 1])

with col_mid:
    st.markdown("<h1 style='text-align:center;'>BENVENUTO</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("ACCEDI AL CAMPIONATO", use_container_width=True, type="primary"):
            st.info("Verifica credenziali...")
