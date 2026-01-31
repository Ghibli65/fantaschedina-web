import streamlit as st
from datetime import datetime

# Simuliamo il recupero della data (che Admin ha appena cambiato)
if "deadline_giornata" not in st.session_state:
    st.session_state.deadline_giornata = datetime(2026, 1, 31, 15, 30)

ora_attuale = datetime.now()
# Il sistema ora vede la NUOVA data impostata dall'admin
scaduta = ora_attuale > st.session_state.deadline_giornata

with st.sidebar:
    st.markdown("### 🏆 FantaSchedina")
    st.divider()
    # Key univoci per evitare StreamlitDuplicateElementId
    if st.button("🏠 Home", key="btn_home_gioca", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", key="btn_palin_gioca", use_container_width=True, type="primary"):
        st.rerun()
    
    st.divider()
    # Mostra la nuova scadenza aggiornata
    scad_format = st.session_state.deadline_giornata.strftime("%d/%m/%Y alle %H:%M")
    if not scaduta:
        st.success(f"✅ GIOCATE RIAPERTE!\nScadenza: {scad_format}")
    else:
        st.error(f"🚫 Tempo scaduto!\nTermine: {scad_format}")


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

st.markdown("""
    <style>
    /* Rimuove il menu di navigazione standard di Streamlit */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Blocca la sidebar in posizione fissa */
    section[data-testid="stSidebar"] > div {
        position: fixed;
        width: inherit;
    }
    
    /* Stile bottoni gialli (ieri) */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Area Gioco", layout="wide")

# CSS di ieri (Sidebar bloccata e bottoni gialli)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] > div { position: fixed; width: inherit; }
    .stButton > button[kind="primary"] { background-color: #ffc107 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI CONTROLLO SCADENZA ---
# In un sistema reale, questi dati verranno letti da Supabase
if "deadline_giornata" not in st.session_state:
    # Esempio: questa data verrebbe dal tuo Pannello Admin
    st.session_state.deadline_giornata = datetime(2026, 1, 31, 15, 30) 

ora_attuale = datetime.now()
scaduta = ora_attuale > st.session_state.deadline_giornata

# --- SIDEBAR: SCHEDINA E INFO SCADENZA ---
with st.sidebar:
    st.header("📋 La tua Giocata")
    
    # Visualizzazione della scadenza per l'utente
    scadenza_str = st.session_state.deadline_giornata.strftime("%d/%m/%Y alle %H:%M")
    if not scaduta:
        st.info(f"⏳ Termine invio:\n{scadenza_str}")
    else:
        st.error(f"🚫 Tempo scaduto!\nTermine: {scadenza_str}")

    if "carrello" not in st.session_state: st.session_state.carrello = {}
    
    if st.session_state.carrello:
        molt = 1.0
        for p_id, item in list(st.session_state.carrello.items()):
            st.write(f"**{item['match']}**: {item['esito']} @{item['quota']}")
            molt *= item['quota']
        
        st.divider()
        st.subheader(f"TOTALE: {molt:.2f}")
        
        # BLOCCO DEL TASTO INVIO
        if not scaduta:
            if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
                st.success("Giocata Inviata!")
        else:
            st.button("🚀 INVIO DISABILITATO", disabled=True, use_container_width=True)

# --- PALINSESTO ---
st.title("⚽ Palinsesto Professionale")
if scaduta:
    st.warning(f"Attenzione: Le giocate per questa giornata sono chiuse dal {scadenza_str}.")

# Qui segue il codice della tabella a 11 colonne che abbiamo già...
