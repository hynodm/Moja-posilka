import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# Nastavenie širokého rozloženia
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- KONFIGURÁCIA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyXtr0a9zWSuUjlb0GrlqVaXpOKqMqtYunMFzkEjizX451UcdhMLvbbPsvcz3hXRlBv/exec"
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?output=csv"

st.title("🏋️ Môj Gym Progres")

# --- 1. FORMULÁR PRE ZÁPIS ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_zapis", clear_on_submit=True):
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        cvik = st.text_input("Názov cviku")
    with col_b:
        vaha = st.number_input("Váha (kg)", min_value=0.0, step=2.5)
    with col_c:
        opak = st.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("ZAPÍSAŤ DO TABUĽKY"):
        if cvik:
            payload = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik,
                "vaha": vaha,
                "opak": opak
            }
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success(f"✅ Úspešne zapísané: {cvik}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Chyba servera: {response.status_code}")
            except Exception as e:
                st.error(f"Nepodarilo sa odoslať dáta: {e}")
        else:
            st.warning("Prosím, zadaj názov cviku.")

st.markdown("---")

# --- 2. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # Načítanie s ochranou proti cache
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    
    # Prevod dátumu
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    dnes = datetime.now().date()

    # --- SEKCIA: PRÁVE CVIČÍM ---
    st.subheader("📝 Práve cvičím")
    df_dnes = df[df['Dátum_dt'].dt.date == dnes].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(
            df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("Dnes si zatiaľ nič nezapísal.")

    st.markdown("---")
    
    # --- SEKCIA: HISTÓRIA ---
    st.subheader("⏳ História predchádzajúceho tréningu")
    historia_all = df[df['Dátum_dt'].dt.date < dnes]

    col1, col2 = st.columns(2)

    def zobraz_historiu(kam, kategoria_nazov, vsetky_data):
        with kam:
            st.markdown(f"### {kategoria_nazov}")
            kat_data = vsetky_data[vsetky_data['Kategória'] == kategoria_nazov]
            if not kat_data.empty:
                posledny_den = kat_data['Dátum_dt'].dt.date.max()
                vypis = kat_data[kat_data['Dátum_dt'].dt.date == posledny_den]
                st.success(f"Naposledy: {posledny_den.strftime('%d.%m.%Y')}")
                st.table(vypis[['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
            else:
                st.write("Žiadna história.")

    zobraz_historiu(col1, "Ostatné", historia_all)
    zobraz_historiu(col2, "Ruky a nohy", historia_all)

except Exception as e:
    st.error(f"Chyba pri načítaní dát: {e}")
