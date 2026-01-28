import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca Schedina", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- STILE CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child { border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Accedi dalla Home per giocare.")
    st.stop()

st.title("⚽ La tua Schedina")

# Recupero partite (ordinate per ID per garantire l'ordine fisso)
res = supabase.table("partite").select("*").order("id", desc=False).limit(10).execute()
partite = res.data

if not partite:
    st.info("Nessuna partita disponibile.")
else:
    if "schedina" not in st.session_state:
        st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1, 2.5])

    # --- COLONNA DESTRA: SELEZIONE ---
    with col_partite:
        for p in partite:
            st.write(f"### {p['match']}")
            r1 = st.columns(5)
            r2 = st.columns(5)
            
            opzioni = [
                ("1", p['quote_1'], r1[0]), ("X", p['quote_x'], r1[1]), ("2", p['quote_2'], r1[2]),
                ("1X", p['quote_1x'], r1[3]), ("X2", p['quote_x2'], r1[4]),
                ("12", p['quote_12'], r2[0]), ("U2.5", p['quote_u25'], r2[1]), ("O2.5", p['quote_o25'], r2[2]),
                ("G", p['quote_g'], r2[3]), ("NG", p['quote_ng'], r2[4])
            ]

            for label, quota, slot in opzioni:
                btn_key = f"btn_{p['id']}_{label}"
                is_selected = st.session_state.schedina.get(p['id'], {}).get('segno') == label
                
                # Se selezionato, il tasto diventa rosso (primary)
                tipo = "primary" if is_selected else "secondary"
                
                if slot.button(f"{label}\n{quota}", key=btn_key, type=tipo, use_container_width=True):
                    st.session_state.schedina[p['id']] = {
                        "id_partita": p['id'], # Usato per l'ordinamento
                        "match": p['match'],
                        "segno": label,
                        "quota": quota,
                        "giornata": p['giornata']
                    }
                    st.rerun()

    # --- COLONNA SINISTRA: RIEPILOGO ORDINATO ---
    with col_riepilogo:
        st.subheader("📋 Riepilogo")
        somma_quote = 0.0
        contatore = 0
        
        # Ordiniamo gli elementi della schedina per ID prima di mostrarli
        schedina_ordinata = dict(sorted(st.session_state.schedina.items()))
        
        for p_id, info in schedina_ordinata.items():
            st.info(f"**{info['match']}**\n{info['segno']} (@{info['quota']})")
            somma_quote += info['quota'] # CALCOLO DELLA SOMMA
            contatore += 1
        
        st.metric("Somma Quote Totale", f"{somma_quote:.2f}")
        st.write(f"Selezionate: {contatore}/10")
        
        btn_off = contatore < 10
        if st.button("SALVA GIOCATA", disabled=btn_off, use_container_width=True, type="primary"):
            try:
                dati_db = []
                for p_id, info in st.session_state.schedina.items():
                    dati_db.append({
                        "user_id": st.session_state.user.id,
                        "email_utente": st.session_state.user.email,
                        "partita_id": info['id_partita'],
                        "pronostico": info['segno'],
                        "quota_giocata": info['quota'],
                        "giornata": info['giornata']
                    })
                supabase.table("pronostici").insert(dati_db).execute()
                st.success("✅ Salvata!")
                st.balloons()
                st.session_state.schedina = {} # Reset
            except Exception as e:
                st.error(f"Errore: {e}")
