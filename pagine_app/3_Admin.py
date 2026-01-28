import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Pannello Admin", layout="wide")

# 1. PROTEZIONE ACCESSO UTENTE
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⛔ Accesso negato. Effettua prima il login nella Home Page.")
    st.stop()

# 2. PASSWORD AMMINISTRATORE (Puoi cambiarla qui)
ADMIN_PASSWORD = "fanta" 

if "admin_authenticated" not in st.session_state:
    st.subheader("🔐 Area Riservata Amministratore")
    pwd = st.text_input("Inserisci la Password Admin", type="password")
    if st.button("Sblocca Pannello"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("Accesso autorizzato!")
            st.rerun()
        else:
            st.error("Password errata. Riprova.")
    st.stop()

# 3. CONFIGURAZIONE SUPABASE E INTERFACCIA
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("⚙️ Gestione Giornata e Quote")
st.write("Copia e incolla qui sotto il blocco di partite e quote separati da punto e virgola.")

# Area di testo per il caricamento massivo
bulk_text = st.text_area(
    "Formato: Match; 1; X; 2; 1X; X2; 12; U2.5; O2.5; G; NG", 
    placeholder="Inter - Milan;1.85;3.40;4.10;1.20;1.90;1.30;1.80;2.00;1.70;2.05",
    height=300
)

col1, col2 = st.columns(2)
giornata = col1.number_input("Numero della Giornata", min_value=1, value=23, step=1)

if st.button("🚀 CARICA E SALVA TUTTE LE PARTITE", use_container_width=True, type="primary"):
    if not bulk_text.strip():
        st.error("L'area di testo è vuota!")
    else:
        righe = bulk_text.strip().split('\n')
        partite_da_inserire = []
        
        try:
            for riga in righe:
                parti = riga.split(';')
                
                # Funzione interna per pulire e convertire i numeri (gestisce virgole e punti)
                def pulisci_quota(valore):
                    return float(valore.strip().replace(',', '.'))

                # Creazione dell'oggetto partita per il database
                partite_da_inserire.append({
                    "giornata": giornata,
                    "match": parti[0].strip(),
                    "quote_1": pulisci_quota(parti[1]),
                    "quote_x": pulisci_quota(parti[2]),
                    "quote_2": pulisci_quota(parti[3]),
                    "quote_1x": pulisci_quota(parti[4]),
                    "quote_x2": pulisci_quota(parti[5]),
                    "quote_12": pulisci_quota(parti[6]),
                    "quote_u25": pulisci_quota(parti[7]),
                    "quote_o25": pulisci_quota(parti[8]),
                    "quote_g": pulisci_quota(parti[9]),
                    "quote_ng": pulisci_quota(parti[10]),
                    "risultato_finale": "-" # Valore di default
                })
            
            # Inserimento massivo in Supabase
            supabase.table("partite").insert(partite_da_inserire).execute()
            st.success(f"✅ Successo! Caricate {len(partite_da_inserire)} partite per la giornata {giornata}.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Errore durante il caricamento: {e}")
            st.info("Controlla che il formato sia corretto: Match;1;X;2;1X;X2;12;U2.5;O2.5;G;NG")

st.divider()
if st.button("Esci dal Pannello Admin"):
    del st.session_state.admin_authenticated
    st.rerun()
