import streamlit as st
import os
import base64

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaSchedina Login", layout="wide")

# Funzione per leggere le immagini e convertirle in formato web (Base64)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo1_b64 = get_base64_image("logo1.png") # Ghiandaia
logo2_b64 = get_base64_image("logo2.png") # Acquarossa

# 2. CSS "HARD" per bloccare la grafica
st.markdown(f"""
    <style>
    /* Sfondo e Pulizia */
    .stApp {{ background-color: #f0f4f8; }}
    [data-testid="stSidebarNav"] {{display: none;}}

    /* POSIZIONAMENTO LOGO 1 (ALTO) */
    .logo-top {{
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
    }}

    /* POSIZIONAMENTO LOGO 2 (BASSO) */
    .logo-bottom {{
        position: fixed;
        bottom: 30px;
        left: 20px;
        width: 120px;
        z-index: 999;
    }}

    /* Centratura Modulo Login */
    .login-container {{
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-top: 50px;
    }}
    
    /* Bottone Giallo Professionale */
    .stButton > button {{
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 45px !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR FISSA ---
with st.sidebar:
    # Logo 1 (Ghiandaia) inserito via HTML per controllo totale
    if logo1_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo1_b64}" class="logo-top">', unsafe_allow_html=True)
    else:
        st.title("🏆 FantaSchedina")
    
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True) # Spazio per il logo in alto
    
    # Menu Navigazione
    st.markdown("### Menu")
    if st.button("🏠 Home / Login", use_container_width=True): st.rerun()
    if st.button("⚽ Vai al Gioco", use_container_width=True): st.switch_page("pages/1_Gioca.py")
    
    # Logo 2 (Acquarossa) bloccato in fondo
    if logo2_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo2_b64}" class="logo-bottom">', unsafe_allow_html=True)

# --- AREA CENTRALE ---
c1, main_col, c3 = st.columns([1, 1.2, 1])

with main_col:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1e3c72;'>Area Accesso</h2>", unsafe_allow_html=True)
    
    email = st.text_input("Indirizzo Email")
    password = st.text_input("Password", type="password")
    
    if st.button("ENTRA NEL CAMPIONATO", use_container_width=True):
        # Collegamento database
        st.info("Accesso in corso...")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 11px; margin-top: 20px;'>FantaSchedina v2.0 - Professional Edition</p>", unsafe_allow_html=True)
