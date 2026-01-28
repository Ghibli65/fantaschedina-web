import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome")
    cognome = col2.text_input("Cognome")
    cellulare = st.text_input("Numero di Cellulare (Nome Utente)")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    
    if st.form_submit_button("REGISTRAMI"):
        if nome and cognome and cellulare and email and len(pw) >= 6:
            try:
                # Salviamo i dati extra nei metadati dell'utente
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
                st.success("✅ Registrazione completata! Ora puoi fare il login.")
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.warning("Compila tutti i campi correttamente.")
