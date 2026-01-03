import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="centered")

# Tvoja adresa z PC (upravená v kóde pre stabilitu)
URL = "https://docs.google.com/spreadsheets/d/1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8/edit?usp=sharing"

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
            
            # Načítanie existujúcich dát
            df = conn.read(spreadsheet=URL)
            
            # Vytvorenie nového riadku
            new_data = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], 
                                   columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
            
            # Spojenie a odoslanie do Google Sheets
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(spreadsheet=URL, data=updated_df)
            st.success("✅ ÚSPEŠNE ZAPÍSANÉ DO TABUĽKY!")
        except Exception as e:
            st.error(f"Chyba pri zápise: {e}")

st.divider()
st.subheader("📊 Dáta z Google Cloudu")
try:
    history = conn.read(spreadsheet=URL)
    if not history.empty:
        st.dataframe(history.tail(10), use_container_width=True)
    else:
        st.info("Tabuľka je zatiaľ prázdna.")
except Exception as e:
    st.error(f"Nepodarilo sa načítať dáta: {e}")
