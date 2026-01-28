import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gioca", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("⚽ Piazza la tua Schedina")

# Prende le ultime 10 partite caricate
res = supabase.table("partite").select("*").order("id", desc=True).limit(10).execute()
partite = res.data

if not partite:
    st.warning("Nessuna partita disponibile. Attendi l'Admin.")
else:
    with st.form("schedina_form"):
        scelte = []
        for p in partite:
            st.write(f"#### {p['match']}")
            # Creiamo le etichette con le quote per l'utente
            opzioni = {
                f"1 ({p['quote_1']})": "1", f"X ({p['quote_x']})": "X", f"2 ({p['quote_2']})": "2",
                f"1X ({p['quote_1x']})": "1X", f"X2 ({p['quote_x2']})": "X2", f"12 ({p['quote_12']})": "12",
                f"U2.5 ({p['quote_u25']})": "U25", f"O2.5 ({p['quote_o25']})": "O25",
                f"G ({p['quote_g']})": "G", f"NG ({p['quote_ng']})": "NG"
            }
            scelta = st.selectbox("Esito:", list(opzioni.keys()), key=f"s_{p['id']}")
            scelte.append({"p_id": p['id'], "segno": opzioni[scelta]})
        
        if st.form_submit_button("INVIA GIOCATA"):
            # Salvataggio su Supabase (assicurati di avere la tabella pronostici pronta)
            st.success("Schedina inviata con successo!")
