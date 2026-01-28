import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Admin", layout="wide")

# 1. PROTEZIONE ACCESSO
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⛔ Effettua prima il login nella Home Page.")
    st.stop()

# 2. PASSWORD ADMIN (Cambiala qui sotto!)
ADMIN_PASSWORD = "fanta" 

if "admin_ok" not in st.session_state:
    st.subheader("Pannello Riservato")
    pwd = st.text_input("Inserisci Password Admin", type="password")
    if st.button("Entra"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_ok = True
            st.rerun()
        else:
            st.error("Sbagliata!")
    st.stop()

# 3. SEZIONE CARICAMENTO (Se la password è corretta)
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
st.title("⚙️ Caricamento Rapido Giornata")

bulk_text = st.text_area("Incolla qui il blocco (Match;1;X;2;1X;X2;12;U;O;G;NG)", height=200)
giornata = st.number_input("Numero Giornata", min_value=1, value=23)

if st.button("SALVA TUTTO"):
    if bulk_text:
        righe = bulk_text.strip().split('\n')
        partite_db = []
        try:
            for riga in righe:
                p = riga.split(';')
                def cf(v): return float(v.replace(',', '.'))
                partite_db.append({
                    "giornata": giornata, "match": p[0].strip(),
                    "quote_1": cf(p[1]), "quote_x": cf(p[2]), "quote_2": cf(p[3]),
                    "quote_1x": cf(p[4]), "quote_x2": cf(p[5]), "quote_12": cf(p[6]),
                    "quote_u25": cf(p[7]), "quote_o25": cf(p[8]), "quote_g": cf(p[9]), "quote_ng": cf(p[10]),
                    "risultato_finale": "-"
                })
            supabase.table("partite").insert(partite_db).execute()
            st.success("✅ Partite caricate!")
        except Exception as e:
            st.error(f"Errore: {e}")
