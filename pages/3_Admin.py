import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Admin - Caricamento Totale", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("⚙️ Caricamento Completo Giornata")

bulk_text = st.text_area("Incolla qui il blocco (10 quote per riga)", height=300, 
                         placeholder="Lazio - Genoa;1,95;3,2;4,25;1,21;1,83;1,34;1,48;2,45;2,2;1,6")

giornata = st.number_input("Numero Giornata", min_value=1, value=23)

if st.button("SALVA TUTTE LE QUOTE"):
    if bulk_text:
        righe = bulk_text.strip().split('\n')
        partite_da_salvare = []
        
        try:
            for riga in righe:
                if not riga.strip(): continue
                parti = riga.split(';')
                
                # Funzione per pulire i numeri (gestisce virgola e punto)
                def cf(val): return float(val.replace(',', '.'))

                dati = {
                    "giornata": giornata,
                    "match": parti[0].strip(),
                    "quote_1": cf(parti[1]),
                    "quote_x": cf(parti[2]),
                    "quote_2": cf(parti[3]),
                    "quote_1x": cf(parti[4]),
                    "quote_x2": cf(parti[5]),
                    "quote_12": cf(parti[6]),
                    "quote_u25": cf(parti[7]),
                    "quote_o25": cf(parti[8]),
                    "quote_g": cf(parti[9]),
                    "quote_ng": cf(parti[10]),
                    "risultato_finale": "-"
                }
                partite_da_salvare.append(dati)
            
            if partite_da_salvare:
                supabase.table("partite").insert(partite_da_salvare).execute()
                st.success(f"✅ Ottimo! Caricate {len(partite_da_salvare)} partite con 10 quote ciascuna.")
                st.balloons()
        except Exception as e:
            st.error(f"Errore nel formato: {e}. Controlla i punti e virgola!")
