import streamlit as st

st.set_page_config(page_title="Gioca Schedina", layout="wide")

st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

if "user" not in st.session_state:
    st.warning("Esegui il login per giocare.")
    st.stop()

st.title("📝 La tua Schedina")

# Carichiamo le partite che hanno 'pubblicata' uguale a True
try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    partite = res.data

    if partite:
        st.success(f"🏟️ Giornata {partite[0]['giornata']} disponibile!")
        
        pronostici = {}
        for p in partite:
            with st.container():
                st.markdown(f"### {p['match']}")
                scelta = st.segmented_control(
                    "Scegli l'esito:", 
                    options=["1", "X", "2", "U", "O", "G", "NG"], 
                    key=f"match_{p['id']}"
                )
                pronostici[p['id']] = scelta
                st.divider()

        if st.button("INVIA SCHEDINA 📤", type="primary", use_container_width=True):
            if None not in pronostici.values():
                st.balloons()
                st.success("✅ Schedina inviata!")
            else:
                st.error("⚠️ Compila tutte le partite prima di inviare.")
    else:
        st.warning("⚠️ L'Admin non ha ancora pubblicato le partite per questa settimana.")
        # Debug per l'Admin
        st.caption(f"Info tecnica: Loggato come {st.session_state.user.email}")

except Exception as e:
    st.error(f"Errore nel caricamento: {e}")
