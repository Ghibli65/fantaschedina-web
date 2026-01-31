import streamlit as st
from supabase import create_client

import streamlit as st

# 1. Questa deve essere la PRIMISSIMA riga di codice dopo gli import
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS Blindato per Sidebar Fissa e Bottoni Gialli
st.markdown("""
    <style>
    /* Rimuove la navigazione standard per evitare doppioni */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* BLOCCA LA SIDEBAR: non deve sparire mai */
    section[data-testid="stSidebar"] {
        min-width: 250px !important;
        max-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        position: fixed !important;
        width: 250px !important;
    }

    /* Stile Bottoni Gialli come da tuoi screenshot */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR FISSA (Identica per tutti i file)
with st.sidebar:
    st.markdown("### 🏆 FantaSchedina")
    st.divider()
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.get('page') == 'home' else 'secondary'):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    if st.button("⚙️ Pannello Admin", use_container_width=True):
        st.switch_page("pages/2_Admin.py")

st.set_page_config(page_title="FantaSchedina", layout="wide")

# --- CONNESSIONE ROBUSTA ---
if "supabase" not in st.session_state:
    try:
        url = st.secrets.get("supabase_url", "").strip()
        key = st.secrets.get("supabase_key", "").strip()
        
        if not url.startswith("https://"):
            st.error("❌ L'URL di Supabase non è valido. Deve iniziare con 'https://'. Controlla i Secrets!")
            st.stop()
            
        st.session_state.supabase = create_client(url, key)
    except Exception as e:
        st.error(f"❌ Errore critico di configurazione: {e}")
        st.stop()

# --- CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")

if "user" in st.session_state:
    st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")
    if st.sidebar.button("🚪 ESCI", use_container_width=True):
        del st.session_state["user"]
        st.rerun()
else:
    st.sidebar.page_link("pages/2_Registrazione.py", label="📝 Registrazione", icon="📩")
    st.sidebar.page_link("pages/3_Admin.py", label="🔐 Accesso Admin", icon="🕵️")

# --- LOGIC LOGIN ---
if "user" in st.session_state:
    st.title("✅ Sei dentro!")
    st.success(f"Utente: {st.session_state.user.email}")
    st.write("Vai su **GIOCA ORA** nel menu a sinistra.")
else:
    st.title("⚽ Accedi a FantaSchedina")
    with st.container():
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("ENTRA", type="primary", use_container_width=True):
            try:
                auth = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = auth.user
                st.rerun()
            except Exception as e:
                st.error(f"Accesso negato: {e}")
