import streamlit as st
import pandas as pd

# 1. Configurazione Pagina (Wide è fondamentale)
st.set_page_config(page_title="Palinsesto", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Professionale: Compattazione estrema e Sidebar Fissa
st.markdown("""
    <style>
    /* Nasconde menu standard */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Rimpicciolisce i font di tutta la pagina */
    html, body, [class*="css"] { font-size: 13px !important; }

    /* SIDEBAR FISSA E STRETTA */
    section[data-testid="stSidebar"] {
        width: 240px !important;
        background-color: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] > div {
        position: fixed;
        width: 240px;
    }

    /* TABELLA QUOTE COMPATTA */
    .stButton > button {
        width: 100% !important;
        padding: 2px !important;
        height: 26px !important;
        font-size: 11px !important;
        border-radius: 4px !important;
        border: 1px solid #e2e8f0 !important;
    }
    /* Colore Giallo Selezione */
    .stButton > button[kind="primary"] {
        background-color: #fbbf24 !important;
        color: #000 !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Schedina Sidebar */
    .bet-row {
        background: white;
        padding: 6px;
        border-radius: 4px;
        margin-bottom: 4px;
        border-left: 3px solid #1e3c72;
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# --- SIDEBAR: NAVIGAZIONE E SCHEDINA ---
with st.sidebar:
    st.subheader("🏆 BetApp")
    c_nav1, c_nav2 = st.columns(2)
    if c_nav1.button("🏠 Home", use_container_width=True): st.switch_page("app.py")
    if c_nav2.button("⚽ Gioca", type="primary", use_container_width=True): st.rerun()
    
    st.markdown("---")
    st.write("📋 **LA TUA GIOCATA**")
    
    # Box schedina con scroll interno bloccato
    with st.container(height=400, border=False):
        if not st.session_state.carrello:
            st.caption("Seleziona quote dal palinsesto")
        else:
            somma = 0.0
            for p_id in sorted(st.session_state.carrello.keys()):
                item = st.session_state.carrello[p_id]
                with st.container():
                    col_t, col_x = st.columns([4, 1])
                    col_t.markdown(f"<div class='bet-row'><b>{item['match'][:18]}</b><br>{item['esito']} @ {item['quota']}</div>", unsafe_allow_html=True)
                    if col_x.button("✕", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    somma += item['quota']
    
    if st.session_state.carrello:
        st.markdown(f"### TOT: {somma:.2f}")
        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            st.success("Registrata!")
            st.session_state.carrello = {}
            st.rerun()

# --- MAIN: PALINSESTO COMPLETO ---
st.title("⚽ Palinsesto Professionale")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        # Header con DOPPIA CHANCE incluse [cite: 2026-01-29]
        cols_size = [2.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        h = st.columns(cols_size)
        headers = ["PARTITA", "1", "X", "2", "1X", "X2", "12", "U2.5", "O2.5", "G", "NG"]
        for i, text in enumerate(headers):
            h[i].caption(f"**{text}**")
        st.divider()

        for p in partite:
            r = st.columns(cols_size)
            r[0].write(f"**{p['match']}**")
            
            # Mappatura chiavi database -> Etichette interfaccia [cite: 2026-01-29]
            quote_map = [
                ('quote_1', '1'), ('quote_x', 'X'), ('quote_2', '2'),
                ('quote_1x', '1X'), ('quote_x2', 'X2'), ('quote_12', '12'),
                ('quote_u25', 'U'), ('quote_o25', 'O'), ('quote_g', 'G'), ('quote_ng', 'NG')
            ]
            
            for i, (q_key, label) in enumerate(quote_map):
                val = p[q_key]
                is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == label)
                
                if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type="primary" if is_sel else "secondary"):
                    st.session_state.carrello[p['id']] = {"match": p['match'], "esito": label, "quota": float(val)}
                    st.rerun()
except Exception as e:
    st.error(f"Errore: {e}")
