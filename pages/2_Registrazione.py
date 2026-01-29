import streamlit as st

st.set_page_config(page_title="Registrazione Utente", layout="centered")

# --- CSS PER BLOCCO MENU AUTOMATICO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERALE (Identico alla Home) ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# --- FORM REGISTRAZIONE ---
st.title("📝 Registrazione Utente")
st.write("Inserisci i tuoi dati per creare un nuovo profilo giocatore.")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome")
    with col2:
        cognome = st.text_input("Cognome")
    
    # Nuovi campi aggiunti [cite: 2026-01-28]
    nome_utente = st.text_input("Nome Utente (Nickname)")
    cellulare = st.text_input("Numero di Cellulare")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    st.divider()
    
    if st.form_submit_button("REGISTRATI ORA", use_container_width=True):
        if nome and nome_utente and cellulare and email and len(password) >= 6:
            try:
                # Logica di registrazione su Supabase [cite: 2026-01-28]
                st.session_state.supabase.auth.sign_up({
                    "email": email, 
                    "password": password,
                    "options": {
                        "data": {
                            "nome": nome, 
                            "cognome": cognome,
                            "username": nome_utente,
                            "cellulare": cellulare
                        }
                    }
                })
                st.success("✅ Registrazione completata con successo!")
                st.balloons()
                st.info("Ora puoi tornare nella Home per effettuare il Login.")
            except Exception as e:
                st.error(f"Errore durante la registrazione: {e}")
        else:
            st.warning("⚠️ Compila tutti i campi obbligatori (Password: almeno 6 caratteri).")
