import streamlit as st
import pandas as pd
import requests
import io
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA GOOGLE FORMULÁRA ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/formResponse"

ENTRY_DATUM = "entry.1160346068"
ENTRY_KATEGORIA = "entry.312830153"
ENTRY_CVIK = "entry.83240949"
ENTRY_VAHA = "entry.1078103613"
ENTRY_OPAK = "entry.166466953"

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?gid=1768652951&single=true&output=csv"

st.title("🏋️ Progres")

# --- 3. FORMULÁR PRE ZÁPIS ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    vaha = st.number_input("Váha (kg)", min_value=0.0, step=2.5, format="%.2f")
    opak = st.number_input("Opakovania", min_value=0, step=1)
    
    submitted = st.form_submit_button("ZÁPISAŤ DO TABUĽKY")
    
    if submitted:
        if not cvik:
            st.warning("Vyplň názov cviku!")
        else:
            dnes = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payload = {
                ENTRY_DATUM: dnes,
                ENTRY_KATEGORIA: kat,
                ENTRY_CVIK: cvik,
                ENTRY_VAHA: str(vaha),
                ENTRY_OPAK: str(opak)
            }
            try:
                res = requests.post(FORM_URL, data=payload)
                res.raise_for_status()
                st.success(f"Uložené: {cvik} - {vaha} kg x {opak}")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Chyba pri zápise: {e}")

st.divider()

# --- 4. ZOBRAZENIE HISTÓRIE ---
try:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(CSV_URL, headers=headers)
    
    if response.status_code == 200:
        csv_data = io.StringIO(response.text)
        df = pd.read_csv(csv_data)
        df.columns = [str(c).strip().replace('"', '') for c in df.columns]
        
        date_col = df.columns[0]
        posledny_riadok_datum = str(df.iloc[-1][date_col]).split(" ")[0]
        df_today = df[df[date_col].astype(str).str.startswith(posledny_riadok_datum)]

        st.subheader(f"📅 Záznamy z posledného tréningu ({posledny_riadok_datum})")

        tab1, tab2 = st.tabs(["🏋️ Ruky a nohy", "🥊 Ostatné"])
        
        # Nájdeme stĺpec, kde sa nachádza text kategórie (hľadáme stĺpec s hodnotami "Ostatné" alebo "Ruky a nohy")
        cat_column = None
        for col in df_today.columns:
            vals = df_today[col].astype(str).str.lower()
            if vals.str.contains("ostatné|ruky", regex=True).any():
                cat_column = col
                break

        with tab1:
            if cat_column:
                df_ruky = df_today[df_today[cat_column].astype(str).str.contains("ruky", case=False, na=False)]
            else:
                df_ruky = pd.DataFrame()
                
            if not df_ruky.empty:
                st.dataframe(df_ruky, use_container_width=True)
            else:
                st.info("Žiadne záznamy v kategórii 'Ruky a nohy' pre tento deň.")
                
        with tab2:
            if cat_column:
                df_ost = df_today[df_today[cat_column].astype(str).str.contains("ostat", case=False, na=False)]
            else:
                df_ost = df_today # ak nenájde stĺpec, ukáže všetko
                
            if not df_ost.empty:
                st.dataframe(df_ost, use_container_width=True)
            else:
                st.info("Žiadne záznamy v kategórii 'Ostatné' pre tento deň.")
            
    else:
        st.error(f"Nepodarilo sa načítať dáta (HTTP {response.status_code}).")

except Exception as e:
    st.error(f"Chyba pri spracovaní dát: {e}")
