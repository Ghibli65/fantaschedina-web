import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Admin", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] > div { position: fixed; width: 250px; }
    .stButton > button[kind="primary"] { background-color: #ffc107 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

if "lista_partite_admin" not in st.session_state:
    st.session_state.lista_partite_admin = []

with st.sidebar:
    st.markdown("### ⚙️ Admin")
    st.divider()
    if st.button("🏠 Home", key="nav_home_adm", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", key="nav_gioca_adm", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

st.title("🛠️ Gestione Schedina")

tab1, tab2 = st.tabs(["🚀 Carica in Blocco", "🔓 Riapri Gioco"])

with tab1:
    c1, c2, c3 = st.columns(3)
    giornata = c1.number_input("N° Giornata", min_value=1, step=1, key="g_admin")
    d_scad = c2.date_input("Data Termine", key="d_admin")
    o_scad = c3.time_input("Ora Termine", key="o_admin")
    
    input_testo = st.text_area("Incolla partite (Match;1;X;2;1X;X2;12;U;O;G;NG)", height=150)
    if st.button("ELABORA E CARICA", key="btn_elabora", type="primary", use_container_width=True):
        if input_testo:
            righe = input_testo.strip().split('\n')
            for r in righe:
                d = r.split(';')
                if len(d) >= 11:
                    st.session_state.lista_partite_admin.append({
                        "Match": d[0], "1": d[1].replace(',','.'), "X": d[2].replace(',','.') # ecc...
                    })
            st.session_state.deadline_giornata = datetime.combine(d_scad, o_scad)
            st.success("Partite caricate e scadenza impostata!")

with tab2:
    st.subheader("🔄 Riapri una sessione chiusa")
    # Elenco fittizio per l'esempio
    g_chiuse = [22, 23, 24]
    scelta = st.selectbox("Seleziona Giornata da riaprire", g_chiuse, key="sel_riapri")
    nuova_d = st.date_input("Nuova Data", key="nd_riapri")
    nuova_o = st.time_input("Nuova Ora", key="no_riapri")
    
    if st.button("CONFERMA RIAPERTURA", key="btn_riapri_conf", type="primary", use_container_width=True):
        st.session_state.deadline_giornata = datetime.combine(nuova_d, nuova_o)
        st.success(f"✅ Giornata {scelta} riaperta correttamente!")
