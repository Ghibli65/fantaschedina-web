import streamlit as st

st.set_page_config(page_title="Admin")

# --- STESSO CSS DI APP.PY ---
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# --- LOGIN ADMIN CON USER: Admin E PASS: fanta ---
if "admin_ok" not in st.session_state:
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
    
    st.title("🔐 Accesso Admin")
    u = st.text_input("Utente Admin")
    p = st.text_input("Password Admin", type="password")
    if st.button("Entra"):
        if u == "Admin" and p == "fanta":
            st.session_state.admin_ok = True
            st.rerun()
        else: st.error("Negato")
    st.stop()

# --- SIDEBAR COMPLETA SE LOGGATO ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

st.title("⚙️ Pannello Admin")
# ... (tuo codice per caricare partite qui) ...
