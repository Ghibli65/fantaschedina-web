import streamlit as st

st.set_page_config(page_title="Compila Schedina", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .match-container {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 1px solid #eee; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .match-title { color: #1e3c72; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

if "user" not in st.session_state:
    st.error("🚨 Effettua il login dalla Home.")
    st.stop()

st.title("📝 La tua Schedina")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    partite = res.data

    if partite:
        giornata_attuale = partite[0]['giornata']
        st.info(f"🏟️ Giornata {giornata_attuale}")
        
        pronostici_scelti = {}
        
        for p in partite:
            with st.container():
                st.markdown(f'<div class="match-container"><div class="match-title">{p["match"]}</div></div>', unsafe_allow_html=True)
                quote_map = {"1": p['quote_1'], "X": p['quote_x'], "2": p['quote_2'], "1X": p['quote_1x'], "X2": p['quote_x2'], "12": p['quote_12'], "U": p['quote_u25'], "O": p['quote_o25'], "G": p['quote_g'], "NG": p['quote_ng']}
                
                scelta = st.segmented_control("Pronostico:", options=list(quote_map.keys()), format_func=lambda x: f"{x} ({quote_map[x]})", key=f"m_{p['id']}")
                pronostici_scelti[p['id']] = scelta

        if st.button("INVIA LA MIA SCHEDINA 📤", type="primary", use_container_width=True):
            if None not in pronostici_scelti.values():
                try:
                    # Salvataggio nel Database [cite: 2026-01-28]
                    for p_id, esito in pronostici_scelti.items():
                        st.session_state.supabase.table("pronostici").insert({
                            "user_id": st.session_state.user.id,
                            "partita_id": p_id,
                            "scelta": esito,
                            "giornata": giornata_attuale
                        }).execute()
                    st.success("🚀 Schedina salvata con successo nel Database!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Errore nel salvataggio: {e}")
            else:
                st.error("⚠️ Pronostica tutti i match!")
    else:
        st.warning("Nessun palinsesto Live.")
except Exception as e:
    st.error(f"Errore: {e}")
