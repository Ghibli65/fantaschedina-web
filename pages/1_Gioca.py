import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca Schedina", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    /* Rende i bottoni più alti e leggibili */
    div.stButton > button {
        height: 75px !important;
        white-space: pre-wrap !important;
        line-height: 1.2 !important;
        border-radius: 10px !important;
    }
    /* Colore rosso per il valore della somma totale */
    [data-testid="stMetricValue"] { color: #ff4b4b; }
    /* Box riepilogo laterale */
    .stInfo { border-left: 5px solid #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# Controllo se l'utente è loggato
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Per favore, effettua il login dalla Home Page per giocare.")
    st.stop()

st.title("⚽ La tua Schedina")

# 1. Recupero delle partite (ordinate per ID per mantenere l'ordine fisso)
res = supabase.table("partite").select("*").order("id", desc=False).limit(10).execute()
partite = res.data

if not partite:
    st.info("ℹ️ Nessuna partita disponibile. Attendi che l'amministratore carichi la giornata.")
else:
    # Inizializzazione dello stato della schedina
    if "schedina" not in st.session_state:
        st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1.3, 3])

    # --- COLONNA DESTRA: SELEZIONE PRONOSTICI ---
    with col_partite:
        for p in partite:
            st.subheader(f"🏟️ {p['match']}")
            
            r1 = st.columns(5)
            r2 = st.columns(5)
            
            # Mappatura delle quote basata sul tuo formato database
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
                # Se la quota è presente mostra il valore, altrimenti N.D.
                valore_visualizzato = f"{quota:.2f}" if quota and quota > 0 else "N.D."
                testo_bottone = f"{label}\n{valore_visualizzato}"
                
                btn_key = f"btn_{p['id']}_{label}"
                is_selected = st.session_state.schedina.get(p['id'], {}).get('segno') == label
                
                # Selezionato = Rosso (primary), Non selezionato = Grigio (secondary)
                if slot.button(testo_bottone, key=btn_key, type="primary" if is_selected else "secondary", use_container_width=True):
                    st.session_state.schedina[p['id']] = {
                        "id_partita": p['id'],
                        "match": p['match'],
                        "segno": label,
                        "quota": float(quota) if quota else 0.0,
                        "giornata": p['giornata']
                    }
                    st.rerun()
            st.divider()

    # --- COLONNA SINISTRA: RIEPILOGO ORDINATO E SOMMA ---
    with col_riepilogo:
        st.subheader("📋 Riepilogo")
        somma_totale = 0.0
        
        # Ordiniamo i pronostici per ID per riflettere l'ordine delle partite a destra
        schedina_ordinata = dict(sorted(st.session_state.schedina.items()))
        
        for p_id, info in schedina_ordinata.items():
            st.info(f"**{info['match']}**\nEsito: **{info['segno']}** (@{info['quota']:.2f})")
            somma_totale += info['quota'] # Calcolo della SOMMA [cite: 2026-01-26]
        
        st.metric("SOMMA QUOTE TOTALE", f"{somma_totale:.2f}")
        
        partite_selezionate = len(st.session_state.schedina)
        st.write(f"Partite completate: **{partite_selezionate}/10**")
        
        # Il tasto si abilita solo se sono state selezionate tutte e 10 le partite [cite: 2026-01-26]
        disabilitato = partite_selezionate < 10
        
        if st.button("🚀 SALVA SCHEDINA", disabled=disabilitato, use_container_width=True, type="primary"):
            try:
                dati_per_db = []
                for p_id, info in st.session_state.schedina.items():
                    dati_per_db.append({
                        "user_id": st.session_state.user.id,
                        "email_utente": st.session_state.user.email,
                        "partita_id": info['id_partita'],
                        "pronostico": info['segno'],
                        "quota_giocata": info['quota'],
                        "giornata": info['giornata']
                    })
                
                supabase.table("pronostici").insert(dati_per_db).execute()
                st.success("✅ Schedina salvata con successo!")
                st.balloons()
                st.session_state.schedina = {} # Reset dopo il salvataggio
                st.rerun()
            except Exception as e:
                st.error(f"Errore nel salvataggio: {e}")

