import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

# --- CSS DESIGN MAESTRO: COMPATTO E VIVACE ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .main-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 15px; border-radius: 12px;
        text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px;
    }
    .section-card {
        background-color: #ffffff; border: 1px solid #e0e0e0;
        padding: 10px; border-radius: 10px; border-top: 5px solid #4CAF50;
        margin-bottom: 15px; font-weight: bold;
    }
    /* Font compatto per la tabella */
    .stDataEditor div { font-size: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica/Modifica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

st.markdown('<div class="main-title">🚀 GESTIONE & PUBBLICAZIONE PALINSESTO</div>', unsafe_allow_html=True)

# --- CARICAMENTO ---
with st.expander("➕ AGGIUNGI NUOVE PARTITE (BOZZA)", expanded=False):
    c1, c2 = st.columns([1, 4])
    with c1: g_num = st.number_input("Giorn.", min_value=1, value=1)
    with c2: bulk = st.text_area("Incolla: Squadre;1;X;2;1X;X2;12;U;O;G;NG", height=80)
    if st.button("CARICA COME BOZZA", use_container_width=True, type="primary"):
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
                st.success("✅ Salvate in bozza! Ora controllale sotto e attiva 'LIVE'.")
                st.rerun()
            except Exception as e: st.error(f"Errore: {e}")

# --- MODIFICA E PUBBLICAZIONE ---
st.markdown('<div class="section-card">📝 MODIFICA E ATTIVAZIONE "LIVE"</div>', unsafe_allow_html=True)

try:
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        # Tabella ultra-compatta per evitare lo scroll [cite: 2026-01-28]
        edited_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True, 
            num_rows="dynamic",
            column_order=("pubblicata", "giornata", "match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "pubblicata": st.column_config.CheckboxColumn("LIVE", width=45),
                "giornata": st.column_config.NumberColumn("G.", width=35),
                "match": st.column_config.TextColumn("PARTITA", width=150),
                "quote_1": st.column_config.NumberColumn("1", width=38, format="%.2f"),
                "quote_x": st.column_config.NumberColumn("X", width=38, format="%.2f"),
                "quote_2": st.column_config.NumberColumn("2", width=38, format="%.2f"),
                "quote_1x": st.column_config.NumberColumn("1X", width=38, format="%.2f"),
                "quote_x2": st.column_config.NumberColumn("X2", width=38, format="%.2f"),
                "quote_12": st.column_config.NumberColumn("12", width=38, format="%.2f"),
                "quote_u25": st.column_config.NumberColumn("U", width=35, format="%.2f"),
                "quote_o25": st.column_config.NumberColumn("O", width=35, format="%.2f"),
                "quote_g": st.column_config.NumberColumn("G", width=35, format="%.2f"),
                "quote_ng": st.column_config.NumberColumn("NG", width=35, format="%.2f"),
            }
        )

        c_save, c_pub = st.columns(2)
        if c_save.button("💾 SALVA TUTTO", use_container_width=True):
            for _, row in edited_df.iterrows():
                st.session_state.supabase.table("partite").update({
                    "match": row["match"], "giornata": row["giornata"], "pubblicata": row["pubblicata"],
                    "quote_1": row["quote_1"], "quote_x": row["quote_x"], "quote_2": row["quote_2"],
                    "quote_1x": row["quote_1x"], "quote_x2": row["quote_x2"], "quote_12": row["quote_12"],
                    "quote_u25": row["quote_u25"], "quote_o25": row["quote_o25"], 
                    "quote_g": row["quote_g"], "quote_ng": row["quote_ng"]
                }).eq("id", row["id"]).execute()
            st.success("✨ Modifiche salvate!")
            st.rerun()

        if c_pub.button("📢 PUBBLICA GIORNATA INTERA", type="primary", use_container_width=True):
            st.session_state.supabase.table("partite").update({"pubblicata": True}).eq("giornata", g_num).execute()
            st.balloons()
            st.rerun()
    else:
        st.info("Palinsesto vuoto.")
except Exception as e: st.error(f"Errore: {e}")
