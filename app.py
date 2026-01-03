import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# Tvoj ID tabuľky (vytiahnuté z tvojho odkazu)
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
# Odkaz na Google Forms script alebo priamy zápis (zjednodušené pre čítanie)
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        st.warning("⚠️ Google vyžaduje overenie pre ZÁPIS. Skúsme aspoň načítať dáta nižšie.")
        # Pre plnohodnotný zápis bez hesla je najlepšie použiť Google Form, 
        # ale skúsme teraz, či aspoň vidíš históriu bez chyby 404.

st.divider()
st.subheader("📊 História z tabuľky")
try:
    df = pd.read_csv(URL)
    st.dataframe(df.tail(10), use_container_width=True)
    st.success("✅ Spojenie s tabuľkou je AKTÍVNE!")
except Exception as e:
    st.error(f"Dáta sa nepodarilo načítať: {e}")
