import streamlit as st

st.set_page_config(page_title="FantaSchedina", layout="wide")

# CSS Minimo: Solo per il colore giallo e pulizia sidebar
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🏆 FantaSchedina")
    if st.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    if st.button("⚽ Gioca", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    st.divider()
    st.info("Effettua il login per continuare")

st.title("Benvenuto su FantaSchedina")
with st.container(border=True):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("ACCEDI"):
        st.success("Accesso in corso...")
