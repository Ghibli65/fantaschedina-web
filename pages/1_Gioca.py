import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per il Carrello e pulizia visiva
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataFrame { width: 100% !important; }
    .cart-container {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
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
    </style>
    """, unsafe_allow_html=True)

# Controllo Login
if "user" not in st.session_state:
    st.warning("⚠️ Per favore, effettua il login dalla Home per giocare.")
    st.stop()

# Inizializzazione Carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Schedina Interattiva")

col_cart, col_table = st.columns([1, 3])

try:
    # Caricamento partite
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        with col_table:
            st.info("💡 Clicca su una quota per aggiungerla alla schedina.")
            
            # Tabella Interattiva
            selection = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-cell",
                column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
                column_config={"match": st.column_config.TextColumn("PARTITA", width=200)}
            )

            # --- GESTIONE SELEZIONE SENZA ERRORI ---
            selected_cells = selection.selection.get("cells", [])
            if selected_cells:
                cell = selected_cells[0]
                
                # Supporto per entrambi i formati (Dizionario o Tupla)
                try:
                    if isinstance(cell, dict):
                        r_idx, c_idx = cell["row"], cell["column"]
                    else:
                        r_idx, c_idx = cell[0], cell[1]
                    
                    col_name = df.columns[c_idx]
                    
                    # Se clicchi su una quota
                    if col_name.startswith("quote_"):
                        partita = df.iloc[r_idx]
                        label = col_name.replace("quote_", "").upper()
                        
                        # Aggiorna il carrello
                        st.session_state.carrello[partita["id"]] = {
                            "match": partita["match"],
                            "esito": label,
                            "quota": float(partita[col_name])
                        }
                except Exception:
                    pass # Evita crash se il formato cambia durante il clic

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.subheader("🛒 Carrello")
            
            if not st.session_state.carrello:
                st.write("Nessuna quota selezionata.")
            else:
                somma_quote = 0.0
                # Ordine fisso per squadra
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.write(f"**{item['match']}**")
                    
                    c1, c2 = st.columns([3, 1])
                    c1.caption(f"{item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    
                    somma_quote += item['quota'] # Somma aritmetica
                
                st.markdown(f'<div class="total-display">SOMMA: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("🚀 INVIA", type="primary", use_container_width=True):
                    st.success("Schedina salvata!")
                    st.session_state.carrello = {} # Reset
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Nessun palinsesto Live.")
except Exception as e:
    st.error(f"Errore caricamento: {e}")
