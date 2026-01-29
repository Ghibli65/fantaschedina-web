import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Palinsesto", layout="wide")

# --- CSS PER STILE VIVACE E COMPATTO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    /* Colori per le sezioni */
    .main-title {color: #2e7d32; font-size: 28px; font-weight: bold;}
    .section-header {background-color: #e8f5e9; padding: 10px; border-radius: 10px; border-left: 5px solid #2e7d32; margin-bottom: 20px;}
    /* Tabella più compatta */
    .stDataEditor {max-height: 400px;}
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

st.markdown('<p class="main-title">🚀 Gestione Palinsesto</p>', unsafe_allow_html=True)

# --- SEZIONE 1: CARICAMENTO RAPIDO (COMPATTO) ---
with st.expander("➕ Inserimento Rapido Nuove Partite", expanded=False):
    c1, c2 = st.columns([1, 3])
    with c1:
        g_num = st.number_input("Giornata", min_value=1, step=1, value=1)
    with c2:
        bulk = st.text_area("Incolla dati (Squadre;1;X;2...)", height=100, help="Separa i valori con ';'")
    
    if st.button("CARICA ORA", type="primary", use_container_width=True):
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
                st.success("✅ Partite aggiunte!")
                st.rerun()
            except Exception as e:
                st.error(f"Formato errato: {e}")

st.markdown('<div class="section-header">📝 <b>Modifica Palinsesto:</b> Clicca sulle celle per correggere quote o giornata</div>', unsafe_allow_html=True)

# --- SEZIONE 2: TABELLA MODIFICA VIVACE ---
try:
    # Carichiamo TUTTE le partite per permettere la modifica globale
    res = st.session_state.supabase.table("partite").select("*").order("giornata").execute()
    df_partite = pd.DataFrame(res.data)

    if not df_partite.empty:
        # Configuriamo l'editor per essere compatto e includere la GIORNATA
        edited_df = st.data_editor(
            df_partite,
            key="palinsesto_editor",
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic", # Permette di eliminare righe con il tasto Canc
            column_order=("giornata", "match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "giornata": st.column_config.NumberColumn("Giorn.", width="small", format="%d"),
                "match": st.column_config.TextColumn("Partita", width="medium"),
                "quote_1": st.column_config.NumberColumn("1", format="%.2f", width="small"),
                "quote_x": st.column_config.NumberColumn("X", format="%.2f", width="small"),
                "quote_2": st.column_config.NumberColumn("2", format="%.2f", width="small"),
            }
        )

        c_save, c_info = st.columns([1, 2])
        with c_save:
            if st.button("💾 SALVA MODIFICHE", use_container_width=True):
                # Logica di aggiornamento massivo
                for _, row in edited_df.iterrows():
                    st.session_state.supabase.table("partite").update({
                        "match": row["match"], "giornata": row["giornata"],
                        "quote_1": row["quote_1"], "quote_x": row["quote_x"], "quote_2": row["quote_2"],
                        "quote_1x": row["quote_1x"], "quote_x2": row["quote_x2"], "quote_12": row["quote_12"],
                        "quote_u25": row["quote_u25"], "quote_o25": row["quote_o25"], 
                        "quote_g": row["quote_g"], "quote_ng": row["quote_ng"]
                    }).eq("id", row["id"]).execute()
                st.success("✨ Modifiche salvate con successo!")
                st.rerun()
        with c_info:
            st.caption("💡 Suggerimento: Seleziona una riga e premi 'Canc' per eliminarla.")

    else:
        st.write("Nessuna partita presente.")

except Exception as e:
    st.error(f"Errore caricamento: {e}")
