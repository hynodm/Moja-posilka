import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 1. ZÁKLADNÉ NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA (Tvoje adresy) ---
# Adresa z "Nasadiť" (Deploy) v Google Apps Scripte
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyXtr0a9zWSuUjlb0GrlqVaXpOKqMqtYunMFzkEjizX451UcdhMLvbbPsvcz3hXRlBv/exec"
# Adresa z "Publikovať na webe" (CSV formát)
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
            # Payload upravený tak, aby ho JSON.parse v skripte správne prečítal
            payload = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik_input,
                "vaha": float(vaha_input),
                "opak": int(opak_input)
            }
            try:
                # Odoslanie dát do Google Tabuľky
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if "Success" in response.text:
                    st.success(f"✅ Úspešne zapísané: {cvik_input}")
                    time.sleep(1)
                    st.rerun()
                else:
                    # Ak skript vráti chybu, zobrazíme ju
                    st.error(f"Odpoveď servera: {response.text}")
            except Exception as e:
                st.error(f"Chyba pri odosielaní: {e}")
        else:
            st.warning("Prosím, zadaj názov cviku.")

st.markdown("---")

# --- 4. NAČÍTANIE A ZOBRAZENIE HISTÓRIE ---
try:
    # Načítanie CSV s timestampom, aby sme nevideli staré dáta (cache)
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    
    # Prevod dátumu na formát, ktorému rozumie Python
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    
    # Odstránenie chybných riadkov (ak by nejaké vznikli)
    df = df.dropna(subset=['Dátum_dt'])
    
    dnes = datetime.now().date()

    # SEKCIA: PRÁVE CVIČÍM (Len dnešné záznamy)
    st.subheader("📝 Práve cvičím")
    df_dnes = df[df['Dátum_dt'].dt.date == dnes].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(
            df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("Dnes zatiaľ žiadny zápis. Tvoj aktuálny tréning uvidíš tu.")

    st.markdown("---")
    
    # SEKCIA: HISTÓRIA (Staršie tréningy)
    st.subheader("⏳ História predchádzajúceho tréningu")
    hist_all = df[df['Dátum_dt'].dt.date < dnes]

    col1, col2 = st.columns(2)

    # Funkcia na vykreslenie histórie pre jednotlivé kategórie
    def render_history_table(stlp, meno_kategorie, data):
        with stlp:
            st.markdown(f"### {meno_kategorie}")
