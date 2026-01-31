import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Palinsesto", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] > div { position: fixed; width: 250px; }
    .stButton > button[kind="primary"] { background-color: #ffc107 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# Recupero della scadenza dall'Admin
deadline = st.session_state.get('deadline_giornata', datetime(2026, 1, 31, 15, 30))
scaduta = datetime.now() > deadline

with st.sidebar:
    st.markdown("### 🏆 FantaSchedina")
    st.divider()
    if st.button("🏠 Home", key="nav_home_gioca", use_container_width=True):
        st.switch_page("app.py")
    st.button("⚽ Gioca", key="nav_gioca_gioca", use_container_width=True, type="primary")
    
    st.divider()
    # Visualizzazione dinamica della scadenza
    scad_str = deadline.strftime("%d/%m/%Y %H:%M")
    if not scaduta:
        st.success(f"🔓 GIOCATE APERTE\nFino al: {scad_str}")
    else:
        st.error(f"🚫 GIOCATE CHIUSE\nTermine: {scad_str}")

st.title("⚽ Palinsesto Professionale")
if scaduta:
    st.warning(f"Attenzione: Termine scaduto il {scad_str}. Non puoi più inviare.")

# Esempio Tabella (11 colonne)
st.write("La tabella delle partite caricata dall'Admin apparirà qui.")
