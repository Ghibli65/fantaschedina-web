import streamlit as st

st.set_page_config(page_title="Compila Schedina", layout="wide")

st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

if "user" not in st.session_state:
    st.warning("Esegui il login dalla Home.")
    st.stop()

st.title("📝 La tua Schedina")

if st.button("🔄 AGGIORNA PALINSESTO"):
    st.rerun()

try:
    # Cerchiamo solo le partite dove pubblicata è True
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    partite = res.data

    if partite:
        st.success(f"🏟️ Palinsesto LIVE trovato! Giornata: {partite[0]['giornata']}")
        pronostici = {}
        for p in partite:
            with st.container():
                st.subheader(p['match'])
                scelta = st.segmented_control("Pronostico:", options=["1", "X", "2", "U", "O", "G", "NG"], key=f"m_{p['id']}")
                pronostici[p['id']] = scelta
        
        if st.button("INVIA SCHEDINA 📤", type="primary", use_container_width=True):
            if None not in pronostici.values():
                st.balloons()
                st.success("Schedina inviata!")
            else:
                st.error("Completa tutte le partite!")
    else:
        st.warning("⚠️ Nessun palinsesto Live. Chiedi all'Admin di pubblicare la giornata.")
        # Debug per l'admin: mostra quante partite totali ci sono nel DB (anche non pubblicate)
        total = st.session_state.supabase.table("partite").select("id", count="exact").execute()
        st.caption(f"(Debug: Partite totali nel database: {total.count if total.count else 0})")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
