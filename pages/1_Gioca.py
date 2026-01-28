import streamlit as st

st.set_page_config(page_title="Gioca", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("⛔ Devi prima fare il login in Home!")
    st.stop()

supabase = st.session_state.supabase

st.title("⚽ La tua Schedina")

# Recupero partite
res = supabase.table("partite").select("*").order("id").execute()
partite = res.data

if not partite:
    st.warning("Nessuna partita disponibile al momento.")
else:
    if "schedina" not in st.session_state: st.session_state.schedina = {}

    col_riepilogo, col_partite = st.columns([1, 2])

    with col_partite:
        for p in partite:
            st.subheader(f"{p['match']}")
            # Griglia quote
            c = st.columns(5)
            # Lista opzioni
            ops = [("1", p['quote_1']), ("X", p['quote_x']), ("2", p['quote_2']), ("1X", p['quote_1x']), ("X2", p['quote_x2'])]
            for i, (label, q) in enumerate(ops):
                btn_type = "primary" if st.session_state.schedina.get(p['id'], {}).get('segno') == label else "secondary"
                if c[i].button(f"{label}\n{q}", key=f"{p['id']}_{label}", type=btn_type, use_container_width=True):
                    st.session_state.schedina[p['id']] = {"match": p['match'], "segno": label, "quota": float(q), "id_p": p['id']}
                    st.rerun()
            st.divider()

    with col_riepilogo:
        st.sticky = True
        st.subheader("📋 Riepilogo")
        somma = 0.0
        for pid, info in st.session_state.schedina.items():
            st.write(f"{info['match']}: **{info['segno']}** (@{info['quota']})")
            somma += info['quota']
        
        st.metric("SOMMA QUOTE", f"{somma:.2f}")
        
        if len(st.session_state.schedina) >= 10:
            if st.button("SALVA SCHEDINA", type="primary", use_container_width=True):
                # Logica inserimento DB qui
                st.success("Schedina salvata!")
        else:
            st.write(f"Seleziona ancora {10 - len(st.session_state.schedina)} partite.")
