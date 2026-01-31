import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Admin - Carica Quote", layout="wide")

# CSS Professionale (Bottoni Gialli e tabelle pulite)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    .stNumberInput input { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione database locale temporaneo per vedere l'inserimento in blocco
if "temp_match_list" not in st.session_state:
    st.session_state.temp_match_list = []

with st.sidebar:
    st.title("⚙️ Pannello Admin")
    st.divider()
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

st.title("🛠️ Caricamento Quote e Scadenze")

# --- SEZIONE 1: INFO GIORNATA E TERMINE MASSIMO ---
with st.container(border=True):
    st.subheader("📌 Impostazioni Giornata")
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    with c1:
        giornata = st.number_input("N° Giornata", min_value=1, value=1, step=1)
    with c2:
        data_scadenza = st.date_input("Data Termine Giocate")
    with c3:
        ora_scadenza = st.time_input("Ora Termine Giocate")

st.divider()

# --- SEZIONE 2: INSERIMENTO MATCH ---
st.subheader("📝 Inserimento Match")
with st.form("form_quote", clear_on_submit=True):
    match_name = st.text_input("Partita", placeholder="Squadra Casa - Squadra Trasferta")
    
    st.write("**Quote Esiti Principali**")
    r1 = st.columns(6)
    q1 = r1[0].number_input("1", value=1.0, format="%.2f")
    qX = r1[1].number_input("X", value=1.0, format="%.2f")
    q2 = r1[2].number_input("2", value=1.0, format="%.2f")
    q1X = r1[3].number_input("1X", value=1.0, format="%.2f")
    qX2 = r1[4].number_input("X2", value=1.0, format="%.2f")
    q12 = r1[5].number_input("12", value=1.0, format="%.2f")
    
    st.write("**Quote Speciali**")
    r2 = st.columns(4)
    qU = r2[0].number_input("Under 2.5", value=1.0, format="%.2f")
    qO = r2[1].number_input("Over 2.5", value=1.0, format="%.2f")
    qG = r2[2].number_input("Goal", value=1.0, format="%.2f")
    qNG = r2[3].number_input("No Goal", value=1.0, format="%.2f")
    
    submit = st.form_submit_button("CARICA PARTITA NEL PALINSESTO", type="primary", use_container_width=True)

    if submit and match_name:
        nuovo_match = {
            "Giornata": giornata,
            "Match": match_name,
            "1": q1, "X": qX, "2": q2, "1X": q1X, "X2": qX2, "12": q12,
            "U2.5": qU, "O2.5": qO, "Goal": qG, "NoGoal": qNG
        }
        st.session_state.temp_match_list.append(nuovo_match)
        st.success(f"Aggiunta: {match_name}")

# --- SEZIONE 3: VISUALIZZAZIONE IN BLOCCO (Riepilogo) ---
if st.session_state.temp_match_list:
    st.divider()
    st.subheader(f"📋 Riepilogo Inserimenti - Giornata {giornata}")
    df = pd.DataFrame(st.session_state.temp_match_list)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    c1, c2 = st.columns([1, 5])
    if c1.button("🗑️ Svuota Lista"):
        st.session_state.temp_match_list = []
        st.rerun()
    
    st.info(f"Le giocate per questa giornata scadranno il {data_scadenza} alle {ora_scadenza}")
