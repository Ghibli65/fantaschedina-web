import streamlit as st

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- LOGIN ADMIN INDIPENDENTE ---
if "admin_logged_in" not in st.session_state:
    # Mostriamo il menu normale finché non si è loggati come admin
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
    
    st.title("🔐 Accesso Amministratore")
    with st.form("admin_login"):
        user_admin = st.text_input("Utente Admin")
        pass_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("ENTRA NEL PANNELLO"):
            if user_admin == "Admin" and pass_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenziali Amministratore errate!")
    st.stop()

# --- SE SEI LOGGATO COME ADMIN: FAI SCOMPARIRE LA BARRA A SINISTRA ---
st.markdown("""
    <style>
    /* Nasconde completamente la barra laterale */
    [data-testid="stSidebar"] {
        display: none;
    }
    /* Allarga il contenuto per occupare lo spazio rimasto vuoto */
    .main .block-container {
        max-width: 95%;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENUTO PANNELLO ADMIN (Senza barra laterale) ---
st.title("⚙️ Pannello di Controllo Admin")
st.write(f"Benvenuto, **Amministratore**. La barra laterale è stata nascosta.")

if st.button("🚪 Esci e torna al Menu"):
    del st.session_state.admin_logged_in
    st.rerun()

st.divider()

# Spazio pronto per quello che vorrai inserire
st.info("Sono pronto! Dimmi cosa dobbiamo inserire qui (tabelle, gestione partite, risultati...).")
