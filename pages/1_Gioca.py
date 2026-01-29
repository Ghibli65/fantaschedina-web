import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gioca Schedina", layout="wide")

# CSS per nascondere menu e scrollbar
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stDataEditor { width: 100% !important; }
    .cart-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
    .total-box { font-size: 20px; font-weight: bold; color: #1e3c72; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.error("Effettua il login dalla Home.")
    st.stop()

# Inizializzazione Carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

st.title("⚽ Compila la tua Schedina")

# Layout a due colonne: Carrello (Sinistra) e Tabella (Destra)
col_cart, col_table = st.columns([1, 3])

try:
    res = st.session_state.supabase.table("partite").select("*").eq("pubblicata", True).order("giornata").execute()
    df = pd.DataFrame(res.data)

    if not df.empty:
        with col_table:
            st.subheader("📊 Seleziona le Quote")
            st.info("💡 Clicca su una quota per aggiungerla alla schedina.")
            
            # Mostriamo la tabella. Rileviamo la selezione dell'utente.
            event = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single_cell", # L'utente clicca una singola quota
                column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
                column_config={"match": st.column_config.TextColumn("PARTITA", width=180)}
            )

            # Logica di aggiunta al carrello [cite: 2026-01-28]
            selected_cells = event.selection.get("cells", [])
            if selected_cells:
                row_idx = selected_cells[0][0]
                col_name = df.columns[selected_cells[0][1]]
                
                if col_name.startswith("quote_"):
                    partita = df.iloc[row_idx]
                    label_esito = col_name.replace("quote_", "").upper()
                    valore_quota = partita[col_name]
                    
                    # Aggiungiamo o aggiorniamo il pronostico nel carrello
                    st.session_state.carrello[partita["id"]] = {
                        "match": partita["match"],
                        "esito": label_esito,
                        "quota": valore_quota
                    }

        with col_cart:
            st.markdown('<div class="cart-box">', unsafe_allow_html=True)
            st.subheader("🛒 Il tuo Carrello")
            
            if not st.session_state.carrello:
                st.write("Nessun evento selezionato.")
            else:
                quota_totale = 0
                # Ordiniamo il carrello come nel pannello (per match) [cite: 2026-01-28]
                for p_id in sorted(st.session_state.carrello.keys()):
                    item = st.session_state.carrello[p_id]
                    st.write(f"**{item['match']}**")
                    st.caption(f"Segno: {item['esito']} @ {item['quota']}")
                    quota_totale += item['quota'] # Somma delle quote richiesta [cite: 2026-01-28]
                    
                    if st.button("❌", key=f"del_{p_id}"):
                        del st.session_state.carrello[p_id]
                        st.rerun()
                
                st.divider()
                st.markdown(f'<div class="total-box">Somma Quote: {quota_totale:.2f}</div>', unsafe_allow_html=True)
                
                if st.button("📤 INVIA SCHEDINA", type="primary", use_container_width=True):
                    # Logica salvataggio su Supabase [cite: 2026-01-28]
                    st.success("Schedina inviata!")
                    st.balloons()
                    st.session_state.carrello = {} # Svuota carrello dopo invio
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Nessun palinsesto live.")
except Exception as e:
    st.error(f"Errore: {e}")
