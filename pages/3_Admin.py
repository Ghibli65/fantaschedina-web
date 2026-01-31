import streamlit as st
from datetime import datetime
import pandas as pd

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

with st.sidebar:
    st.title("⚙️ Pannello Admin")
    st.divider()
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto Utenti", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    st.divider()
    st.info("Loggato come: ADMIN")

st.set_page_config(page_title="Admin - Carica & Gestisci", layout="wide")

# CSS consolidato
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Simulazione database giornate chiuse
if "giornate_archiviate" not in st.session_state:
    st.session_state.giornate_archiviate = [
        {"Giornata": 22, "Scadenza": "2026-01-20 15:00", "Stato": "Chiuso"},
        {"Giornata": 23, "Scadenza": "2026-01-27 18:30", "Stato": "Chiuso"}
    ]

tab1, tab2 = st.tabs(["🚀 Carica Nuove Quote", "🔓 Riapri Gioco"])

# --- TAB 1: CARICAMENTO (Il codice di prima) ---
with tab1:
    st.subheader("Caricamento Rapido e Scadenze")
    # ... (qui resta il codice del caricamento in blocco con 2 decimali) ...
    st.info("Usa questa sezione per le nuove partite.")

# --- TAB 2: RIAPRI IL GIOCO (Nuova funzione) ---
with tab2:
    st.subheader("🔄 Gestione Giornate Chiuse")
    st.caption("Elenco delle giornate con termine scaduto. Puoi impostare una nuova data per riaprirle.")

    if st.session_state.giornate_archiviate:
        df_chiuse = pd.DataFrame(st.session_state.giornate_archiviate)
        st.table(df_chiuse)

        with st.container(border=True):
            st.write("**Seleziona giornata da riaprire**")
            c1, c2, c3 = st.columns([1, 1.5, 1.5])
            
            with c1:
                scelta_g = st.selectbox("Giornata", options=[g["Giornata"] for g in st.session_state.giornate_archiviate])
            with c2:
                nuova_data = st.date_input("Nuova Data Chiusura", key="nd")
            with c3:
                nuova_ora = st.time_input("Nuova Ora Chiusura", key="no")
            
            if st.button("CONFERMA RIAPERTURA", type="primary", use_container_width=True):
                nuova_deadline = f"{nuova_data} {nuova_ora}"
                # Logica: Aggiorna il database (qui simulato)
                st.success(f"✅ Giornata {scelta_g} riaperta! Nuova scadenza: {nuova_deadline}")
                st.balloons()
    else:
        st.write("Non ci sono giornate chiuse al momento.")
