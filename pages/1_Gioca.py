import streamlit as st

st.set_page_config(page_title="Area Gioco", layout="wide")

# CSS per Sidebar Fissa e Tabella Compatta [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] > div { position: fixed; width: inherit; }
    .stButton > button { height: 30px !important; font-size: 11px !important; }
    .stButton > button[kind="primary"] { background-color: #ffc107 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# SIDEBAR: SCHEDINA [cite: 2026-01-29]
with st.sidebar:
    st.header("🛒 La tua Giocata")
    if not st.session_state.carrello:
        st.caption("Seleziona le quote dal palinsesto")
    else:
        somma_quote = 0.0
        for p_id, item in list(st.session_state.carrello.items()):
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{item['match'][:15]}**\n{item['esito']} @{item['quota']}")
            if c2.button("❌", key=f"del_{p_id}"):
                del st.session_state.carrello[p_id]
                st.rerun()
            somma_quote += item['quota']
        st.divider()
        st.subheader(f"TOTALE: {somma_quote:.2f}")
        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            st.success("Schedina Inviata con successo!")

# MAIN: PALINSESTO A 11 COLONNE [cite: 2026-01-29]
st.title("⚽ Palinsesto Professionale")

# Recupero dati (Sostituire con chiamata Supabase)
try:
    # Qui inseriremo la logica per leggere dal DB stasera
    partite = [
        {"id": 1, "match": "Lazio - Genoa", "1": 2.10, "X": 3.20, "2": 3.80, "1X": 1.25, "X2": 1.70, "12": 1.30, "U": 1.85, "O": 1.95, "G": 1.75, "NG": 2.10}
    ]

    # Header Tabella
    cols_size = [2.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    h = st.columns(cols_size)
    headers = ["MATCH", "1", "X", "2", "1X", "X2", "12", "U2.5", "O2.5", "G", "NG"]
    for i, txt in enumerate(headers): h[i].caption(f"**{txt}**")

    for p in partite:
        r = st.columns(cols_size)
        r[0].write(f"**{p['match']}**")
        
        # Elenco esiti per i bottoni
        esiti = [("1","1"), ("X","X"), ("2","2"), ("1X","1X"), ("X2","X2"), ("12","12"), ("U","U"), ("O","O"), ("G","G"), ("NG","NG")]
        
        for i, (chiave, etichetta) in enumerate(esiti):
            valore = p[chiave]
            # Controllo se è selezionato per il colore giallo [cite: 2026-01-29]
            is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == etichetta)
            
            if r[i+1].button(str(valore), key=f"q_{p['id']}_{chiave}", type="primary" if is_sel else "secondary"):
                st.session_state.carrello[p['id']] = {"match": p['match'], "esito": etichetta, "quota": valore}
                st.rerun()
except Exception as e:
    st.error(f"Errore caricamento dati: {e}")
