import streamlit as st
import pandas as pd

st.set_page_config(page_title="La tua Schedina", layout="wide")

# CSS per il Carrello a sinistra e pulizia visiva
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataFrame { width: 100% !important; }
    .cart-container {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        position: sticky;
        top: 20px;
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
        border: 1px solid #bfdbfe;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.error("Effettua il login per accedere.")
    st.stop()

# Inizializzazione Carrello se non esiste
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Compila la tua Schedina")

# Layout: Carrello (Sinistra) e Palinsesto (Destra)
col_cart, col_table = st.columns([1, 3])

try:
    # Recupero partite dal database
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        with col_table:
            st.subheader("📊 Palinsesto Quote")
            st.info("💡 Clicca direttamente sulla quota per aggiungerla alla schedina.")
            
            # Tabella Interattiva con selezione cella
            selection = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-cell",
                column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
                column_config={"match": st.column_config.TextColumn("PARTITA", width=220)}
            )

            # Logica corretta per estrarre i dati della cella cliccata
            if selection.selection.get("cells"):
                # Estraiamo gli indici corretti evitando l'errore 'str'
                cell = selection.selection["cells"][0]
                row_idx = cell["row"]
                col_idx = cell["column"]
                
                # Identifichiamo la colonna cliccata
                col_name = df.columns[col_idx]
                
                if col_name.startswith("quote_"):
                    partita_selezionata = df.iloc[row_idx]
                    label_esito = col_name.replace("quote_", "").upper()
                    
                    # Salviamo nel carrello (sovrascrive se la partita esiste già)
                    st.session_state.carrello[partita_selezionata["id"]] = {
                        "match": partita_selezionata["match"],
                        "esito": label_esito,
                        "quota": float(partita_selezionata[col_name])
                    }

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.subheader("🛒 Carrello")
            
            if not st.session_state.carrello:
                st.write("Seleziona una quota...")
            else:
                somma_quote = 0.0
                # Ordiniamo per mantenere la stessa sequenza del pannello
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.markdown(f"**{item['match']}**")
                    
                    c1, c2 = st.columns([3, 1])
                    c1.caption(f"Segno: {item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"remove_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    
                    somma_quote += item['quota']
                
                st.markdown(f'<div class="total-display">SOMMA QUOTE: {somma_quote:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("📤 INVIA SCHEDINA", type="primary", use_container_width=True):
                    # Qui puoi inserire la logica per salvare la schedina su Supabase
                    st.success("✅ Schedina inviata con successo!")
                    st.balloons()
                    st.session_state.carrello = {} # Reset carrello
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Nessun palinsesto disponibile.")

except Exception as e:
    st.error(f"⚠️ Errore durante il caricamento: {e}")
