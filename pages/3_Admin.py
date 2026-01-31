import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Admin - Carica Quote", layout="wide")

# CSS per mantenere lo stile giallo e compatto
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

# --- SEZIONE 2: INSERIMENTO PARTITA (LAYOUT COMPATTO) ---
st.subheader("📝 Inserimento Match")
with st.form("form_quote", clear_on_submit=True):
    match = st.text_input("Partita (es. Lazio - Genoa)", placeholder="Squadra Casa - Squadra Trasferta")
    
    st.write("**Quote Esiti Principali (1X2 e Doppia Chance)**")
    row1 = st.columns(6)
    q1 = row1[0].number_input("1", min_value=1.0, value=1.0, format="%.2f")
    qX = row1[1].number_input("X", min_value=1.0, value=1.0, format="%.2f")
    q2 = row1[2].number_input("2", min_value=1.0, value=1.0, format="%.2f")
    q1X = row1[3].number_input("1X", min_value=1.0, value=1.0, format="%.2f")
    qX2 = row1[4].number_input("X2", min_value=1.0, value=1.0, format="%.2f")
    q12 = row1[5].number_input("12", min_value=1.0, value=1.0, format="%.2f")
    
    st.write("**Quote Speciali (U/O e Goal/NoGoal)**")
    row2 = st.columns(4)
    qU = row2[0].number_input("Under 2.5", min_value=1.0, value=1.0, format="%.2f")
    qO = row2[1].number_input("Over 2.5", min_value=1.0, value=1.0, format="%.2f")
    qG = row2[2].number_input("Goal", min_value=1.0, value=1.0, format="%.2f")
    qNG = row2[3].number_input("No Goal", min_value=1.0, value=1.0, format="%.2f")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("CARICA PARTITA NEL PALINSESTO", type="primary", use_container_width=True)

    if submit:
        # Qui andrà la logica per salvare su Supabase
        # st.session_state.supabase.table("partite").insert({...}).execute()
        st.success(f"✅ {match} caricata correttamente per la Giornata {giornata}!")
        st.info(f"Termine ultimo: {data_scadenza} alle {ora_scadenza}")

# --- LOGICA DI CONTROLLO (Esempio per blocco) ---
deadline = datetime.combine(data_scadenza, ora_scadenza)
if datetime.now() > deadline:
    st.warning("⚠️ ATTENZIONE: Il termine impostato è già passato rispetto all'ora attuale.")
