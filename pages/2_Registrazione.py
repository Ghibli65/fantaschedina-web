import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione Nuovo Utente")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome")
    cognome = col2.text_input("Cognome")
    cellulare = st.text_input("Numero di Cellulare (Nome Utente)")
    email = st.text_input("Email")
    pw = st.text_input("Password (min. 6 caratteri)", type="password")
    
    if st.form_submit_button("REGISTRAMI"):
        if nome and cognome and cellulare and email and len(pw) >= 6:
            try:
                # Salvataggio dati nei metadati di autenticazione Supabase
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": pw,
                    "options": {
                        "data": {
                            "nome": nome,
                            "cognome": cognome,
                            "cellulare": cellulare
                        }
                    }
                })
                st.success("✅ Registrazione completata! Torna in Home per il Login.")
            except Exception as e:
                st.error(f"Errore durante la registrazione: {e}")
        else:
            st.warning("Assicurati di aver compilato tutti i campi correttamente.")
