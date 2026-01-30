import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantaSchedina - Home", layout="wide")

# CSS di ieri: Sfondo chiaro, bottoni gialli e sidebar ordinata [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
    }
    .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR [cite: 2026-01-29]
with st.sidebar:
    st.markdown("## 🏆 FantaSchedina")
    st.divider()
    if st.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    if st.button("⚽ Gioca", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

# AREA LOGIN CENTRATA [cite: 2026-01-29]
st.markdown("<br><br>", unsafe_allow_html=True)
col_l, col_main, col_r = st.columns([1, 1.2, 1])

with col_main:
    st.markdown("<h1 style='text-align: center;'>BENVENUTO</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("ACCEDI", use_container_width=True, type="primary"):
            st.success("Accesso in corso...")
