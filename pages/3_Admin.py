import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Admin - Carica Quote", layout="wide")

# CSS per bottoni gialli e stile pulito
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

# Inizializzazione della lista partite (persistente nella sessione)
if "lista_partite_admin" not in st.session_state:
    st.session_state.lista_partite_admin = []

with st.sidebar:
    st.title("⚙️ Pannello Admin")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

st.title("🛠️ Caricamento Quote e Scadenze")

# --- SEZIONE 1: GIORNATA E SCADENZA ---
with st.container(border=True):
    st.subheader("📌 Impostazioni Giornata")
    c1, c2, c3 = st.columns(3)
    with c1:
        giornata = st.number_input("N° Giornata", min_value=1, step=1)
    with c2:
        data_scadenza = st.date_input("Data Termine")
    with c3:
        ora_scadenza = st.time_input("Ora Termine")

st.divider()

# --- SEZIONE 2: INSERIMENTO SINGOLO MATCH ---
st.subheader("📝 Inserimento Match")
match_nome = st.text_input("Nome Partita (es. Lazio - Genoa)")

# Griglia compatta per le quote
r1 = st.columns(6)
q1 = r1[0].number_input("1", value=1.0, step=0.01)
qx = r1[1].number_input("X", value=1.0, step=0.01)
q2 = r1[2].number_input("2", value=1.0, step=0.01)
q1x = r1[3].number_input("1X", value=1.0, step=0.01)
qx2 = r1[4].number_input("X2", value=1.0, step=0.01)
q12 = r1[5].number_input("12", value=1.0, step=0.01)

r2 = st.columns(4)
qu = r2[0].number_input("U2.5", value=1.0, step=0.01)
qo = r2[1].number_input("O2.5", value=1.0, step=0.01)
qg = r2[2].number_input("G", value=1.0, step=0.01)
qng = r2[3].number_input("NG", value=1.0, step=0.01)

if st.button("AGGIUNGI ALLA LISTA IN BLOCCO", type="primary", use_container_width=True):
    if match_nome:
        nuovo = {
            "Giorno/Ora Termine": f"{data_scadenza} {ora_scadenza}",
            "Match": match_nome,
            "1": q1, "X": qx, "2": q2, "1X": q1x, "X2": qx2, "12": q12,
            "U2.5": qu, "O2.5": qo, "G": qg, "NG": qng
        }
        st.session_state.lista_partite_admin.append(nuovo)
        st.success(f"Partita {match_nome} aggiunta!")
    else:
        st.error("Inserisci il nome della partita!")

# --- SEZIONE 3: VISUALIZZAZIONE IN BLOCCO (Tabella di riepilogo) ---
if st.session_state.lista_partite_admin:
    st.divider()
    st.subheader(f"📋 Riepilogo Giornata {giornata}")
    
    # Trasforma la lista in una tabella visibile
    df = pd.DataFrame(st.session_state.lista_partite_admin)
    st.table(df) # st.table è migliore di dataframe per vedere tutto subito senza scroll
    
    col_a, col_b = st.columns([1, 4])
    if col_a.button("🗑️ Svuota Tutto"):
        st.session_state.lista_partite_admin = []
        st.rerun()
    
    if st.button("🚀 SALVA DEFINITIVAMENTE TUTTA LA GIORNATA", type="primary", use_container_width=True):
        st.balloons()
        st.success("Tutte le partite sono state salvate nel database!")
        # Qui inseriremo il codice Supabase finale
