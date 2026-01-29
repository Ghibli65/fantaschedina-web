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
with st.form("reg_form"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.form_submit_button("REGISTRATI"):
        if nome and email and len(password) >= 6:
            try:
                st.session_state.supabase.auth.sign_up({
                    "email": email, 
                    "password": password,
                    "options": {"data": {"nome": nome, "cognome": cognome}}
                })
                st.success("Registrazione completata! Torna in Home per il Login.")
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.warning("Compila tutti i campi (Password min. 6 caratteri).")
