import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per mantenere il Carrello a sinistra e pulire la tabella
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataFrame { width: 100% !important; }
    .cart-container {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        min-height: 200px;
    }
    .total-display {
        font-size: 20px;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        padding: 10px;
        background: #ebf2ff;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Verifica Sessione
if "user" not in st.session_state:
    st.warning("⚠️ Effettua il login dalla Home per giocare.")
    st.stop()

# 2. Inizializzazione Carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

# 3. Layout: Carrello (Sinistra) e Palinsesto (Destra)
col_cart, col_table = st.columns([1, 3])

try:
    # Recupero partite dal DB
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        with col_table:
            st.info("💡 Clicca su una quota numerica per aggiungerla alla schedina.")
            
            # Tabella Interattiva - Nota: 'single-cell' con il trattino
            selection = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-cell",
                column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
                column_config={"match": st.column_config.TextColumn("PARTITA", width=200)}
            )

            # --- LOGICA DI SELEZIONE ROBUSTA ---
            if selection.selection.get("cells"):
                cell = selection.selection["cells"][0]
                
                # Gestiamo sia il formato dizionario {'row': 0, 'column': 1} che tupla (0, 1)
                try:
                    if isinstance(cell, dict):
                        r_idx = cell.get("row")
                        c_idx = cell.get("column")
                    else:
                        r_idx = cell[0]
                        c_idx = cell[1]
                    
                    if r_idx is not None and c_idx is not None:
                        col_name = df.columns[c_idx]
                        
                        # Verifichiamo che la colonna sia effettivamente una quota
                        if col_name.startswith("quote_"):
                            partita = df.iloc[r_idx]
                            label = col_name.replace("quote_", "").upper()
                            
                            # Aggiorniamo il carrello (la chiave è l'ID partita per evitare duplicati della stessa partita)
                            st.session_state.carrello[partita["id"]] = {
                                "match": partita["match"],
                                "esito": label,
                                "quota": float(partita[col_name])
                            }
                except Exception as e:
                    # Silenziamo errori di indice durante il passaggio di stato
                    pass

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.subheader("🛒 Carrello")
            
            if not st.session_state.carrello:
                st.write("Nessuna quota selezionata. Clicca sulla tabella.")
            else:
                somma_quote = 0.0
                # Ordiniamo per mantenere l'ordine della tabella (per ID)
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"**{item['match']}**")
                    
                    c1, c2 = st.columns([3, 1])
                    c1.caption(f"{item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    
                    somma_quote += item['quota']
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA SCHEDINA", type="primary", use_container_width=True):
                    # Qui andrà la logica per salvare la giocata nel database
                    st.success("✅ Schedina registrata!")
                    st.balloons()
                    st.session_state.carrello = {} # Reset carrello
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Nessun palinsesto disponibile al momento.")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
