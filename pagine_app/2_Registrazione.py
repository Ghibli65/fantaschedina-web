import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione")
st.write("Inserisci i tuoi dati per creare un profilo.")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome")
    cognome = col2.text_input("Cognome")
    username_cell = st.text_input("Numero Cellulare (Nome Utente)")
    email = st.text_input("Email")
    pw = st.text_input("Password (min. 6 caratteri)", type="password")
    
    if st.form_submit_button("REGISTRAMI"):
        if nome and cognome and username_cell and email and len(pw) >= 6:
            try:
                # Registrazione con salvataggio dati extra nei metadati
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": pw,
                    "options": {
                        "data": {
                            "nome": nome,
                            "cognome": cognome,
                            "cellulare": username_cell
                        }
                    }
                })
                st.success("✅ Registrazione completata! Ora puoi fare il login in Home.")
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.warning("Completa tutti i campi (la password deve essere di almeno 6 caratteri).")
