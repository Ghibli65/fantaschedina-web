import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS Avanzato per Carrello ad altezza fissa e Colori Selezione
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Carrello con altezza fissa e scroll interno */
    .cart-container {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #1e3c72;
        max-height: 550px; /* Altezza media di 10 righe di partite */
        overflow-y: auto;  /* Appare la barra solo nel carrello se serve */
        font-size: 13px;
    }
    
    /* Evidenziazione quota selezionata */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important; /* Giallo Oro per la scelta */
        color: black !important;
        border: 1px solid #ffa000 !important;
        font-weight: bold !important;
    }

    .cart-item {
        border-bottom: 1px solid #ddd;
        padding: 5px 0;
    }

    .total-display {
        position: sticky;
        bottom: 0;
        background: #1e3c72;
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("⚠️ Effettua il login dalla Home.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

# Layout: Carrello compatto e Palinsesto largo
col_cart, col_table = st.columns([0.8, 3.2])

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        with col_table:
            st.subheader("📊 Palinsesto Quote")
            h = st.columns([2, 1, 1, 1, 1, 1, 1])
            cols_labels = ["**PARTITA**", "**1**", "**X**", "**2**", "**U**", "**O**", "**G**"]
            for i, label in enumerate(cols_labels): h[i].write(label)
            st.divider()

            for p in partite:
                r = st.columns([2, 1, 1, 1, 1, 1, 1])
                r[0].write(f"**{p['match']}**")
                
                # Generazione bottoni quote
                for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    val = p[q_key]
                    tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    # Controllo se questa quota è quella selezionata nel carrello [cite: 2026-01-29]
                    is_selected = False
                    if p['id'] in st.session_state.carrello:
                        if st.session_state.carrello[p['id']]['esito'] == tipo:
                            is_selected = True
                    
                    # Se selezionata, usa lo stile 'primary' (colore giallo impostato nel CSS) [cite: 2026-01-29]
                    btn_type = "primary" if is_selected else "secondary"
                    
                    if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type=btn_type):
                        st.session_state.carrello[p['id']] = {
                            "match": p['match'], "esito": tipo, "quota": float(val)
                        }
                        st.rerun()

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.markdown("### 🛒 Schedina")
            
            if not st.session_state.carrello:
                st.caption("Seleziona le quote...")
            else:
                somma_quote = 0.0
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"<div class='cart-item'><b>{item['match']}</b><br>{item['esito']} @ {item['quota']}</div>", unsafe_allow_html=True)
                    somma_quote += item['quota']
                    
                    if st.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA", type="primary", use_container_width=True, key="send_bet"):
                    # Logica di salvataggio (verrà aggiunta nel prossimo step) [cite: 2026-01-29]
                    st.success("Inviata!")
                    st.session_state.carrello = {}
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nessun palinsesto live.")

except Exception as e:
    st.error(f"Errore: {e}")
