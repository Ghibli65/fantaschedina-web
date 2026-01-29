import streamlit as st
import pandas as pd

st.set_page_config(page_title="Area Gioco", layout="wide")

# CSS per Sidebar Microscopica e Selezione Gialla
st.markdown("""
    <style>
    /* Nasconde il menu pagine standard per pulizia */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Sidebar: font ridotto e margini minimi */
    .sb-item {
        font-size: 10px !important;
        line-height: 1.1;
        margin-bottom: 2px;
        color: #333;
    }
    
    /* Bottoni selezione (GIALLO) */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Riduce lo spazio tra le righe del palinsesto */
    .stVerticalBlock { gap: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SICUREZZA E SESSIONE ---
if "user" not in st.session_state:
    st.warning("Effettua il login.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# --- SIDEBAR PERSONALIZZATA (Solo pulsanti utili) ---
with st.sidebar:
    st.title("🏆 BetApp")
    
    # Navigazione pulita per l'utente [cite: 2026-01-29]
    if st.button("🏠 Home", use_container_width=True): st.switch_page("app.py")
    if st.button("⚽ Gioca Ora", type="primary", use_container_width=True): st.rerun()
    
    # Sezione Schedina compatta
    st.markdown("---")
    st.markdown("📋 **LA TUA GIOCATA**")
    
    # Contenitore con altezza fissa per non allungare la sidebar [cite: 2026-01-29]
    with st.container(height=300, border=False):
        if not st.session_state.carrello:
            st.caption("Seleziona quote...")
        else:
            somma_quote = 0.0
            for p_id in sorted(st.session_state.carrello.keys()):
                item = st.session_state.carrello[p_id]
                c1, c2 = st.columns([5, 1])
                # Testo ultra-compresso
                c1.markdown(f"<div class='sb-item'>{item['match'][:12]}. <b>{item['esito']}</b> @{item['quota']}</div>", unsafe_allow_html=True)
                if c2.button("❌", key=f"del_{p_id}"):
                    del st.session_state.carrello[p_id]
                    st.rerun()
                somma_quote += item['quota']
    
    if st.session_state.carrello:
        st.markdown(f"**TOTALE: {somma_quote:.2f}**")
        if st.button("🚀 INVIA SCHEDINA", use_container_width=True, type="primary"):
            st.success("Schedina Inviata!")
            st.session_state.carrello = {}
            st.rerun()

# --- MAIN: PALINSESTO ---
st.title("⚽ Compila la tua Schedina")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        # Header leggero
        h = st.columns([2.2, 1, 1, 1, 1, 1, 1])
        for i, l in enumerate(["MATCH", "1", "X", "2", "U", "O", "G"]): h[i].caption(l)
        
        for p in partite:
            r = st.columns([2.2, 1, 1, 1, 1, 1, 1])
            r[0].write(f"**{p['match']}**")
            
            for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                val = p[q_key]
                tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                
                # Feedback GIALLO [cite: 2026-01-29]
                is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == tipo)
                
                if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type="primary" if is_sel else "secondary"):
                    st.session_state.carrello[p['id']] = {"match": p['match'], "esito": tipo, "quota": float(val)}
                    st.rerun()
except Exception as e:
    st.error(f"Errore: {e}")
