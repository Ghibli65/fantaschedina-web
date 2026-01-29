import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gioca Schedina", layout="wide")

# CSS per rendere tutto microscopico e ordinato nella sidebar
st.markdown("""
    <style>
    /* Colore Giallo per i tasti selezionati nel palinsesto */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    /* Stile per la riga della schedina nella sidebar */
    .sidebar-item {
        font-size: 11px;
        line-height: 1.2;
        padding: 5px;
        background: #ffffff10;
        border-radius: 5px;
        margin-bottom: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# --- SIDEBAR: CARRELLO COMPATTO ---
with st.sidebar:
    st.markdown("### 📋 La tua Giocata")
    
    # Sezione a scorrimento limitato per non coprire il menu [cite: 2026-01-29]
    with st.container():
        if not st.session_state.carrello:
            st.caption("Vuota")
        else:
            somma_quote = 0.0
            for p_id in sorted(st.session_state.carrello.keys()):
                item = st.session_state.carrello[p_id]
                # Visualizzazione su una sola riga per risparmiare spazio [cite: 2026-01-29]
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"<div class='sidebar-item'>{item['match'][:15]}.. <b>{item['esito']}</b> @{item['quota']}</div>", unsafe_allow_html=True)
                if col2.button("❌", key=f"side_del_{p_id}"):
                    del st.session_state.carrello[p_id]
                    st.rerun()
                somma_quote += item['quota']
            
            st.markdown(f"**TOTALE: {somma_quote:.2f}**")
            if st.button("🚀 INVIA", type="primary", use_container_width=True):
                st.success("Inviata!")
                st.session_state.carrello = {}
                st.rerun()
    
    st.divider() # Qui sotto Streamlit mostrerà automaticamente i pulsanti delle pagine

# --- MAIN: PALINSESTO ---
st.title("⚽ Palinsesto Giornata")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        # Header ultra-sottile
        h = st.columns([2, 1, 1, 1, 1, 1, 1])
        for i, l in enumerate(["MATCH", "1", "X", "2", "U", "O", "G"]): h[i].caption(f"**{l}**")
        
        for p in partite:
            r = st.columns([2, 1, 1, 1, 1, 1, 1])
            r[0].write(f"**{p['match']}**")
            
            for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                val = p[q_key]
                tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                
                # Feedback visivo: GIALLO se cliccato [cite: 2026-01-29]
                is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == tipo)
                
                if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type="primary" if is_sel else "secondary"):
                    st.session_state.carrello[p['id']] = {"match": p['match'], "esito": tipo, "quota": float(val)}
                    st.rerun()
except Exception as e:
    st.error(f"Errore: {e}")
