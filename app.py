import streamlit as st
import pandas as pd
import requests

# Nastavenie vzhľadu
st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# --- TVOJA POSLEDNÁ ADRESA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxCROtSStArcNvfGoq4DD_Dd-h_4vV8-YoUkqRdCzlDUhPPRCHXJzjzAH1QbAoegoDu/exec"

SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Dáta, ktoré posielame do Apps Scriptu
                payload = {"kat": kat, "cvik": cvik, "vaha": str(vaha), "opak": str(opak)}
                response = requests.get(WEB_APP_URL, params=payload, timeout=10)
                
                if "Success" in response.text:
                    st.success("✅ Úspešne zapísané!")
                    st.balloons()
                else:
                    st.error(f"❌ Odpoveď servera: {response.text}")
            except Exception as e:
                st.error(f"❌ Chyba spojenia: {e}")
        else:
            st.warning("⚠️ Zadaj názov cviku!")

st.divider()
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
except:
    st.info("⌛ Čakám na prvý zápis...")
