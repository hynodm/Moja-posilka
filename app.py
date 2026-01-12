import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA ---
# SEM MUSÍŠ VLOŽIŤ NOVÚ ADRESU, KTORÚ ZÍSKAL V KROKU 2 NIŽŠIE
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21o0ZVwJjI-kYy1M560Nl_S7A/exec"

# Verejný CSV odkaz
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?output=csv"

st.title("🏋️ Môj Gym Progres")

# --- 3. FORMULÁR PRE ZÁPIS ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_zapis", clear_on_submit=True):
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        cvik_input = st.text_input("Názov cviku")
    with col_b:
        vaha_input = st.number_input("Váha (kg)", min_value=0.0, step=0.5)
    with col_c:
        opak_input = st.number_input("Opakovania", min_value=0, step=1)
    
    if st.form_submit_button("ZAPÍSAŤ DO TABUĽKY"):
        if cvik_input:
            # Posielame dáta ako klasické parametre v URL (najspoľahlivejšia cesta)
            params = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik_input,
                "vaha": vaha_input,
                "opak": opak_input
            }
            try:
                # Dôležité: Používame params=params namiesto json=payload
                response = requests.post(WEB_APP_URL, params=params, timeout=15)
                
                if response.status_code == 200:
                    st.success(f"✅ Zapísané: {cvik_input}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Chyba: Server vrátil kód {response.status_code}")
            except Exception as e:
                st.error(f"Chyba pripojenia: {e}")
        else:
            st.warning("Zadaj názov cviku!")

st.markdown("---")

# --- 4. NAČÍTANIE HISTÓRIE ---
try:
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Dátum_dt'])
    dnes = datetime.now().date()

    st.subheader("📝 Práve cvičím")
    df_dnes = df[df['Dátum_dt'].dt.date == dnes].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], use_container_width=True, hide_index=True)
    else:
        st.info("Dnes zatiaľ nič.")

    st.markdown("---")
    st.subheader("⏳ História")
    hist_all = df[df['Dátum_dt'].dt.date < dnes]
    c1, c2 = st.columns(2)

    def draw(col, name, data):
        with col:
            st.markdown(f"### {name}")
            f = data[data['Kategória'] == name]
            if not f.empty:
                last = f['Dátum_dt'].dt.date.max()
                st.table(f[f['Dátum_dt'].dt.date == last][['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
    
    draw(c1, "Ostatné", hist_all)
    draw(c2, "Ruky a nohy", hist_all)
except Exception as e:
    st.error(f"Chyba dát: {e}")
