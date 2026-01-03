
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="centered")

# Adresa upravená pre priamy export (rieši chybu 404)
URL = "https://docs.google.com/spreadsheets/d/1oCkoXdoXdPpmdc8s9qPhQjTRUfzHcGTxeIySehyh8/export?format=csv"

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
            # Načítanie dát
            df = conn.read(spreadsheet=URL)
            
            # Príprava nového riadku (presná zhoda s tvojou tabuľkou)
            new_data = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], 
                                   columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
            
            # Spojenie dát a aktualizácia
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(spreadsheet=URL, data=updated_df)
            st.success("✅ ÚSPEŠNE ZAPÍSANÉ DO GOOGLE!")
        except Exception as e:
            st.error(f"Chyba pri zápise: {e}")

st.divider()
st.subheader("📊 História z Google Cloudu")
try:
    # Zobrazenie posledných 10 záznamov
    history = conn.read(spreadsheet=URL)
    st.dataframe(history.tail(10), use_container_width=True)
except:
    st.info("Tabuľka v cloude je prázdna alebo nedostupná.")
