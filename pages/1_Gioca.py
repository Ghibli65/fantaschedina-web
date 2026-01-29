import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per pulire la tabella e colorare i tasti selezionati
st.markdown("""
    <style>
    /* Colore Giallo per i tasti cliccati */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        border: none !important;
        font-weight: bold !important;
    }
    /* Rimpiccioliamo i tasti del palinsesto per farli stare in riga */
    .stButton > button {
        padding: 2px 5px !important;
        height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Effettua il login per giocare.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# --- PARTE 1: IL CARRELLO NELLA ZONA GRIGIA (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🛒 La tua Schedina")
    st.divider()
    
    if not st.session_state.carrello:
        st.info("Seleziona le quote dal palinsesto per comporre la schedina.")
    else:
        somma_quote = 0.0
        # Mostriamo ogni partita selezionata nel menu grigio
        for p_id in sorted(st.session_state.carrello.keys()):
            item = st.session_state.carrello[p_id]
            with st.container():
                st.markdown(f"**{item['match']}**")
                c1, c2 = st.columns([3, 1])
                c1.caption(f"{item['esito']} @ {item['quota']}")
                if c2.button("🗑️", key=f"side_del_{p_id}"):
                    del st.session_state.carrello[p_id]
                    st.rerun()
                somma_quote += item['quota']
            st.divider()
        
        # Totale e tasto invio in fondo al menu grigio
        st.markdown(f"### TOTALE: {somma_quote:.2f}")
        if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
            st.success("Schedina registrata!")
            st.session_state.carrello = {}
            st.rerun()

# --- PARTE 2: IL PALINSESTO NELLA ZONA BIANCA ---
st.title("⚽ Compila la tua Schedina")

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        st.subheader("📊 Palinsesto Giornata")
        # Header Tabella
        h = st.columns([2.5, 1, 1, 1, 1, 1, 1])
        cols_labels = ["MATCH", "1", "X", "2", "U", "O", "G"]
        for i, label in enumerate(cols_labels):
            h[i].markdown(f"**{label}**")
        st.divider()

        # Righe Partite
        for p in partite:
            r = st.columns([2.5, 1, 1, 1, 1, 1, 1])
            r[0].write(f"**{p['match']}**")
            
            # Generazione tasti quote
            for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                val = p[q_key]
                tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                
                # Controllo se è selezionato per cambiare colore in GIALLO
                is_sel = (p['id'] in st.session_state.carrello and 
                           st.session_state.carrello[p['id']]['esito'] == tipo)
                
                if r[i+1].button(str(val), key=f"main_q_{p['id']}_{q_key}", 
                                 type="primary" if is_sel else "secondary"):
                    st.session_state.carrello[p['id']] = {
                        "match": p['match'], "esito": tipo, "quota": float(val)
                    }
                    st.rerun()
    else:
        st.info("In attesa di pubblicazione del palinsesto.")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
