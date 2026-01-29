import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

# --- DESIGN ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .main-title {background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px;}
    .status-box {padding: 10px; border-radius: 10px; margin-bottom: 10px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica/Modifica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

st.markdown('<div class="main-title">🚀 GESTIONE & PUBBLICAZIONE</div>', unsafe_allow_html=True)

# --- SEZIONE CARICAMENTO ---
with st.expander("➕ AGGIUNGI NUOVE PARTITE", expanded=False):
    c1, c2 = st.columns([1, 4])
    with c1: g_num = st.number_input("Giorn.", min_value=1, value=1)
    with c2: bulk = st.text_area("Incolla qui i dati...", height=80)
    if st.button("CARICA IN BOZZA", use_container_width=True, type="primary"):
        if bulk:
            try:
                righe = bulk.strip().split('\n')
                for riga in righe:
                    p = riga.split(';')
                    def q(v): return float(str(v).replace(',', '.'))
                    st.session_state.supabase.table("partite").insert({
                        "match": p[0].strip(), "quote_1": q(p[1]), "quote_x": q(p[2]), "quote_2": q(p[3]),
                        "quote_1x": q(p[4]), "quote_x2": q(p[5]), "quote_12": q(p[6]),
                        "quote_u25": q(p[7]), "quote_o25": q(p[8]), "quote_g": q(p[9]),
                        "quote_ng": q(p[10]), "giornata": g_num, "pubblicata": False
                    }).execute()
                st.success("✅ Partite caricate come BOZZA!")
                st.rerun()
            except Exception as e: st.error(f"Errore: {e}")

# --- TABELLA E PUBBLICAZIONE ---
st.subheader("📝 Palinsesto Attuale")

try:
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        # Data Editor per modifiche rapide
        edited_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True, 
            num_rows="dynamic",
            column_order=("pubblicata", "giornata", "match", "quote_1", "quote_x", "quote_2"),
            column_config={"pubblicata": st.column_config.CheckboxColumn("LIVE", width=60)}
        )

        c1, c2 = st.columns(2)
        
        if c1.button("💾 SALVA MODIFICHE TABELLA", use_container_width=True):
            for _, row in edited_df.iterrows():
                st.session_state.supabase.table("partite").update({
                    "pubblicata": row["pubblicata"], 
                    "match": row["match"], 
                    "giornata": row["giornata"]
                }).eq("id", row["id"]).execute()
            st.success("✅ Database aggiornato correttamente!")
            st.rerun()

        # TASTO PUBBLICAZIONE FORZATA (Il più importante)
        if c2.button("📢 PUBBLICA GIORNATA " + str(g_num), type="primary", use_container_width=True):
            st.session_state.supabase.table("partite").update({"pubblicata": True}).eq("giornata", g_num).execute()
            st.balloons()
            st.success(f"🚀 Giornata {g_num} messa in LIVE!")
            st.rerun()
            
    else:
        st.info("Nessuna partita nel database.")
except Exception as e:
    st.error(f"Errore connessione: {e}")
