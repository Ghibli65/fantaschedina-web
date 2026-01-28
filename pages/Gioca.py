import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Inserisci Pronostici")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Fai il login in Home Page per giocare!")
    st.stop()

st.title("⚽ La tua Schedina")

# Recupera l'ultima giornata inserita
res = supabase.table("partite").select("giornata").order("giornata", desc=True).limit(1).execute()
if not res.data:
    st.info("L'amministratore non ha ancora caricato le partite.")
else:
    g_corrente = res.data[0]['giornata']
    st.subheader(f"Pronostici per la Giornata {g_corrente}")
    
    partite = supabase.table("partite").select("*").eq("giornata", g_corrente).execute().data
    
    with st.form("schedina"):
        pronostici = {}
        for p in partite:
            pronostici[p['id']] = st.radio(f"{p['match']}", ["1", "X", "2"], horizontal=True)
        
        if st.form_submit_button("INVIA SCHEDINA"):
            for p_id, segno in pronostici.items():
                supabase.table("pronostici").upsert({
                    "user_id": st.session_state.user.id,
                    "partita_id": p_id,
                    "pronostico": segno,
                    "email_utente": st.session_state.user.email,
                    "giornata": g_corrente
                }).execute()
            st.success("Schedina salvata! In bocca al lupo 🍀")
