import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca Schedina", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    /* Rende i bottoni più alti per ospitare Segno e Quota */
    div.stButton > button {
        height: 60px !important;
        line-height: 1.2 !important;
        border-radius: 8px !important;
    }
    /* Colore rosso per il valore della somma */
    [data-testid="stMetricValue"] { color: #ff4b4b; }
    /* Box riepilogo ordinato */
    .stInfo { border-left: 5px solid #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Accedi dalla Home Page per poter giocare.")
    st.stop()

st.title("⚽ Piazza i tuoi Pronostici")

# 1. Recupero partite ordinate per ID (ordine fisso di inserimento)
res = supabase.table("partite").select("*").order("id", desc=False).limit(10).execute()
partite = res.data

if not partite:
    st.info("ℹ️ L'amministratore sta caricando le partite. Torna tra poco!")
else:
    if "schedina" not in st.session_state:
        st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1.2, 3])

    # --- COLONNA DESTRA: GRIGLIA DI SELEZIONE ---
    with col_partite:
        for p in partite:
            st.subheader(f"🏟️ {p['match']}")
            
            r1 = st.columns(5)
            r2 = st.columns(5)
            
            # Mappatura esatta delle colonne del DB
            opzioni = [
                ("1", p.get('quote_1', 0), r1[0]), 
                ("X", p.get('quote_x', 0), r1[1]), 
                ("2", p.get('quote_2', 0), r1[2]),
                ("1X", p.get('quote_1x', 0), r1[3]), 
                ("X2", p.get('quote_x2', 0), r1[4]),
                ("12", p.get('quote_12', 0), r2[0]), 
                ("U2.5", p.get('quote_u25', 0), r2[1]), 
                ("O2.5", p.get('quote_o25', 0), r2[2]),
                ("G", p.get('quote_g', 0), r2[3]), 
                ("NG", p.get('quote_ng', 0), r2[4])
            ]

            for label, quota, slot in opzioni:
                # Creiamo l'etichetta con il segno sopra e la quota sotto
                testo_bottone = f"{label}\n{quota:.2f}"
                
                btn_key = f"btn_{p['id']}_{label}"
                is_selected = st.session_state.schedina.get(p['id'], {}).get('segno') == label
                
                # Selezionato = Rosso (primary), Non selezionato = Grigio (secondary)
                if slot.button(testo_bottone, key=btn_key, type="primary" if is_selected else "secondary", use_container_width=True):
                    st.session_state.schedina[p['id']] = {
                        "id_partita": p['id'],
                        "match": p['match'],
                        "segno": label,
                        "quota": quota,
                        "giornata": p['giornata']
                    }
                    st.rerun()
            st.divider()

    # --- COLONNA SINISTRA: RIEPILOGO ORDINATO E SOMMA ---
    with col_riepilogo:
        st.sticky_header = st.container()
        with st.sticky_header:
            st.subheader("📋 Schedina")
            somma_quote = 0.0
            
            # Ordiniamo la schedina per ID prima della visualizzazione
            schedina_ordinata = dict(sorted(st.session_state.schedina.items()))
            
            for p_id, info in schedina_ordinata.items():
                st.info(f"**{info['match']}**\nEsito: **{info['segno']}** (@{info['quota']:.2f})")
                somma_quote += info['quota']
            
            st.metric("SOMMA QUOTE TOTALE", f"{somma_quote:.2f}")
            
            contatore = len(st.session_state.schedina)
            st.write(f"Partite selezionate: **{contatore}/10**")
            
            # Il tasto si abilita solo se hai scelto per tutte e 10 le partite
            btn_disabled = contatore < 10
            
            if st.button("🚀 SALVA GIOCATA", disabled=btn_disabled, use_container_width=True, type="primary"):
                try:
                    per_db = []
                    for p_id, info in st.session_state.schedina.items():
                        per_db.append({
                            "user_id": st.session_state.user.id,
                            "email_utente": st.session_state.user.email,
                            "partita_id": info['id_partita'],
                            "pronostico": info['segno'],
                            "quota_giocata": info['quota'],
                            "giornata": info['giornata']
                        })
                    
                    supabase.table("pronostici").insert(per_db).execute()
                    st.success("✅ Schedina salvata nel database!")
                    st.balloons()
                    st.session_state.schedina = {} # Reset dopo il successo
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nel salvataggio: {e}")
