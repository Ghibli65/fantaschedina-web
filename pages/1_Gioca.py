import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataEditor { width: 100% !important; }
    /* Nasconde scrollbar inutili */
    .stDataEditor div[data-testid="stTable"] { overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.page_link("app.py", label="Torna alla Home", icon="🏠")

if "user" not in st.session_state:
    st.error("Esegui il login per giocare.")
    st.stop()

st.title("📝 Compila la Schedina")

try:
    # Recupero partite pubblicate [cite: 2026-01-29]
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        st.write(f"### 📊 Palinsesto Giornata {df['giornata'].iloc[0]}")
        
        # TABELLA QUOTE SOLA LETTURA (Stile Admin) [cite: 2026-01-29]
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
                "quote_u25": st.column_config.NumberColumn("U", width=40),
                "quote_o25": st.column_config.NumberColumn("O", width=40),
                "quote_g": st.column_config.NumberColumn("G", width=40),
                "quote_ng": st.column_config.NumberColumn("NG", width=40),
            }
        )

        st.divider()
        st.subheader("✍️ Inserisci i Pronostici")
        
        pronostici = {}
        for _, p in df.iterrows():
            st.write(f"**{p['match']}**")
            pronostici[p['id']] = st.segmented_control(
                "Scegli:", 
                options=["1", "X", "2", "1X", "X2", "12", "U", "O", "G", "NG"], 
                key=f"match_{p['id']}",
                label_visibility="collapsed"
            )
            st.markdown("---")

        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            if None not in pronostici.values():
                # Qui aggiungerai la logica di inserimento nella tabella 'pronostici' [cite: 2026-01-29]
                st.balloons()
                st.success("Schedina inviata!")
            else:
                st.error("⚠️ Pronostica tutte le partite!")
    else:
        st.warning("Nessuna partita pubblicata.")
except Exception as e:
    st.error(f"Errore caricamento: {e}")
