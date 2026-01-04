import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Gym Progres", layout="centered")

# Tvoja URL adresa z Apps Scriptu
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx-y_HEPOihM7d9ifoHk6K3ybAXbmJSjTTrxRBphpPXZtLcedYXi6zo2J0yRRbjHtBv/exec"

# ID tvojej tabuľky pre čítanie histórie
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Príprava dát pre Apps Script
                data = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                # Odoslanie dát priamo do tabuľky
                response = requests.post(WEB_APP_URL, data=json.dumps(data))
                
                if response.status_code == 200:
                    st.success("✅ ÚSPEŠNE ZAPÍSANÉ PRIAMO DO TABUĽKY!")
                    st.balloons()
                else:
                    st.error("Chyba: Skript vrátil chybu. Skontroluj nastavenie 'Anyone'.")
            except Exception as e:
                st.error(f"Chyba pri komunikácii: {e}")
        else:
            st.warning("Najprv napíš názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    # Načítanie dát z tabuľky pre zobrazenie v aplikácii
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobrazenie posledných 15 záznamov, najnovšie navrchu
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka je zatiaľ prázdna.")
except:
    st.info("História sa načíta po prvom úspešnom zápise.")
