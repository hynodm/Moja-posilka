
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky pre čítanie (vďaka exportu 404 zmizne)
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Odkaz na tvoj Google Formulár pre ZÁPIS
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdR2AkDaoNk9Z0OCdglFkwrQJMGOjNF9PAc5IncDW0HEyarJw/formResponse"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                dnes = datetime.now().strftime("%d.%m.%Y")
                # Toto sú ID tvojich polí vo formulári (automaticky namapované)
                payload = {
                    "entry.1481534065": dnes,
                    "entry.1051515234": kat,
                    "entry.1415151515": cvik,
                    "entry.1815151515": str(vaha),
                    "entry.1915151515": str(opak)
                }
                # Odoslanie dát cez formulár (obchádza Service Account chybu)
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri odosielaní dát.")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História")
try:
    df = pd.read_csv(READ_URL)
    st.dataframe(df.tail(10), use_container_width=True)
except:
    st.info("Tabuľka je zatiaľ prázdna.")
