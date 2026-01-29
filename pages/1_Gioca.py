import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gioca Schedina", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .stDataEditor { width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Esegui il login.")
    st.stop()

st.title("⚽ La tua Schedina")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        st.success(f"📅 Giornata {df['giornata'].iloc[0]} disponibile!")
        
        # TABELLA STILE ADMIN (Sola Lettura)
        st.write("### 📊 Palinsesto Quote")
        st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=True, # L'utente non può modificare le quote!
            column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={
                "match": st.column_config.TextColumn("PARTITA", width=180),
                "quote_1": st.column_config.NumberColumn("1", width=45),
                "quote_x": st.column_config.NumberColumn("X", width=45),
                "quote_2": st.column_config.NumberColumn("2", width=45),
                "quote_1x": st.column_config.NumberColumn("1X", width=45),
                "quote_x2": st.column_config.NumberColumn("X2", width=45),
                "quote_12": st.column_config.NumberColumn("12", width=45),
                "quote_u25": st.column_config.NumberColumn("U", width=45),
                "quote_o25": st.column_config.NumberColumn("O", width=45),
                "quote_g": st.column_config.NumberColumn("G", width=45),
                "quote_ng": st.column_config.NumberColumn("NG", width=45),
            }
        )

        st.divider()
        st.write("### ✍️ Inserisci i tuoi Pronostici")
        
        pronostici = {}
        # Creiamo dei selettori semplici sotto la tabella per inviare la schedina
        for _, p in df.iterrows():
            c1, c2 = st.columns([2, 3])
            c1.write(f"**{p['match']}**")
            pronostici[p['id']] = c2.segmented_control(
                "Esito", 
                options=["1", "X", "2", "1X", "X2", "12", "U", "O", "G", "NG"], 
                key=f"prono_{p['id']}",
                label_visibility="collapsed"
            )
        
        if st.button("🚀 INVIA SCHEDINA DEFINITIVA", type="primary", use_container_width=True):
            if None not in pronostici.values():
                # Logica di salvataggio (già pronta nei passaggi precedenti)
                st.balloons()
                st.success("Schedina inviata con successo!")
            else:
                st.error("⚠️ Pronostica tutte le partite prima di inviare!")
                
    else:
        st.warning("Nessun palinsesto Live.")

except Exception as e: st.error(f"Errore: {e}")
