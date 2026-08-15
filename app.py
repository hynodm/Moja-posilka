import streamlit as st
import pandas as pd
import requests
import io
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- KONFIGURÁCIA ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?gid=1768652951&single=true&output=csv"

st.title("🏋️ Progres")

# --- FORMULÁR PRIAMO V APPKE (BEZ GOOGLE FORMULÁRA) ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    vaha = st.number_input("Váha (kg)", min_value=0.0, step=2.5, format="%.2f")
    opak = st.number_input("Opakovania", min_value=0, step=1)
    
    submitted = st.form_submit_button("ZÁPISAŤ")
    
    if submitted:
        if not cvik:
            st.warning("Vyplň názov cviku!")
        else:
            dnes = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"Zaznamenané: {dnes} | {kat} | {cvik} - {vaha} kg x {opak}")
            # Tu môžeš doplniť vlastné spracovanie alebo ukladanie

st.divider()

# --- ZOBRAZENIE HISTÓRIE ---
try:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(CSV_URL, headers=headers)
    
    if response.status_code == 200:
        csv_data = io.StringIO(response.text)
        df = pd.read_csv(csv_data)
        df.columns = [str(c).strip().replace('"', '') for c in df.columns]
        
        date_col = df.columns[0]
        
        # Nájdeme stĺpec kategórie
        cat_column = None
        for col in df.columns:
            vals = df[col].astype(str).str.lower()
            if vals.str.contains("ostatné|ruky", regex=True).any():
                cat_column = col
                break
        if not cat_column:
            cat_column = df.columns[1]

        # Dáta pre Ostatné (zoberú úplne posledný deň)
        posledny_riadok_datum = str(df.iloc[-1][date_col]).split(" ")[0]
        df_today = df[df[date_col].astype(str).str.startswith(posledny_riadok_datum)]
        df_ost = df_today[df_today[cat_column].astype(str).str.contains("ostat", case=False, na=False)]
        if df_ost.empty:
            df_ost = df_today # poistka

        # Dáta pre Ruky a nohy (hľadáme posledný deň, kedy sa cvičili ruky/nohy)
        df_ruky_all = df[df[cat_column].astype(str).str.contains("ruky", case=False, na=False)]
        if not df_ruky_all.empty:
            posledny_datum_ruky = str(df_ruky_all.iloc[-1][date_col]).split(" ")[0]
            df_ruky = df_ruky_all[df_ruky_all[date_col].astype(str).str.startswith(posledny_datum_ruky)]
        else:
            posledny_datum_ruky = "žiadny"
            df_ruky = pd.DataFrame()

        tab1, tab2 = st.tabs(["🏋️ Ruky a nohy", "🥊 Ostatné"])
        
        with tab1:
            st.caption(f"Posledný tréning Ruky a nohy zo dňa: {posledny_datum_ruky}")
            if not df_ruky.empty:
                st.dataframe(df_ruky, use_container_width=True)
            else:
                st.info("Zatiaľ žiadne záznamy v kategórii 'Ruky a nohy'.")
                
        with tab2:
            st.caption(f"Posledný tréning Ostatné zo dňa: {posledny_riadok_datum}")
            if not df_ost.empty:
                st.dataframe(df_ost, use_container_width=True)
            else:
                st.info("Žiadne záznamy v kategórii 'Ostatné'.")
            
    else:
        st.error(f"Nepodarilo sa načítať dáta (HTTP {response.status_code}).")

except Exception as e:
    st.error(f"Chyba pri spracovaní dát: {e}")
