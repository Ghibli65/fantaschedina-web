import streamlit as st
import pandas as pd

st.set_page_config(page_title="Compila Schedina", layout="wide")

# CSS per eliminare barre di scorrimento e stilizzare il carrello
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataFrame { width: 100% !important; }
    .cart-container {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #d1d5db;
    }
    .total-display {
        font-size: 24px;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        padding: 10px;
        background: white;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.error("Effettua il login per accedere.")
    st.stop()

# Gestione Stato Carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ La tua Schedina Interattiva")

# Layout: Carrello a sinistra (1/4) e Tabella a destra (3/4)
col_cart, col_table = st.columns([1, 3])

try:
    # Recupero partite pubblicate [cite: 2026-01-29]
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("id").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        with col_table:
            st.subheader("📊 Palinsesto Quote")
            st.info("💡 Clicca su una quota per aggiungerla al carrello.")
            
            # Tabella interattiva [cite: 2026-01-28, 2026-01-29]
            # Usiamo 'single-cell' (con trattino) per compatibilità
            selection = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-cell",
                column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
                column_config={"match": st.column_config.TextColumn("PARTITA", width=200)}
            )

            # Elaborazione selezione [cite: 2026-01-28, 2026-01-29]
            if selection.selection.get("cells"):
                row_idx = selection.selection["cells"][0]["row"]
                col_idx = selection.selection["cells"][0]["column"]
                col_name = df.columns[col_idx]
                
                # Se la colonna cliccata è una quota [cite: 2026-01-28]
                if col_name.startswith("quote_"):
                    partita = df.iloc[row_idx]
                    label_esito = col_name.replace("quote_", "").upper().replace("U25", "U").replace("O25", "O")
                    st.session_state.carrello[partita["id"]] = {
                        "match": partita["match"],
                        "esito": label_esito,
                        "quota": float(partita[col_name])
                    }

        with col_cart:
            st.markdown('<div class="cart-container">', unsafe_allow_html=True)
            st.subheader("🛒 Carrello")
            
            if not st.session_state.carrello:
                st.write("Seleziona una quota dalla tabella.")
            else:
                quota_somma = 0.0
                # Ordine per ID partita (stesso del pannello) [cite: 2026-01-28]
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"**{item['match']}**\n{item['esito']} @ {item['quota']}")
                    if c2.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                    quota_somma += item['quota'] # Somma quote richiesta [cite: 2026-01-28]
                
                st.markdown(f'<div class="total-display">TOTALE: {quota_somma:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("📤 INVIA SCHEDINA", type="primary", use_container_width=True):
                    # Logica per salvare su Supabase (da implementare) [cite: 2026-01-29]
                    st.success("✅ Schedina inviata!")
                    st.balloons()
                    st.session_state.carrello = {} # Svuota dopo invio
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Nessun palinsesto disponibile.")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
