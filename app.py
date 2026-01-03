
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="centered")

# Riadok 9: Tvoja adresa upravená tak, aby fungovala v mobile
URL = "https://docs.google.com/spreadsheets/d/1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8/export?format=csv"

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        try:
            dnes = datetime.now().strftime("%d.%m.%Y")
            # Načítanie dát cez export formát (rieši chybu 404)
            df = pd.read_csv(URL)
            
            new_data = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], 
                                   columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
            
            updated_df = pd.concat([df, new_data], ignore_index=True)
            # Zápis späť do tabuľky
            conn.update(spreadsheet=URL.replace("/export?format=csv", "/edit"), data=updated_df)
            st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
        except Exception as e:
            st.error(f"Chyba pri zápise: {e}")

st.divider()
st.subheader("📊 História")
try:
    history = pd.read_csv(URL)
    st.dataframe(history.tail(10), use_container_width=True)
except:
    st.info("Tabuľka je prázdna.")
