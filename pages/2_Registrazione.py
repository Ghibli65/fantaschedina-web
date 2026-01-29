import streamlit as st

st.set_page_config(page_title="Registrazione Utente", layout="centered")

# --- CSS PER BLOCCO MENU AUTOMATICO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERALE FISSO ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# --- FORM REGISTRAZIONE ---
st.title("📝 Registrazione Nuova Squadra")
st.write("Completa i campi per iscriverti al FantaSchedina.")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome")
    with col2:
        cognome = st.text_input("Cognome")
    
    nome_utente = st.text_input("Nome Utente (Nickname)")
    cellulare = st.text_input("Numero di Cellulare")
    
    st.divider()
    
    email = st.text_input("Email")
    password = st.text_input("Password (min. 6 caratteri)", type="password")
    
    if st.form_submit_button("CREA ACCOUNT", use_container_width=True):
        if nome and nome_utente and cellulare and email and len(password) >= 6:
            try:
                # Registrazione dell'utente con metadati su Supabase [cite: 2026-01-28]
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
                st.success("✅ Registrazione inviata! Controlla l'email o torna in Home per il Login.")
                st.balloons()
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.warning("⚠️ Per favore, compila tutti i campi obbligatori.")
