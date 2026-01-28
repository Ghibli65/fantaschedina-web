import streamlit as st

st.title("Pannello Amministratore")
st.write("Se vedi questo, il menu funziona correttamente!")

# Proviamo a caricare i segreti qui per vedere se danno errore
try:
    url = st.secrets["SUPABASE_URL"]
    st.success(f"Connesso a: {url}")
except Exception as e:
    st.error(f"Errore segreti: {e}")
