import streamlit as st
import pandas as pd

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- TVOJE ADRESY ---
URL_FORMULARA = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/viewform"

# Použijeme webový pub odkaz na celú tabuľku (ten, ktorý Google vygeneruje ako prvý)
WEB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pubhtml"

st.title("🏋️ Gym Progres - Stabilný prístup")

# --- HLAVNÁ ČASŤ ---
st.info("Aplikácia využíva oficiálny formulár na zápis a načítava dáta z tabuľky.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Zápis tréningu")
    st.write("Kliknutím na tlačidlo otvoríš oficiálny formulár Google:")
    st.markdown(f'<a href="{URL_FORMULARA}" target="_blank" style="text-decoration:none;"><button style="padding:10px 20px; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px; font-weight:bold;">OTVORIŤ FORMULÁR</button></a>', unsafe_allow_html=True)

with col2:
    st.subheader("Rýchly náhľad tabuľky")
    st.write("Aktuálne dáta:")

st.divider()

# --- AUTOMATICKÉ ZOBRAZENIE HISTÓRIE ---
try:
    # Načítanie tabuľki priamo z publikovanej HTML stránky
    df_list = pd.read_html(WEB_URL)
    if df_list:
        df = df_list[0]
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("V tabuľke sa nenašli žiadne dáta.")
except Exception as e:
    st.warning("Tabuľka ešte nie je publikovaná na web. Pre zobrazenie údajov urobte toto:")
    st.markdown("""
    1. Otvorte svoju Google tabuľku v počítači.
    2. Hore kliknite na **Súbor** -> **Zdieľať** -> **Publikovať na web**.
    3. Kliknite na veľké zelené tlačidlo **Publikovať**.
    """)
