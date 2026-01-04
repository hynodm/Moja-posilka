import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Gym Progres", layout="centered")

# Tvoja URL adresa z Apps Scriptu
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx-y_HEPOihM7d9ifoHk6K3ybAXbmJSjTTrxRBphpPXZtLcedYXi6zo2J0yRRbjHtBv/exec"

# ID tabuľky
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
# Čítame priamo hárok "Odpovede z formulára 1" (gid=1116243306 podľa tvojho obrázka)
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1116243306"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                data = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                # Tu posielame dáta
                response = requests.post(WEB_APP_URL, data=json.dumps(data))
                
                if "Success" in response.text:
                    st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                    st.balloons()
                else:
                    st.error(f"Skript odpovedal inak: {response.text}")
            except Exception as e:
                st.error(f"Chyba: {e}")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka je prázdna.")
except:
    st.info("Načítavam históriu...")
