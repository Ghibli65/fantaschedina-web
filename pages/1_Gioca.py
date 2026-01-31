import streamlit as st
from datetime import datetime

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
