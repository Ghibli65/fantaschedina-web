import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per il Carrello a sinistra e bottoni quote
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .cart-container {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    .total-display {
        font-size: 22px;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        padding: 12px;
        background: #ebf2ff;
        border-radius: 8px;
        margin-top: 15px;
    }
    /* Stile per i bottoni delle quote */
    .stButton > button {
        width: 100%;
        padding: 5px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("⚠️ Effettua il login dalla Home.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

col_cart, col_table = st.columns([1, 3])

try:
    # Carichiamo i dati
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        with col_table:
            st.subheader("📊 Palinsesto")
            
            # Intestazione Tabella Manuale per massima stabilità
            header = st.columns([2, 1, 1, 1, 1, 1, 1])
            header[0].write("**PARTITA**")
            header[1].write("**1**")
            header[2].write("**X**")
            header[3].write("**2**")
            header[4].write("**U**")
            header[5].write("**O**")
            header[6].write("**G**")
            st.divider()

            for p in partite:
                r = st.columns([2, 1, 1, 1, 1, 1, 1])
                r[0].write(f"**{p['match']}**")
                
                # Bottoni per ogni quota
                for i, quota_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    label = str(p[quota_key])
                    tipo = quota_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    if r[i+1].button(label, key=f"btn_{p['id']}_{quota_key}"):
                        st.session_state.carrello[p['id']] = {
                            "match": p['match'],
                            "esito": tipo,
                            "quota": float(p[quota_key])
                        }
                        st.rerun()

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.subheader("🛒 Carrello")
            
            if not st.session_state.carrello:
                st.write("Clicca su una quota per iniziare.")
            else:
                somma_quote = 0.0
                # Ordine per ID partita
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"**{item['match']}**")
                    
                    c1, c2 = st.columns([4, 1])
                    c1.caption(f"{item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    
                    somma_quote += item['quota']
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
                    st.success("✅ Schedina salvata!")
                    st.session_state.carrello = {}
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nessuna partita disponibile.")

except Exception as e:
    st.error(f"Errore: {e}")
