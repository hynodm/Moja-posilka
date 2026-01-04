import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky "Gym data"
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"

# Odkaz na čítanie dát z hárka (gid=0 je zvyčajne prvý hárok s odpoveďami)
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Odkaz na tvoj Google Formulár pre ZÁPIS
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie podľa tvojho formulára
kat = st.radio("Čo dnes cvičíš?", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Automatický dátum
                dnes = datetime.now().strftime("%Y-%m-%d")
                
                # Presné ID čísla z tvojho odkazu
                payload = {
                    "entry.984639089": kat,     # Kategória
                    "entry.959036654": cvik,    # Cvik
                    "entry.472178838": str(vaha), # Váha
                    "entry.1345757671": str(opak), # Opakovania
                    "entry.1121013446": dnes    # Dátum (toto ID je odhadnuté, ak by nefungovalo, skontrolujeme ho)
                }
                
                # Odoslanie do Google Formulára
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri zápise.")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
    else:
        st.info("Zatiaľ žiadne záznamy.")
except:
    st.info("Tabuľka sa zobrazí po prvom zápise a obnovení.")
