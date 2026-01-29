import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per Carrello Fisso e selezione colorata
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    
    /* BLOCCA IL CARRELLO IN ALTO */
    [data-testid="stVerticalBlock"] > div:first-child > [data-testid="stVerticalBlock"] {
        position: sticky;
        top: 2rem;
        z-index: 999;
    }

    /* Contenitore carrello con altezza controllata e scroll interno */
    .cart-container {
        background-color: #f8fafc;
        padding: 12px;
        border-radius: 10px;
        border: 2px solid #1e3c72;
        max-height: 80vh; /* 80% dell'altezza dello schermo */
        overflow-y: auto;
        font-size: 13px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Stile bottoni selezionati (GIALLO) */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        border: 1px solid #ffa000 !important;
        font-weight: bold !important;
    }

    .cart-item {
        border-bottom: 1px solid #e2e8f0;
        padding: 8px 0;
        margin-bottom: 5px;
    }

    .total-display {
        background: #1e3c72;
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("⚠️ Effettua il login dalla Home.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

# Layout proporzionato
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
                
                # Bottoni quote con cambio colore
                for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    val = p[q_key]
                    tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    is_selected = (p['id'] in st.session_state.carrello and 
                                   st.session_state.carrello[p['id']]['esito'] == tipo)
                    
                    btn_type = "primary" if is_selected else "secondary"
                    
                    if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type=btn_type):
                        st.session_state.carrello[p['id']] = {
                            "match": p['match'], "esito": tipo, "quota": float(val)
                        }
                        st.rerun()

        with col_cart:
            # Il carrello ora sta dentro un contenitore con scroll interno
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.markdown("### 🛒 La tua Schedina")
            
            if not st.session_state.carrello:
                st.caption("Seleziona le quote per iniziare.")
            else:
                somma_quote = 0.0
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"<div class='cart-item'><b>{item['match']}</b><br>{item['esito']} @ {item['quota']}</div>", unsafe_allow_html=True)
                    somma_quote += item['quota']
                    
                    if st.button("🗑️ Rimuovi", key=f"del_{p_id}", use_container_width=True):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA", type="primary", use_container_width=True):
                    st.success("Schedina Inviata!")
                    st.session_state.carrello = {}
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Nessun palinsesto live.")

except Exception as e:
    st.error(f"Errore: {e}")
