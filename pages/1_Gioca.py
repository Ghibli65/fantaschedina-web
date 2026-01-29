import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS AGGRESSIVO PER BLOCCARE IL CARRELLO
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Forza la colonna del carrello a non allungarsi */
    [data-testid="column"] {
        height: fit-content !important;
    }

    /* Crea il box del carrello fisso e piccolo */
    .sticky-cart {
        position: fixed;
        top: 80px;
        width: 20%; /* Larghezza fissa proporzionale */
        max-height: 450px; /* Altezza massima bloccata */
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #1e3c72;
        overflow-y: auto; /* Scroll interno se ci sono troppe partite */
        z-index: 1000;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
    }

    /* Colore Giallo per la quota selezionata */
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        border: 1px solid #ffa000 !important;
        font-weight: bold !important;
    }

    .total-box {
        background: #1e3c72;
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    .item-bet {
        font-size: 12px;
        border-bottom: 1px solid #ddd;
        padding: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.stop()

if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina")

# Usiamo le colonne ma il carrello sarà "fixed" tramite CSS
col_spacer, col_table = st.columns([0.8, 3.2])

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    partite = res.data

    if partite:
        # --- COLONNA DESTRA: PALINSESTO ---
        with col_table:
            st.subheader("📊 Seleziona Quote")
            h = st.columns([2, 1, 1, 1, 1, 1, 1])
            labels = ["**MATCH**", "**1**", "**X**", "**2**", "**U**", "**O**", "**G**"]
            for i, l in enumerate(labels): h[i].write(l)
            st.divider()

            for p in partite:
                r = st.columns([2, 1, 1, 1, 1, 1, 1])
                r[0].write(f"**{p['match']}**")
                
                for i, q_key in enumerate(['quote_1', 'quote_x', 'quote_2', 'quote_u25', 'quote_o25', 'quote_g']):
                    val = p[q_key]
                    tipo = q_key.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    
                    # Controllo selezione per colore giallo [cite: 2026-01-29]
                    is_sel = (p['id'] in st.session_state.carrello and st.session_state.carrello[p['id']]['esito'] == tipo)
                    
                    if r[i+1].button(str(val), key=f"q_{p['id']}_{q_key}", type="primary" if is_sel else "secondary"):
                        st.session_state.carrello[p['id']] = {"match": p['match'], "esito": tipo, "quota": float(val)}
                        st.rerun()

        # --- COLONNA SINISTRA: IL CARRELLO FISSO ---
        with col_spacer:
            # Creiamo il contenitore HTML fisso
            cart_html = ""
            somma_quote = 0.0
            
            for p_id in sorted(st.session_state.carrello.keys()):
                item = st.session_state.carrello[p_id]
                cart_html += f"<div class='item-bet'><b>{item['match']}</b><br>{item['esito']} @ {item['quota']}</div>"
                somma_quote += item['quota']

            # Inseriamo tutto dentro il div "sticky-cart" [cite: 2026-01-29]
            st.markdown(f"""
                <div class="sticky-cart">
                    <h3 style='margin-top:0'>🛒 Schedina</h3>
                    {cart_html if cart_html else "<p>Vuoto</p>"}
                    <div class="total-box">SOMMA: {somma_quote:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # I bottoni di azione devono essere fuori dal div HTML per funzionare in Streamlit
            if st.session_state.carrello:
                if st.button("🗑️ SVUOTA", use_container_width=True):
                    st.session_state.carrello = {}
                    st.rerun()
                if st.button("🚀 INVIA", type="primary", use_container_width=True):
                    st.success("Inviata!")
                    st.session_state.carrello = {}
                    st.rerun()

except Exception as e:
    st.error(f"Errore: {e}")
