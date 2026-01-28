import streamlit as st

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- CSS PER NASCONDERE IL MENU AUTOMATICO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI ACCESSO ---
if "admin_logged_in" not in st.session_state:
    # Sidebar visibile prima del login (solo link pubblici) [cite: 2026-01-28]
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
    st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
    
    st.title("🔐 Accesso Amministratore")
    with st.form("admin_login"):
        u_admin = st.text_input("Utente Admin")
        p_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("SBLOCCA AREA TECNICA"):
            if u_admin == "Admin" and p_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenziali non valide.")
    st.stop()

# --- SIDEBAR ADMIN (Sbloccata dopo il login) ---
st.sidebar.title("⚙️ Pannello Admin")
st.sidebar.page_link("app.py", label="Torna alla Home", icon="🏠")
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica Quote", icon="🚀")

st.sidebar.divider()
if st.sidebar.button("Esci da Admin"):
    del st.session_state.admin_logged_in
    st.rerun()

# --- CONTENUTO DELLA PAGINA ADMIN ---
st.title("⚙️ Gestione Generale")

# Qui puoi inserire i widget per le altre sezioni che avevamo accennato [cite: 2026-01-28]
scelta = st.radio("Cosa vuoi gestire?", ["Riepilogo Giornate", "Risultati Partite", "Gestione Utenti"], horizontal=True)

if scelta == "Riepilogo Giornate":
    st.subheader("Visualizzazione Giornate Caricate")
    # Qui potremmo mettere una tabella che legge da Supabase [cite: 2026-01-28]
    st.info("Usa il tasto 'Carica Quote' nel menu a sinistra per aggiungere nuove partite.")

elif scelta == "Risultati Partite":
    st.subheader("Inserimento Risultati Finali")
    st.write("Questa sezione verrà configurata per aggiornare i punteggi degli utenti.")

elif scelta == "Gestione Utenti":
    st.subheader("Elenco Iscritti")
    st.write("Qui potrai vedere chi si è registrato al tuo FantaSchedina.")
