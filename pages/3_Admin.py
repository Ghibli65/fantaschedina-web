import streamlit as st

st.set_page_config(page_title="Accesso Admin", layout="centered")

# --- CSS PER BLOCCO MENU AUTOMATICO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERALE ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# --- LOGIN ADMIN ---
st.title("🔐 Accesso Amministratore")

if "admin_logged_in" not in st.session_state:
    with st.form("admin_login"):
        user_admin = st.text_input("Utente Admin")
        pass_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("ENTRA"):
            if user_admin == "Admin" and pass_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.success("Accesso Admin riuscito!")
                st.rerun()
            else:
                st.error("Credenziali Admin errate.")
else:
    st.success("Sei loggato come Amministratore.")
    if st.button("Vai al Caricamento Dati"):
        st.switch_page("pages/4_Caricamento_Dati.py")
    if st.button("Logout Admin"):
        del st.session_state.admin_logged_in
        st.rerun()
