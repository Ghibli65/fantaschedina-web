import streamlit as st

st.set_page_config(page_title="Pannello Admin")
st.title("⚙️ Area Amministratore")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Fai il login in Home Page")
    st.stop()

st.write(f"Benvenuto, {st.session_state.user.email}!")
st.info("Se vedi questa scritta, la cartella è finalmente corretta!")
