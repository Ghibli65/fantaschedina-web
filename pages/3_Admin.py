import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Admin - Caricamento Rapido", layout="wide")
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("⚙️ Caricamento Rapido Giornata")

# Area di testo per incollare il blocco
st.info("Incolla qui sotto il blocco delle partite nel formato: SquadraA - SquadraB;quota1;quotaX;quota2...")
bulk_text = st.text_area("Blocco Partite e Quote", height=250, placeholder="Lazio - Genoa;1,95;3,2;4,25...")

giornata = st.number_input("Numero Giornata", min_value=1, value=23)

if st.button("ELABORA E SALVA TUTTO"):
    if bulk_text:
        righe = bulk_text.strip().split('\n')
        partite_da_salvare = []
        
        try:
            for riga in righe:
                if not riga.strip(): continue
                
                # Dividiamo la riga usando il punto e virgola
                parti = riga.split(';')
                
                # Pulizia dei dati (sostituiamo la virgola con il punto per i numeri)
                def clean_float(val):
                    return float(val.replace(',', '.'))

                # Mappatura basata sul tuo esempio:
                # 0: Match, 1: Q1, 2: QX, 3: Q2, 4: 1X (saltiamo?), 5: X2 (saltiamo?), 6: 12 (saltiamo?), 
                # 7: U2.5, 8: O2.5, 9: G, 10: NG
                dati = {
                    "giornata": giornata,
                    "match": parti[0].strip(),
                    "quote_1": clean_float(parti[1]),
                    "quote_x": clean_float(parti[2]),
                    "quote_2": clean_float(parti[3]),
                    "quote_u25": clean_float(parti[7]),
                    "quote_o25": clean_float(parti[8]),
                    "quote_g": clean_float(parti[9]),
                    "quote_ng": clean_float(parti[10]),
                    "risultato_finale": "-"
                }
                partite_da_salvare.append(dati)
            
            # Invio a Supabase
            if partite_da_salvare:
                supabase.table("partite").insert(partite_da_salvare).execute()
                st.success(f"✅ Caricate con successo {len(partite_da_salvare)} partite per la giornata {giornata}!")
                st.balloons()
                
        except Exception as e:
            st.error(f"❌ Errore nel formato dei dati: {e}")
            st.warning("Assicurati che ogni riga sia corretta e che i valori siano separati da ;")
    else:
        st.error("L'area di testo è vuota!")
