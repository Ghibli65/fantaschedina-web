import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per rendere il carrello molto più compatto
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Carrello compatto */
    .cart-container {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        font-size: 13px; /* Testo più piccolo */
    }
    
    .cart-item {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }
    
    .total-display {
        font-size: 16px;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        padding: 8px;
        background: #ebf2ff;
        border-radius: 5px;
        margin-top: 10px;
    }

    /* Riduzione spazio tra i bottoni della tabella */
    .stButton > button {
        width: 100%;
        padding: 2px 5px !important;
        height: 28px !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("⚠️ Effettua il login dalla Home.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

# Layout: Colonna carrello più stretta (0.8) e tabella più larga (3.2)
col_cart, col_table = st.columns([0.8, 3.2])

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        with col_table:
            st.subheader("📊 Palinsesto")
            # Intestazione compatta
            h = st.columns([2, 1, 1, 1, 1, 1, 1])
            cols_labels = ["**PARTITA**", "**1**", "**X**", "**2**", "**U**", "**O**", "**G**"]
            for i, label in enumerate(cols_labels):
                h[i].write(label)
            st.divider()

            for p in partite:
                r = st.columns([2, 1, 1, 1, 1, 1, 1])
                r[0].write(f"<div style='font-size:14px'>{p['match']}</div>", unsafe_allow_html=True)
                
                for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    val = p[q_key]
                    tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}"):
                        st.session_state.carrello[p['id']] = {
                            "match": p['match'],
                            "esito": tipo,
                            "quota": float(val)
                        }
                        st.rerun()

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.markdown("### 🛒 Schedina")
            
            if not st.session_state.carrello:
                st.caption("Seleziona quote...")
            else:
                somma_quote = 0.0
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"<div class='cart-item'><b>{item['match']}</b>", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"{item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    
                    somma_quote += item['quota']
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA", type="primary", use_container_width=True):
                    st.success("Inviata!")
                    st.session_state.carrello = {}
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nessun palinsesto live.")

except Exception as e:
    st.error(f"Errore: {e}")
