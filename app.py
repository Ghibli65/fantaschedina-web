import streamlit as st

st.set_page_config(page_title="FantaSchedina - Home", layout="wide")

# CSS per i bottoni GIALLI e la pulizia sidebar [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🏆 FantaSchedina")
    st.divider()
    if st.button("🏠 Home / Login", use_container_width=True, type="primary"):
        st.rerun()
    if st.button("⚽ Gioca Ora", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

# Layout Login [cite: 2026-01-29]
st.markdown("<br><br>", unsafe_allow_html=True)
_, col_mid, _ = st.columns([1, 1.2, 1])

with col_mid:
    st.markdown("<h1 style='text-align: center;'>BENVENUTO</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.text_input("Indirizzo Email")
        st.text_input("Password", type="password")
        if st.button("ENTRA NEL CAMPIONATO", use_container_width=True, type="primary"):
            st.info("Verifica credenziali...")
