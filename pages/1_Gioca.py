import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gioca Schedina", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .stDataEditor { width: 100% !important; }
    .match-row { padding: 10px; border-bottom: 1px solid #eee; display: flex; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Per favore, effettua il login dalla Home.")
    st.stop()

st.title("⚽ La tua Schedina")

try:
    # Carichiamo solo le partite pubblicate
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        st.success(f"📅 Giornata {df['giornata'].iloc[0]} disponibile!")
        
        # TABELLA QUOTE IDENTICA AD ADMIN (SOLA LETTURA)
        st.write("### 📊 Consulta le Quote")
        st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "match": st.column_config.TextColumn("PARTITA", width=180),
                "quote_1": st.column_config.NumberColumn("1", width=42),
                "quote_x": st.column_config.NumberColumn("X", width=42),
                "quote_2": st.column_config.NumberColumn("2", width=42),
                "quote_1x": st.column_config.NumberColumn("1X", width=42),
                "quote_x2": st.column_config.NumberColumn("X2", width=42),
                "quote_12": st.column_config.NumberColumn("12", width=42),
                "quote_u25": st.column_config.NumberColumn("U", width=42),
                "quote_o25": st.column_config.NumberColumn("O", width=42),
                "quote_g": st.column_config.NumberColumn("G", width=42),
                "quote_ng": st.column_config.NumberColumn("NG", width=42),
            }
        )

        st.divider()
        st.write("### ✍️ Compila i tuoi Pronostici")
        
        pronostici = {}
        for _, p in df.iterrows():
            st.markdown(f"**{p['match']}**")
            # Selettore pronostico per ogni partita
            scelta = st.segmented_control(
                "Esito:", 
                options=["1", "X", "2", "1X", "X2", "12", "U", "O", "G", "NG"], 
                key=f"p_{p['id']}",
                label_visibility="collapsed"
            )
            pronostici[p['id']] = scelta
            st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            if None not in pronostici.values():
                # Qui inseriremo la logica di salvataggio definitiva nel DB
                st.balloons()
                st.success("Schedina inviata correttamente!")
            else:
                st.error("⚠️ Devi pronosticare tutte le partite!")
                
    else:
        st.warning("Nessun palinsesto Live al momento.")

except Exception as e: st.error(f"Errore: {e}")
