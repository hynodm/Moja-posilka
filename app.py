import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- TVOJE ADRESY ---
URL_FORMULARA = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/viewform"
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?gid=1768652951&single=true&output=csv"

st.title("🏋️ Gym Progres - Analýza a História")

# --- HLAVNÁ ČASŤ ---
st.info("Aplikácia na sledovanie tréningového progresu a analýzu kategórií.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Zápis tréningu")
    st.write("Kliknutím na tlačidlo otvoríš oficiálny formulár Google:")
    st.markdown(f'<a href="{URL_FORMULARA}" target="_blank" style="text-decoration:none;"><button style="padding:10px 20px; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px; font-weight:bold;">OTVORIŤ FORMULÁR</button></a>', unsafe_allow_html=True)

with col2:
    st.subheader("Rýchly náhľad tabuľky")
    st.write("Dáta priamo z tvojho dokumentu:")

st.divider()

# --- NAČÍTANIE A SPRACOVANIE DÁT ---
try:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(CSV_URL, headers=headers)
    
    if response.status_code == 200:
        csv_data = io.StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Kontrola, či tabuľka nie je prázdna
        if not df.empty:
            st.success("Dáta boli úspešne načítané.")
            
            # Zobrazenie kompletnej tabuľky s históriou
            st.subheader("Kompletná história záznamov")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.warning("Tabuľka zatiaľ neobsahuje žiadne záznamy.")
    else:
        st.warning(f"Nepodarilo sa načítať dáta (HTTP {response.status_code}). Skontrolujte zverejnenie hárku.")
        
except Exception as e:
    st.error(f"Chyba pri spracovaní dát: {e}")
