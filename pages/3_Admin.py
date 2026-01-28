import streamlit as st

st.set_page_config(page_title="Pannello Admin", layout="wide")

# LOGIN ADMIN INDIPENDENTE
if "admin_logged_in" not in st.session_state:
    st.title("🔐 Accesso Amministratore")
    with st.form("admin_login"):
        user_admin = st.text_input("Utente Admin")
        pass_admin = st.text_input("Password Admin", type="password")
        if st.form_submit_button("ENTRA NEL PANNELLO"):
            if user_admin == "Admin" and pass_admin == "fanta":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenziali Amministratore errate!")
    st.stop()

# --- SE IL LOGIN È OK, MOSTRA IL PANNELLO ---
st.title("⚙️ Gestione Partite e Quote")
if st.button("Esci dall'area Admin"):
    del st.session_state.admin_logged_in
    st.rerun()

st.divider()

# Area caricamento massivo
bulk_text = st.text_area(
    "Incolla qui: Match;1;X;2;1X;X2;12;U2.5;O2.5;G;NG", 
    placeholder="Inter-Milan;1.85;3.40;4.10;1.20;1.90;1.30;1.80;2.00;1.70;2.05",
    height=250
)

giornata = st.number_input("Giornata n.", min_value=1, value=1, step=1)

if st.button("🚀 CARICA E AGGIORNA DB", type="primary"):
    if bulk_text:
        try:
            supabase = st.session_state.supabase
            righe = bulk_text.strip().split('\n')
            
            for riga in righe:
                p = riga.split(';')
                def q(val): return float(val.replace(',', '.'))
                
                supabase.table("partite").insert({
                    "match": p[0].strip(),
                    "quote_1": q(p[1]), "quote_x": q(p[2]), "quote_2": q(p[3]),
                    "quote_1x": q(p[4]), "quote_x2": q(p[5]), "quote_12": q(p[6]),
                    "quote_u25": q(p[7]), "quote_o25": q(p[8]), "quote_g": q(p[9]),
                    "quote_ng": q(p[10]),
                    "giornata": giornata
                }).execute()
            st.success(f"Caricate {len(righe)} partite con successo!")
        except Exception as e:
            st.error(f"Errore: {e}. Controlla i separatori (;)")
    else:
        st.warning("L'area di testo è vuota.")
