import streamlit as st
import pandas as pd

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- TVOJE ADRESY ---
URL_FORMULARA = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/viewform"

# Odkaz priamo na tvoju Google tabuľku (export do CSV cez base prepojenie)
# ID tabuľky: 1K81RIVLwfOKGap8d-1_ERDJvo8CBTWVTDsQZKMOFq8
CSV_URL = "https://docs.google.com/spreadsheets/d/1K81RIVLwfOKGap8d-1_ERDJvo8CBTWVTDsQZKMOFq8/export?format=csv&gid=1768652951"

st.title("🏋️ Gym Progres - Stabilný prístup")

# --- HLAVNÁ ČASŤ ---
st.info("Aplikácia využíva oficiálny formulár na zápis a priamo načítava dáta z tabuľky.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Zápis tréningu")
    st.write("Kliknutím na tlačidlo otvoríš oficiálny formulár Google:")
    st.markdown(f'<a href="{URL_FORMULARA}" target="_blank" style="text-decoration:none;"><button style="padding:10px 20px; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px; font-weight:bold;">OTVORIŤ FORMULÁR</button></a>', unsafe_allow_html=True)

with col2:
    st.subheader("Rýchly náhľad tabuľky")
    st.write("Aktuálne dáta načítané z tvojho dokumentu:")

st.divider()

# --- AUTOMATICKÉ ZOBRAZENIE HISTÓRIE ---
try:
    # Priamy export tabuľky do CSV formátu (funguje, ak má tabuľka zapnuté zdieľanie "Každý, kto má odkaz")
    df = pd.read_csv(CSV_URL)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.warning("Zatiaľ sa nepodarilo načítať dáta. Uistite sa, že Google tabuľka je zdieľaná pre 'Každý, kto má odkaz'.")
    st.caption(f"Detail chyby: {e}")
