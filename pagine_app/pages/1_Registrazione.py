import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("📝 Registrazione")
with st.form("reg_form"):
    n = st.text_input("Nome")
    c = st.text_input("Cognome")
    cel = st.text_input("Cellulare (User)")
    em = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    
    if st.form_submit_button("REGISTRAMI"):
        if n and c and cel and em and len(pw) >= 6:
            try:
                supabase.auth.sign_up({
                    "email": em, "password": pw,
                    "options": {"data": {"nome": n, "cognome": c, "cellulare": cel}}
                })
                st.success("✅ Registrato! Torna in Home.")
            except Exception as e: st.error(f"Errore: {e}")
