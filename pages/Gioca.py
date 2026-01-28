import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca Schedina", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- STILE CSS PER BOTTONI ROSSI ---
st.markdown("""
    <style>
    /* Stile per i bottoni selezionati */
    div.stButton > button.selected {
        background-color: #ff4b4b !important;
        color: white !important;
        border: 2px solid #800000 !important;
    }
    /* Allineamento colonna sinistra */
    [data-testid="stVerticalBlock"] > div:has(div.stInfo) {
        border-left: 3px solid #ff4b4b;
        padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Fai il login in Home Page per giocare!")
    st.stop()

st.title("⚽ La tua Schedina")

# Recupero ultime 10 partite caricate
res = supabase.table("partite").select("*").order("id", desc=True).limit(10).execute()
partite = res.data

if not partite:
    st.info("Attendi che l'Admin carichi le partite della giornata.")
else:
    # Stato della schedina
    if "schedina" not in st.session_state:
        st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1, 3])

    # --- COLONNA DESTRA: SELEZIONE ---
    with col_partite:
        st.subheader("Seleziona i tuoi pronostici")
        for p in partite:
            st.write(f"**{p['match']}**")
            
            # Griglia quote
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
                # Verifica se questo esito è quello selezionato
                is_selected = st.session_state.schedina.get(p['id'], {}).get('segno') == label
                
                if slot.button(f"{label}\n{quota}", key=btn_key, 
                               help=f"Quota: {quota}",
                               type="secondary" if not is_selected else "primary"):
                    st.session_state.schedina[p['id']] = {
                        "p_id": p['id'],
                        "match": p['match'],
                        "segno": label,
                        "quota": quota,
                        "giornata": p['giornata']
                    }
                    st.rerun() # Aggiorna subito la colonna sinistra
            st.divider()

    # --- COLONNA SINISTRA: SCHEDINA ---
    with col_riepilogo:
        st.subheader("📋 Riepilogo")
        tot_quota = 1.0
        contatore = 0
        
        for p_id, info in st.session_state.schedina.items():
            st.info(f"**{info['match']}**\n{info['segno']} @{info['quota']}")
            tot_quota *= info['quota']
            contatore += 1
        
        if contatore > 0:
            st.metric("Quota Totale", f"{tot_quota:.2f}")
        
        st.write(f"Partite: {contatore}/10")
        
        # Il tasto si abilita solo con 10 partite
        btn_disabilitato = contatore < 10
        
        if st.button("SALVA SCHEDINA", disabled=btn_disabilitato, use_container_width=True):
            try:
                per_database = []
                for p_id, info in st.session_state.schedina.items():
                    per_database.append({
                        "user_id": st.session_state.user.id,
                        "email_utente": st.session_state.user.email,
                        "partita_id": info['p_id'],
                        "pronostico": info['segno'],
                        "quota_giocata": info['quota'],
                        "giornata": info['giornata']
                    })
                
                supabase.table("pronostici").insert(per_database).execute()
                st.success("✅ Giocata registrata!")
                st.balloons()
                # Pulisce la schedina dopo il salvataggio
                st.session_state.schedina = {}
            except Exception as e:
                st.error(f"Errore nel salvataggio: {e}")
