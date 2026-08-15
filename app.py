import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA GOOGLE FORMULÁRA ---
# Adresa pre odosielanie dát z formulára
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/formResponse""

# Mapovanie ID políčok z tvojho formulára
ENTRY_DATUM = "entry.1160346068"
ENTRY_KATEGORIA = "entry.312830153"
ENTRY_CVIK = "entry.83240949"
ENTRY_VAHA = "entry.1078103613"
ENTRY_OPAK = "entry.166466953"

# CSV odkaz na záložku "Odpovede z formulára 2"
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?gid=551519505&single=true&output=csv"

st.title("🏋️ Môj Gym Progres")

# --- 3. FORMULÁR PRE ZÁPIS ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    vaha = st.number_input("Váha (kg)", min_value=0.0, step=0.5, format="%.2f")
    opak = st.number_input("Opakovania", min_value=0, step=1)
    
    submitted = st.form_submit_button("ZÁPISAŤ DO TABUĽKY")

if submitted:
    if cvik.strip() == "":
        st.warning("⚠️ Vyplň názov cviku!")
    else:
        dnes = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Príprava dát pre Google Formulár
        payload = {
            ENTRY_DATUM: dnes,
            ENTRY_KATEGORIA: kat,
            ENTRY_CVIK: cvik,
            ENTRY_VAHA: str(vaha),
            ENTRY_OPAK: str(opak)
        }
        
        try:
            res = requests.post(FORM_URL, data=payload, timeout=5)
            if res.status_code == 200:
                st.success(f"✅ Zápis pridaný: {cvik} ({vaha} kg x {opak})")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Chyba pri zápise: HTTP {res.status_code}")
        except Exception as e:
            st.error(f"Chyba pripojenia: {e}")

st.markdown("---")

# --- 4. NAČÍTANIE HISTÓRIE ---
try:
    df = pd.read_csv(CSV_URL)
    
    if not df.empty:
        st.subheader("História cvičení")
        
        # Zobrazenie stĺpcov
        df_filtered = df[df["Kategória"] == kat] if "Kategória" in df.columns else df
        
        if not df_filtered.empty:
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.info(f"Žiadne dáta v kategórii {kat}.")
            
except Exception as e:
    st.error(f"Nepodarilo sa načítať históriu: {e}")
