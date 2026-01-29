import streamlit as st

st.set_page_config(page_title="Registrazione Utente", layout="centered")

# CSS: Fondamentale per non far apparire il menu "grigio" automatico
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

# --- CONTENUTO REGISTRAZIONE ---
st.title("📝 Registrazione Utente")
with st.form("reg_form"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    email = st.text_input("Email")
    st.form_submit_button("REGISTRATI")
