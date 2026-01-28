import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione Utente")

with st.form("reg_form"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    cellulare = st.text_input("Numero Cellulare")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    
    if st.form_submit_button("REGISTRAMI"):
        if email and pw and cellulare:
            try:
                # Registrazione con salvataggio dati extra nei metadati
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
                st.success("✅ Registrazione effettuata! Vai in Home per il login.")
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.error("Email, Password e Cellulare sono obbligatori.")
