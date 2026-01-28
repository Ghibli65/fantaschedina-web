import streamlit as st

st.set_page_config(page_title="Caricamento Dati", layout="wide")

# --- CSS PER IL MENU ---
st.markdown("""<style>[data-testid="stSidebarNav"] { display: none; } .stPageLink { background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px; }</style>""", unsafe_allow_html=True)

# --- CONTROLLO ACCESSO (Sola Admin) ---
if "admin_logged_in" not in st.session_state:
    st.error("⛔ Accesso riservato agli amministratori. Effettua il login nella pagina Admin.")
    if st.button("Vai alla pagina Admin"):
        st.switch_page("pages/3_Admin.py")
    st.stop()

# --- SIDEBAR COORDINATA ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Torna alla Home", icon="🏠")
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Caricamento Quote", icon="🚀")

# --- INTERFACCIA DI CARICAMENTO ---
st.title("🚀 Caricamento Massivo Quote")
st.info("Questa pagina serve esclusivamente per iniettare i dati nel Database.")

giornata_num = st.number_input("Imposta Numero Giornata", min_value=1, step=1)

bulk_data = st.text_area("Incolla qui il blocco partite (Separatore ';')", height=400, 
                         placeholder="SquadraA-SquadraB;1.85;3.40;4.10;1.20;1.90;1.30;1.80;2.00;1.70;2.05")

if st.button("ESEGUI CARICAMENTO", type="primary"):
    if bulk_data:
        try:
            supabase = st.session_state.supabase
            righe = bulk_data.strip().split('\n')
            for riga in righe:
                p = riga.split(';')
                def q(v): return float(v.replace(',', '.'))
                
                supabase.table("partite").insert({
                    "match": p[0].strip(),
                    "quote_1": q(p[1]), "quote_x": q(p[2]), "quote_2": q(p[3]),
                    "quote_1x": q(p[4]), "quote_x2": q(p[5]), "quote_12": q(p[6]),
                    "quote_u25": q(p[7]), "quote_o25": q(p[8]), "quote_g": q(p[9]),
                    "quote_ng": q(p[10]),
                    "giornata": giornata_num
                }).execute()
            st.success(f"✅ Ottimo! Inserite {len(righe)} partite per la giornata {giornata_num}.")
        except Exception as e:
            st.error(f"Errore nel formato dati: {e}")
    else:
        st.warning("Incolla i dati prima di premere il tasto.")
