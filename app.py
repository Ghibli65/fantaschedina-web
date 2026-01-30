import streamlit as st
from supabase import create_client, Client

# 1. Configurazione Iniziale
st.set_page_config(page_title="FantaSchedina - Home", layout="wide")

# 2. Inizializzazione Supabase (Assicurati che i segreti siano nel file .streamlit/secrets.toml)
if "supabase" not in st.session_state:
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    st.session_state.supabase = create_client(url, key)

# 3. CSS per Professionalità ed Estetica
st.markdown("""
    <style>
    /* Sfondo pagina grigio chiarissimo professionale */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Pulizia Sidebar */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Box Login Moderno */
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        max-width: 500px;
        margin: auto;
    }
    
    /* Header Benvenuto */
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1e3c72;
        text-align: center;
        font-weight: 700;
    }

    /* Footer Sidebar */
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        right: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR PERSONALIZZATA ---
with st.sidebar:
    # Logo 1: Identità (in alto)
    st.image("logo1.png", width=150) # Assicurati di avere il file o l'URL
    st.markdown("### 🏆 FantaSchedina")
    st.divider()
    
    # Menu di Navigazione pulito
    if st.button("🏠 Home / Login", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    if st.button("⚽ Gioca", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    
    # Logo 2: Brand (in basso, separato)
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    st.image("logo2.png", width=120)
    st.caption("© 2026 FantaSchedina - Pro Version")
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO CENTRALE ---
col_l, col_main, col_r = st.columns([1, 2, 1])

with col_main:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='welcome-text'>Benvenuto su FantaSchedina</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>Inserisci le tue credenziali per accedere al campionato</p>", unsafe_allow_html=True)
    
    # Contenitore Login
    with st.container(border=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        c1, c2 = st.columns(2)
        if c1.button("ACCEDI", type="primary", use_container_width=True):
            try:
                res = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Accesso eseguito!")
                st.rerun()
            except Exception as e:
                st.error("Credenziali non valide")
        
        if c2.button("REGISTRATI", use_container_width=True):
            st.info("Funzione di registrazione in arrivo...")

    # Spazio per comunicazioni o news
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📢 **News:** Il nuovo palinsesto della Serie A è ora disponibile!")
