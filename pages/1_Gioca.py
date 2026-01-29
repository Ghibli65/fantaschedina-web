import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS DEFINITIVO: Blocca il carrello senza coprire le squadre
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Contenitore Carrello: Fisso a sinistra ma non sovrapposto */
    .sticky-wrapper {
        position: sticky;
        top: 20px;
        height: fit-content;
    }

    .cart-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #1e3c72;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-height: 500px; /* Altezza bloccata per 10 partite */
        overflow-y: auto;  /* Scroll solo se necessario */
    }

    /* Stile bottoni selezionati (GIALLO come in foto) */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    .total-footer {
        background: #1e3c72;
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
    }

    .item-row {
        font-size: 13px;
        border-bottom: 1px solid #eee;
        padding: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Effettua il login.")
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Compila la tua Schedina")

# Layout: 1/4 per il carrello, 3/4 per il palinsesto
col_left, col_right = st.columns([1, 3])

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        # --- COLONNA DESTRA: PALINSESTO ---
        with col_right:
            st.subheader("📊 Seleziona le Quote")
            # Header tabella
            h = st.columns([2, 1, 1, 1, 1, 1, 1])
            cols = ["MATCH", "1", "X", "2", "U", "O", "G"]
            for i, txt in enumerate(cols): h[i].markdown(f"**{txt}**")
            st.divider()

            for p in partite:
                r = st.columns([2, 1, 1, 1, 1, 1, 1])
                r[0].write(f"**{p['match']}**")
                
                for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    val = p[q_key]
                    tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    # Controllo se selezionato per colore giallo
                    is_sel = (p['id'] in st.session_state.carrello and 
                               st.session_state.carrello[p['id']]['esito'] == tipo)
                    
                    if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", 
                                     type="primary" if is_sel else "secondary"):
                        st.session_state.carrello[p['id']] = {
                            "match": p['match'], "esito": tipo, "quota": float(val)
                        }
                        st.rerun()

        # --- COLONNA SINISTRA: CARRELLO ---
        with col_left:
            st.markdown('<div class="sticky-wrapper">', unsafe_allow_html=True)
            st.markdown('<div class="cart-box">', unsafe_allow_html=True)
            st.markdown("### 🛒 Schedina")
            
            if not st.session_state.carrello:
                st.write("Nessuna selezione")
            else:
                somma = 0.0
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"""
                        <div class="item-row">
                            <b>{item['match']}</b><br>
                            {item['esito']} @ {item['quota']}
                        </div>
                    """, unsafe_allow_html=True)
                    somma += item['quota']
                    
                    if st.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                
                st.markdown(f'<div class="total-footer">SOMMA: {somma:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA GIOCATA", type="primary", use_container_width=True):
                    # Qui aggiungeremo il salvataggio su Supabase
                    st.success("Giocata inviata!")
                    st.session_state.carrello = {}
                    st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Errore: {e}")
