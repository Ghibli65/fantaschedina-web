import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

# --- CSS AVANZATO PER COMPATTEZZA E COLORI ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    
    /* Titolo e Header */
    .main-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 15px; border-radius: 12px;
        text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px;
    }
    
    /* Riduzione font tabella per far stare tutto */
    [data-testid="stTable"] td, [data-testid="stTable"] th { font-size: 12px !important; }
    .stDataEditor div { font-size: 13px !important; }
    
    /* Colori Sezioni */
    .section-card {
        background-color: #ffffff; border: 1px solid #e0e0e0;
        padding: 15px; border-radius: 10px; border-top: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PROTEZIONE ACCESSO ---
if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato.")
    st.stop()

# --- MENU LATERALE ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica/Modifica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

st.markdown('<div class="main-title">🚀 GESTIONE PALINSESTO CALCIO</div>', unsafe_allow_html=True)

# --- SEZIONE CARICAMENTO (EXPANDER) ---
with st.expander("➕ AGGIUNGI NUOVE PARTITE (CLICCA QUI)", expanded=False):
    c1, c2 = st.columns([1, 4])
    with c1:
        g_num = st.number_input("Giorn.", min_value=1, step=1, value=1)
    with c2:
        bulk = st.text_area("Incolla: Squadre;1;X;2;1X;X2;12;U;O;G;NG", height=80)
    
    if st.button("CARICA DATI", type="primary", use_container_width=True):
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
                        "quote_ng": q(p[10]), "giornata": g_num
                    }).execute()
                st.success("✅ Partite aggiunte con successo!")
                st.rerun()
            except Exception as e:
                st.error(f"Errore: {e}")

st.markdown('<br>', unsafe_allow_html=True)

# --- TABELLA DI MODIFICA ULTRA-STRETTA ---
st.markdown('<div class="section-card"><b>📝 MODIFICA PARTITE CARICATE</b> (Modifica celle e clicca Salva)</div>', unsafe_allow_html=True)

try:
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df_partite = pd.DataFrame(res.data)

    if not df_partite.empty:
        # Configurazione colonne millimetrica per evitare lo scroll [cite: 2026-01-28]
        edited_df = st.data_editor(
            df_partite,
            key="palinsesto_editor",
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_order=("giornata", "match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "giornata": st.column_config.NumberColumn("G.", width=40),
                "match": st.column_config.TextColumn("PARTITA", width=180),
                "quote_1": st.column_config.NumberColumn("1", format="%.2f", width=45),
                "quote_x": st.column_config.NumberColumn("X", format="%.2f", width=45),
                "quote_2": st.column_config.NumberColumn("2", format="%.2f", width=45),
                "quote_1x": st.column_config.NumberColumn("1X", format="%.2f", width=45),
                "quote_x2": st.column_config.NumberColumn("X2", format="%.2f", width=45),
                "quote_12": st.column_config.NumberColumn("12", format="%.2f", width=45),
                "quote_u25": st.column_config.NumberColumn("U", format="%.2f", width=40),
                "quote_o25": st.column_config.NumberColumn("O", format="%.2f", width=40),
                "quote_g": st.column_config.NumberColumn("G", format="%.2f", width=40),
                "quote_ng": st.column_config.NumberColumn("NG", format="%.2f", width=40),
            }
        )

        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("💾 SALVA TUTTE LE MODIFICHE", type="primary", use_container_width=True):
            for _, row in edited_df.iterrows():
                st.session_state.supabase.table("partite").update({
                    "match": row["match"], "giornata": row["giornata"],
                    "quote_1": row["quote_1"], "quote_x": row["quote_x"], "quote_2": row["quote_2"],
                    "quote_1x": row["quote_1x"], "quote_x2": row["quote_x2"], "quote_12": row["quote_12"],
                    "quote_u25": row["quote_u25"], "quote_o25": row["quote_o25"], 
                    "quote_g": row["quote_g"], "quote_ng": row["quote_ng"]
                }).eq("id", row["id"]).execute()
            st.success("✨ Database aggiornato!")
            st.rerun()
    else:
        st.info("Nessuna partita in archivio.")

except Exception as e:
    st.error(f"Errore: {e}")
