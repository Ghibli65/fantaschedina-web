import streamlit as st

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- LOGIN ADMIN INDIPENDENTE ---
if "admin_logged_in" not in st.session_state:
    # Mostriamo il menu normale dell'app finché non si è loggati come admin
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
    
    st.title("🔐 Accesso Amministratore")
    with st.form("admin_login"):
        user_admin = st.text_input("Utente Admin")
        pass_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("ENTRA NEL PANNELLO"):
            if user_admin == "Admin" and pass_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenziali Amministratore errate!")
    st.stop()

# --- SE LOGGATO: NUOVA BARRA LATERALE ADMIN ---
# Nascondiamo i link della navigazione standard e personalizziamo la sidebar admin
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    .stPageLink { background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("⚙️ Pannello Admin")
scelta = st.sidebar.radio(
    "Seleziona Operazione:",
    ["Inserisci Giornata", "Inserisci Risultati", "Gestione Utenti"]
)

st.sidebar.divider()
if st.sidebar.button("🚪 Esci e torna al Menu"):
    del st.session_state.admin_logged_in
    st.rerun()

# --- LOGICA DELLE SEZIONI ---

if scelta == "Inserisci Giornata":
    st.title("📅 Inserisci Giornata")
    st.write("Qui caricheremo le nuove partite per la prossima giornata.")
    # Esempio di segnaposto
    with st.expander("Istruzioni"):
        st.info("Incolla le partite nel formato: SquadraA-SquadraB;1.80;3.40;4.00...")

elif scelta == "Inserisci Risultati":
    st.title("🏁 Inserisci Risultati")
    st.write("Qui inseriremo i risultati finali delle partite giocate per calcolare i punti.")

elif scelta == "Gestione Utenti":
    st.title("👥 Gestione Utenti")
    st.write("Qui potrai visualizzare gli iscritti e gestire i loro profili.")
