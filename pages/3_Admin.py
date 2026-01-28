import streamlit as st

st.set_page_config(page_title="Admin")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("⛔ Effettua il login in Home.")
    st.stop()

if "admin_ok" not in st.session_state:
    pwd = st.text_input("Password Admin", type="password")
    if st.button("Sblocca"):
        if pwd == "fanta":
            st.session_state.admin_ok = True
            st.rerun()
        else: st.error("Errata")
    st.stop()

st.title("⚙️ Pannello Admin")
bulk = st.text_area("Incolla partite (Match;1;X;2;1X;X2;12;U2.5;O2.5;G;NG)", height=200)

if st.button("CARICA DATI"):
    lines = bulk.strip().split("\n")
    for l in lines:
        parts = l.split(";")
        st.session_state.supabase.table("partite").insert({
            "match": parts[0], "quote_1": float(parts[1]), "quote_x": float(parts[2]),
            "quote_2": float(parts[3]), "quote_1x": float(parts[4]), "quote_x2": float(parts[5]),
            "giornata": 1
        }).execute()
    st.success("Caricate!")
