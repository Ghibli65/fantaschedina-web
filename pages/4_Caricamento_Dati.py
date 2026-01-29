import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

# CSS PER ELIMINARE BARRE E SCROLL
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataEditor { width: 100% !important; }
    .stDataEditor div[data-testid="stTable"] { overflow: hidden !important; }
    .main-title {background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 10px; border-radius: 8px; text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato.")
    st.stop()

st.sidebar.title("⚙️ Admin")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Palinsesto", icon="🚀")

st.markdown('<div class="main-title">🚀 ADMIN: GESTIONE QUOTE</div>', unsafe_allow_html=True)

try:
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        # Configurazione compatta
        edited_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True, 
            num_rows="dynamic",
            column_order=("pubblicata", "giornata", "match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "pubblicata": st.column_config.CheckboxColumn("LIVE", width=40),
                "giornata": st.column_config.NumberColumn("G.", width=35),
                "match": st.column_config.TextColumn("PARTITA", width=170),
                "quote_1": st.column_config.NumberColumn("1", width=42),
                "quote_x": st.column_config.NumberColumn("X", width=42),
                "quote_2": st.column_config.NumberColumn("2", width=42),
                "quote_1x": st.column_config.NumberColumn("1X", width=42),
                "quote_x2": st.column_config.NumberColumn("X2", width=42),
                "quote_12": st.column_config.NumberColumn("12", width=42),
            }
        )

        if st.button("💾 SALVA TUTTO", type="primary", use_container_width=True):
            for _, row in edited_df.iterrows():
                st.session_state.supabase.table("partite").update({
                    "pubblicata": row["pubblicata"], "match": row["match"], "giornata": row["giornata"],
                    "quote_1": row["quote_1"], "quote_x": row["quote_x"], "quote_2": row["quote_2"],
                    "quote_1x": row["quote_1x"], "quote_x2": row["quote_x2"], "quote_12": row["quote_12"],
                    "quote_u25": row["quote_u25"], "quote_o25": row["quote_o25"], "quote_g": row["quote_g"], "quote_ng": row["quote_ng"]
                }).eq("id", row["id"]).execute()
            st.success("✅ Salvato!")
            st.rerun()
except Exception as e: st.error(f"Errore: {e}")
