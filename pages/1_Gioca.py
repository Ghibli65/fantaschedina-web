import streamlit as st

st.set_page_config(page_title="Gioca Schedina", layout="wide")

# CSS PER BLOCCO MENU AUTOMATICO
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;} .match-box {background-color: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 10px;}</style>""", unsafe_allow_html=True)

# --- MENU UTENTE ---
st.sidebar.title("🏆 FantaSchedina")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

st.title("⚽ La tua Schedina")

# Carichiamo solo le partite pubblicate [cite: 2026-01-28]
try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    partite = res.data

    if partite:
        st.info(f"📅 Giornata in corso: {partite[0]['giornata']}")
        schedina_utente = {}

        for p in partite:
            st.markdown(f'<div class="match-box"><b>{p["match"]}</b></div>', unsafe_allow_html=True)
            
            # Griglia di pulsanti per i pronostici [cite: 2026-01-28]
            opzioni = {
                "1": p['quote_1'], "X": p['quote_x'], "2": p['quote_2'],
                "1X": p['quote_1x'], "X2": p['quote_x2'], "12": p['quote_12'],
                "U2.5": p['quote_u25'], "O2.5": p['quote_o25'], 
                "GOAL": p['quote_g'], "NOGOAL": p['quote_ng']
            }
            
            # L'utente sceglie l'esito [cite: 2026-01-28]
            scelta = st.segmented_control(
                "Scegli il pronostico:", 
                options=list(opzioni.keys()), 
                format_func=lambda x: f"{x} ({opzioni[x]})",
                key=f"pick_{p['id']}"
            )
            schedina_utente[p['id']] = scelta
            st.divider()

        if st.button("INVIA SCHEDINA 📤", type="primary", use_container_width=True):
            if all(schedina_utente.values()):
                # Qui il sistema è pronto per salvare i dati su Supabase [cite: 2026-01-28]
                st.success("✅ Schedina inviata! In bocca al lupo!")
                st.balloons()
            else:
                st.warning("⚠️ Completa tutte le partite prima di inviare!")
    else:
        st.warning("⏳ L'amministratore non ha ancora pubblicato le partite per questa giornata.")

except Exception as e:
    st.error(f"Errore caricamento: {e}")
