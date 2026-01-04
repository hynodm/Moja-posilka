import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky a odkazy
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
# Čítanie dát z prvého hárka
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
# Odkaz na tvoj formulár pre zápis
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie (presne podľa tvojich možností vo formulári)
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Prepojenie na tvoj formulár cez získané ID kódy
                payload = {
                    "entry.984639089": kat,         # Kategória
                    "entry.959036654": cvik,        # Cvik
                    "entry.472178838": str(vaha),   # Váha
                    "entry.1345757671": str(opak)   # Opakovania
                }
                
                # Odoslanie dát
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri odosielaní do tabuľky.")
        else:
            st.warning("Prosím, napíš názov cviku.")

st.divider()
st.subheader("📊 História tréningov")

try:
    # Načítanie a zobrazenie histórie
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobraziť posledných 10 riadkov, najnovšie hore
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
except:
    st.info("História sa načíta po prvom úspešnom zápise.")
