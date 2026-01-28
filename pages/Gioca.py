import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca Schedina", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- STILE CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        height: 70px !important;
        white-space: pre-wrap !important; /* Permette l'andata a capo */
        line-height: 1.2 !important;
    }
    [data-testid="stMetricValue"] { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Effettua il login in Home Page.")
    st.stop()

st.title("⚽ La tua Schedina")

# 1. Recupero partite
res = supabase.table("partite").select("*").order("id", desc=False).limit(10).execute()
partite = res.data

if not partite:
    st.info("ℹ️ Nessuna partita caricata dall'Admin.")
else:
    if "schedina" not in st.session_state:
        st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1.2, 3])

    with col_partite:
        for p in partite:
            st.subheader(f"🏟️ {p['match']}")
            
            r1 = st.columns(5)
            r2 = st.columns(5)
            
            # NOTA: Usiamo .get() con i nomi delle colonne TUTTI MINUSCOLI 
            # come creato nel comando SQL ALTER TABLE
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
                # Se la quota è 0 o None, mostriamo 'N.D.' (Non Disponibile)
                valore_quota = f"{quota:.2f}" if quota and quota > 0 else "N.D."
                testo_bottone = f"{label}\n{valore_quota}"
                
                btn_key = f"btn_{p['id']}_{label}"
                is_selected = st.session_state.schedina.get(p['id'], {}).get('segno') == label
                
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

    with col_riepilogo:
        st.subheader("📋 Riepilogo")
        somma_quote = 0.0
        
        # Ordinamento fisso per ID
        schedina_ordinata = dict(sorted(st.session_state.schedina.items()))
        
        for p_id, info in schedina_ordinata.items():
            st.info(f"**{info['match']}**\n{info['segno']} (@{info['quota']:.2f})")
            somma_quote += info['quota']
        
        st.metric("SOMMA QUOTE TOTALE", f"{somma_quote:.2f}")
        
        contatore = len(st.session_state.schedina)
        st.write(f"Partite: {contatore}/10")
        
        if st.button("🚀 SALVA GIOCATA", disabled=(contatore < 10), use_container_width=True, type="primary"):
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
                st.success("✅ Salvata!")
                st.session_state.schedina = {}
                st.rerun()
            except Exception as e:
                st.error(f"Errore: {e}")
