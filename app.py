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

CSV_URL = "https://docs.google.com/spreadsheets/d/1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWvTDSQZKMOFq8/gviz/tq?tqx=out:csv&sheet=Odpovede%20z%20formul%C3%A1ra%202"

st.title("🏋️ Môj Gym Progres")

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
                if res.status_code == 200:
                    st.success(f"Uložené: {cvik} - {vaha} kg x {opak}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Chyba pri zápise: HTTP {res.status_code}")
            except Exception as e:
                st.error(f"Chyba spojenia: {e}")

st.divider()

# --- 4. ZOBRAZENIE HISTÓRIE ---
try:
    # Stiahnutie CSV obsahu pomocou requests
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(CSV_URL, headers=headers)
    
    if response.status_code == 200:
        csv_data = io.StringIO(response.text)
        df = pd.read_csv(csv_data)
        df.columns = [c.strip() for c in df.columns]
        
        col_map = {}
        for c in df.columns:
            cl = c.lower()
            if "kateg" in cl: col_map[c] = "Kategória"
            elif "cvik" in cl: col_map[c] = "Cvik"
            elif "váha" in cl or "vaha" in cl: col_map[c] = "Váha (kg)"
            elif "opak" in cl: col_map[c] = "Opakovania"
            elif "dátum" in cl or "datum" in cl or "čas" in cl: col_map[c] = "Dátum"
        
        df = df.rename(columns=col_map)
        
        tab1, tab2 = st.tabs(["🏋️ Ruky a nohy", "🥊 Ostatné"])
        
        with tab1:
            df_ruky = df[df["Kategória"] == "Ruky a nohy"] if "Kategória" in df.columns else pd.DataFrame()
            if not df_ruky.empty:
                st.dataframe(df_ruky[["Dátum", "Cvik", "Váha (kg)", "Opakovania"]], use_container_width=True)
            else:
                st.info("Žiadne dáta v kategórii Ruky a nohy.")
                
        with tab2:
            df_ost = df[df["Kategória"] == "Ostatné"] if "Kategória" in df.columns else pd.DataFrame()
            if not df_ost.empty:
                st.dataframe(df_ost[["Dátum", "Cvik", "Váha (kg)", "Opakovania"]], use_container_width=True)
            else:
                st.info("Žiadne dáta v kategórii Ostatné.")
    else:
        st.error(f"Nepodarilo sa načítať históriu z Google (HTTP {response.status_code}).")

except Exception as e:
    st.error(f"Chyba pri spracovaní histórie: {e}")
