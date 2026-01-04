import streamlit as st
import pandas as pd
import requests
import json

# Nastavenie stránky
st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# --- KONFIGURÁCIA ---
# Tvoja nová URL adresa z Apps Scriptu
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzEE4TWHkEK1voMdH_wY2QUAjrix0GUZWsPQ4krZQ6szFJJap6Ij2yr0oz14tsr2hcY/exec"

# ID tvojej tabuľky
SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"
# Odkaz na čítanie dát priamo z hárka "Data"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie (prepínač)
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

# Formulár pre zápis
with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Príprava dát pre Apps Script
                payload = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                # Odoslanie dát
                response = requests.post(WEB_APP_URL, data=json.dumps(payload))
                
                if "Success" in response.text:
                    st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                    st.balloons()
                else:
                    st.error(f"Skript vrátil neočakávanú odpoveď: {response.text}")
            except Exception as e:
                st.error(f"Chyba pri komunikácii: {e}")
        else:
            st.warning("⚠️ Prosím, zadaj názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

# Zobrazenie histórie
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobrazenie posledných 15 záznamov, najnovšie sú hore
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("ℹ️ Tabuľka 'Data' je zatiaľ prázdna. Urob svoj prvý zápis!")
except Exception:
    st.info("⌛ Čakám na prvé dáta v novom hárku 'Data'...")
