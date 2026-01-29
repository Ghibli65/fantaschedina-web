import streamlit as st

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- CSS PER NASCONDERE IL MENU AUTOMATICO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- PROTEZIONE ACCESSO ADMIN ---
if "admin_logged_in" not in st.session_state:
    # Sidebar base visibile prima del login
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")
    
    st.title("🔐 Accesso Amministratore")
    with st.form("admin_login"):
        u_admin = st.text_input("Utente Admin")
        p_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("SBLOCCA PANNELLO"):
            if u_admin == "Admin" and p_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenziali non valide.")
    st.stop()

# --- SIDEBAR ADMIN (Sbloccata dopo il login) ---
st.sidebar.title("⚙️ Pannello Admin")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

st.sidebar.divider()
if st.sidebar.button("Chiudi Sessione Admin"):
    del st.session_state.admin_logged_in
    st.rerun()

# --- CONTENUTO DELLA PAGINA ADMIN ---
st.title("⚙️ Pannello di Controllo")
st.write(f"Benvenuto, **Amministratore**. Da qui puoi monitorare lo stato del FantaSchedina.")

# Piccola Dashboard riassuntiva
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pagine Gestione", "3")
with col2:
    st.metric("Stato Database", "Connesso")
with col3:
    st.metric("Sessione", "Attiva")

st.divider()
st.info("Scegli un'operazione dal menu a sinistra per iniziare a lavorare sui dati.")
