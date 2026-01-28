import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione Nuovo Utente")

with st.form("reg_form"):
    new_email = st.text_input("Email")
    new_pw = st.text_input("Password (min. 6 caratteri)", type="password")
    if st.form_submit_button("REGISTRAMI"):
        try:
            res = supabase.auth.sign_up({"email": new_email, "password": new_pw})
            st.success("Registrazione completata! Ora puoi fare il login in Home.")
        except Exception as e:
            st.error(f"Errore: {e}")
