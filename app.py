import streamlit as st
from supabase import create_client

# Configurazione della pagina
st.set_page_config(page_title="FantaSchedina - Home", layout="wide")

# Inizializzazione Supabase (Assicurati che i segreti siano corretti)
if "supabase" not in st.session_state:
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        st.session_state.supabase = create_client(url, key)
    except:
        st.error("Configura i segreti di Supabase per continuare.")

# CSS Professionale di ieri: Giallo per i bottoni e pulizia sidebar [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
    }
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 40px;
        background: white;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR [cite: 2026-01-29]
with st.sidebar:
    st.title("🏆 FantaSchedina")
    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    if st.button("⚽ Gioca", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

# AREA LOGIN
st.markdown("<br><br>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns([1, 1.2, 1])

with col_b:
    st.markdown("<h2 style='text-align: center;'>BENVENUTO</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("ACCEDI", use_container_width=True, type="primary"):
            st.info("Accesso in corso...")
