import streamlit as st

st.set_page_config(page_title="Compila Schedina", layout="wide")

# CSS PER BLOCCO MENU E STILE SCHEDINA
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

# --- MENU UTENTE ---
st.sidebar.title("🏆 Menu")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")

if "user" not in st.session_state:
    st.warning("Per favore, effettua il login dalla Home per giocare.")
    st.stop()

st.title("📝 La tua Schedina")

# Recuperiamo dal database solo le partite contrassegnate come "pubblicata = True" [cite: 2026-01-28]
try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    partite = res.data

    if partite:
        st.info(f"🏟️ Stai giocando la Giornata numero {partite[0]['giornata']}")
        
        pronostici_scelti = {}
        
        for p in partite:
            with st.container():
                st.markdown(f'<div class="match-container"><div class="match-title">{p["match"]}</div></div>', unsafe_allow_html=True)
                
                # Definiamo le quote disponibili [cite: 2026-01-28]
                quote_map = {
                    "1": p['quote_1'], "X": p['quote_x'], "2": p['quote_2'],
                    "1X": p['quote_1x'], "X2": p['quote_x2'], "12": p['quote_12'],
                    "U2.5": p['quote_u25'], "O2.5": p['quote_o25'], 
                    "GOAL": p['quote_g'], "NOGOAL": p['quote_ng']
                }
                
                # Selettore orizzontale moderno per mobile e desktop [cite: 2026-01-28]
                scelta = st.segmented_control(
                    "Seleziona il tuo esito:", 
                    options=list(quote_map.keys()), 
                    format_func=lambda x: f"{x} ({quote_map[x]})",
                    key=f"match_{p['id']}"
                )
                pronostici_scelti[p['id']] = scelta
                st.markdown("<br>", unsafe_allow_html=True)

        st.divider()
        if st.button("INVIA LA MIA SCHEDINA 📤", type="primary", use_container_width=True):
            # Controlliamo che tutte le partite abbiano una scelta [cite: 2026-01-28]
            if None not in pronostici_scelti.values():
                st.success("🚀 Schedina salvata! Buona fortuna per le partite.")
                st.balloons()
            else:
                st.error("⚠️ Devi selezionare un pronostico per ogni partita!")
    else:
        st.warning("Nessuna partita pubblicata per questa settimana. Riprova più tardi!")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
