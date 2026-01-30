import streamlit as st
import os
import base64

st.set_page_config(page_title="FantaSchedina Login", layout="wide")

# Funzione per caricare le immagini in modo sicuro
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carichiamo i loghi (Assicurati che i nomi file siano corretti nella cartella)
logo_top_b64 = get_image_base64("ghiandaia imitatrice1.jpg")
logo_bottom_b64 = get_image_base64("WhatsApp Image 2026-01-30 at 12.59.32.jpeg")

# CSS AGGRESSIVO per eliminare i margini di Streamlit e centrare tutto
st.markdown(f"""
    <style>
    /* 1. Sfondo e pulizia margini */
    .stApp {{ background-color: #f1f5f9; }}
    [data-testid="stSidebarNav"] {{ display: none; }}
    
    /* 2. Rimuove lo spazio vuoto in cima alla sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 0rem !important;
    }}

    /* 3. Contenitore Sidebar Personalizzato */
    .sidebar-content {{
        display: flex;
        flex-direction: column;
        height: 95vh;
        justify-content: space-between;
        align-items: center;
        padding: 20px 10px;
    }}

    /* 4. Stile Loghi */
    .img-top {{ width: 180px; transition: 0.3s; }}
    .img-bottom {{ width: 140px; border-radius: 50%; }}

    /* 5. Box Login Centrato e Professionale */
    .login-card {{
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
    }}

    /* 6. Bottoni Gialli Uniformi */
    .stButton > button {{
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-content">
            <div>
                <img src="data:image/jpeg;base64,{logo_top_b64}" class="img-top">
                <h2 style='text-align: center; color: #1e3c72; margin-top: 10px;'>FantaSchedina</h2>
            </div>
            
            <div style="width: 100%;">
                </div>

            <div>
                <img src="data:image/jpeg;base64,{logo_bottom_b64}" class="img-bottom">
                <p style='text-align: center; font-size: 10px; color: #64748b; margin-top: 10px;'>By Acquarossa</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Inseriamo i pulsanti sopra il logo in basso ma fuori dal div HTML per renderli cliccabili
    if st.button("🏠 HOME / LOGIN", use_container_width=True): st.rerun()
    if st.button("⚽ VAI AL GIOCO", use_container_width=True): st.switch_page("pages/1_Gioca.py")

# --- AREA CENTRALE ---
_, col_mid, _ = st.columns([1, 1.2, 1])

with col_mid:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
            <div class="login-card">
                <h1 style='color: #1e3c72;'>BENVENUTO</h1>
                <p style='color: #64748b;'>Inserisci i tuoi dati per accedere</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA NEL CAMPIONATO", use_container_width=True):
                st.info("Connessione a Supabase...")

    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px; margin-top: 20px;'>v2.0 Professional Edition</p>", unsafe_allow_html=True)
