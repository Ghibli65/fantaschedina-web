import streamlit as st

st.set_page_config(page_title="FantaSchedina - Login", layout="wide", initial_sidebar_state="expanded")

# CSS BLINDATO: Sidebar fissa e bottoni gialli
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] > div { position: fixed; width: 250px; }
    .stButton > button[kind="primary"] { background-color: #ffc107 !important; color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR FISSA
with st.sidebar:
    st.markdown("### 🏆 FantaSchedina")
    st.divider()
    st.button("🏠 Home", key="nav_home_main", use_container_width=True, type="primary")
    if st.button("⚽ Gioca Ora", key="nav_gioca_main", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    if st.button("⚙️ Admin", key="nav_admin_main", use_container_width=True):
        st.switch_page("pages/2_Admin.py")

# LOGIN
st.markdown("<h1 style='text-align: center;'>BENVENUTO</h1>", unsafe_allow_html=True)
_, col_mid, _ = st.columns([1, 1.2, 1])
with col_mid:
    with st.container(border=True):
        st.text_input("Indirizzo Email")
        st.text_input("Password", type="password")
        if st.button("ENTRA NEL CAMPIONATO", key="btn_login", use_container_width=True, type="primary"):
            st.success("Accesso eseguito!")
