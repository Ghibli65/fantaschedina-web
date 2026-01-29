import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .main-title {background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px;}
    .section-card {background-color: #ffffff; border: 1px solid #e0e0e0; padding: 10px; border-radius: 10px; border-top: 5px solid #4CAF50; margin-bottom: 15px;}
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

# --- CARICAMENTO ---
with st.expander("➕ AGGIUNGI NUOVE PARTITE", expanded=False):
    c1, c2 = st.columns([1, 4])
    with c1: g_num = st.number_input("Giorn.", min_value=1, value=1, key="g_input")
    with c2: bulk = st.text_area("Incolla: Squadre;1;X;2;1X;X2;12;U;O;G;NG", height=80)
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
                st.success("✅ Salvate in bozza!")
                st.rerun()
            except Exception as e: st.error(f"Errore: {e}")

# --- TABELLA E PUBBLICAZIONE ---
st.markdown('<div class="section-card">📝 <b>CONTROLLA E ATTIVA LIVE</b></div>', unsafe_allow_html=True)
try:
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        edited_df = st.data_editor(df, use_container_width=True, hide_index=True, num_rows="dynamic",
                                   column_order=("pubblicata", "giornata", "match", "quote_1", "quote_x", "quote_2"),
                                   column_config={"pubblicata": st.column_config.CheckboxColumn("LIVE", width=60)})

        c_s, c_p = st.columns(2)
        if c_s.button("💾 SALVA MODIFICHE TABELLA", use_container_width=True):
            for _, row in edited_df.iterrows():
                st.session_state.supabase.table("partite").update({"pubblicata": row["pubblicata"], "match": row["match"], "giornata": row["giornata"]}).eq("id", row["id"]).execute()
            st.success("✨ Modifiche salvate!")
            st.rerun()

        if c_p.button("📢 PUBBLICA TUTTA LA GIORNATA", type="primary", use_container_width=True):
            # Forza TUTTE le partite di quella giornata a pubblicata = True
            st.session_state.supabase.table("partite").update({"pubblicata": True}).eq("giornata", g_num).execute()
            st.balloons()
            st.success(f"🚀 Giornata {g_num} ora visibile!")
            st.rerun()
    else:
        st.info("Nessuna partita trovata.")
except Exception as e: st.error(f"Errore: {e}")
