import streamlit as st

# Configurazione minima
st.set_page_config(page_title="Sblocco FantaSchedina", layout="wide")

# Rimuoviamo ogni riga di CSS o HTML che può dare errore
st.title("SISTEMA RIPRISTINATO ✅")
st.write("Se vedi questa scritta, l'app si è sbloccata.")

with st.sidebar:
    st.header("Menu Tecnico")
    if st.button("VAI AL GIOCO"):
        st.switch_page("pages/1_Gioca.py")

st.info("Dopo che vedi questa pagina, potrai rimettere il codice di ieri.")
