import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gioca Schedina", layout="wide")

st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

if "user" not in st.session_state:
    st.warning("Esegui il login per giocare.")
    st.stop()

st.title("⚽ La tua Schedina")

try:
    # Mostriamo solo partite LIVE
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        st.info(f"🏟️ Giornata {df['giornata'].iloc[0]} disponibile!")
        
        # Tabella Quote (Sola Lettura)
        st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            column_config={"match": "PARTITA", "quote_1": "1", "quote_x": "X", "quote_2": "2"}
        )

        st.divider()
        st.subheader("✍️ Pronostici")
        
        pronostici = {}
        for _, p in df.iterrows():
            st.markdown(f"**{p['match']}**")
            pronostici[p['id']] = st.segmented_control(
                "Esito", 
                options=["1", "X", "2", "1X", "X2", "12", "U", "O", "G", "NG"], 
                key=f"p_{p['id']}",
                label_visibility="collapsed"
            )
        
        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            if None not in pronostici.values():
                # Salvataggio nel DB
                for p_id, esito in pronostici.items():
                    st.session_state.supabase.table("pronostici").insert({
                        "user_id": st.session_state.user.id,
                        "partita_id": p_id,
                        "scelta": esito,
                        "giornata": int(df['giornata'].iloc[0])
                    }).execute()
                st.balloons()
                st.success("✅ Schedina registrata!")
            else:
                st.error("⚠️ Compila tutte le partite!")
    else:
        st.warning("Nessun palinsesto Live.")
except Exception as e: st.error(f"Errore: {e}")
