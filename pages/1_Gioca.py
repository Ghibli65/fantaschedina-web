import streamlit as st

st.set_page_config(page_title="Gioca", layout="wide")

# CSS per i bottoni gialli e carrello a sinistra
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# --- SIDEBAR (CARRELLO) ---
with st.sidebar:
    st.header("🛒 Schedina")
    if not st.session_state.carrello:
        st.write("Vuota")
    else:
        totale = 0.0
        for id_p, item in list(st.session_state.carrello.items()):
            c1, c2 = st.columns([4,1])
            c1.write(f"**{item['match']}**\n{item['esito']} @ {item['quota']}")
            if c2.button("❌", key=f"del_{id_p}"):
                del st.session_state.carrello[id_p]
                st.rerun()
            totale += item['quota']
        st.divider()
        st.subheader(f"TOTALE: {totale:.2f}")
        if st.button("🚀 INVIA", type="primary", use_container_width=True):
            st.success("Giocata inviata!")
            st.session_state.carrello = {}
            st.rerun()

# --- MAIN (PALINSESTO) ---
st.title("⚽ Palinsesto")

# Esempio dati (Poi collegati al tuo Supabase)
partite = [
    {"id": 1, "match": "Lazio - Genoa", "1": 2.10, "X": 3.20, "2": 3.50, "1X": 1.30, "X2": 1.70},
    {"id": 2, "match": "Napoli - Fiorentina", "1": 1.80, "X": 3.40, "2": 4.50, "1X": 1.20, "X2": 2.00}
]

cols_size = [3, 1, 1, 1, 1, 1]
h = st.columns(cols_size)
labels = ["MATCH", "1", "X", "2", "1X", "X2"]
for i, l in enumerate(labels): h[i].write(f"**{l}**")

for p in partite:
    r = st.columns(cols_size)
    r[0].write(p['match'])
    
    for i, esito in enumerate(["1", "X", "2", "1X", "X2"]):
        quota = p[esito]
        is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == esito)
        
        if r[i+1].button(str(quota), key=f"btn_{p['id']}_{esito}", type="primary" if is_sel else "secondary"):
            st.session_state.carrello[p['id']] = {"match": p['match'], "esito": esito, "quota": quota}
            st.rerun()
