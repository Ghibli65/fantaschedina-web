import streamlit as st

st.set_page_config(page_title="Registrazione")
supabase = st.session_state.supabase

st.title("📝 Registrazione")

with st.form("reg"):
    n = st.text_input("Nome")
    c = st.text_input("Cognome")
    cel = st.text_input("Cellulare")
    em = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    
    if st.form_submit_button("REGISTRATI"):
        if n and c and em and len(pw) >= 6:
            try:
                supabase.auth.sign_up({
                    "email": em, "password": pw,
                    "options": {"data": {"nome": n, "cognome": c, "cellulare": cel}}
                })
                st.success("Registrazione completata! Vai in Home per il login.")
            except Exception as e: st.error(f"Errore: {e}")
        else: st.error("Compila tutti i campi correttamente.")
