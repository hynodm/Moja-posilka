import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# Nastavenie širokého rozloženia
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- KONFIGURÁCIA (Tvoj overený odkaz z nastavení publikovania) ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLIdDAemHUDjRbs4brpOvaMqO_Bzbn3pkMhq64HfU_iQJqRMbGVe1bka4RV5pyZDUqvjzAUumb3-_0/pub?output=csv"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbu0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21o0ZVwJjI-kYy1M560Nl_S7A/exec"

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
                response = requests.post(WEB_APP_URL, json=payload)
                if response.status_code == 200:
                    st.success("✅ Úspešne zapísané!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Chyba pri zápise: {e}")

st.markdown("---")

# --- 2. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # Načítanie dát s parametrom proti cache pre okamžitú aktualizáciu
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    
    # Prevod dátumu pre filtrovanie (podpora formátu d.m.Y H:M:S)
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    dnes = datetime.now().date()

    # --- SEKCIA: PRÁVE CVIČÍM ---
    st.subheader("📝 Práve cvičím")
    df_dnes = df[df['Dátum_dt'].dt.date == dnes].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        # Zobrazenie dnešných výsledkov
        st.dataframe(df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("Dnes si zatiaľ nič nezapísal. Tu uvidíš výsledky tvojho aktuálneho tréningu.")

    st.markdown("---")
    
    # --- SEKCIA: HISTÓRIA (LEN PREDCHÁDZAJÚCI DÁTUM TRÉNINGU) ---
    st.subheader("⏳ História predchádzajúceho tréningu")
    
    # Vyberieme všetko staršie ako dnes
    hist_vsetko = df[df['Dátum_dt'].dt.date < dnes]

    col1, col2 = st.columns(2)

    def zobraz_kategoriu(stlpik, nazov_kat, data):
        with stlpik:
            st.markdown(f"### {nazov_kat}")
            filtrovane = data[data['Kategória'] == nazov_kat]
            if not filtrovane.empty:
                # Nájdeme posledný dostupný dátum pre túto kategóriu
                posledny_den = filtrovane['Dátum_dt'].dt.date.max()
                vypis = filtrovane[filtrovane['Dátum_dt'].dt.date == posledny_den]
                
                st.success(f"Naposledy cvičené: {posledny_den.strftime('%d.%m.%Y')}")
                # Zobrazenie tabuľky so všetkými stĺpcami, ktoré si žiadal
                st.table(vypis[['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
            else:
                st.write("V tejto kategórii zatiaľ nie je žiadna história.")

    zobraz_kategoriu(col1, "Ostatné", hist_vsetko)
    zobraz_kategoriu(col2, "Ruky a nohy", hist_vsetko)

except Exception as e:
    st.error("Nepodarilo sa načítať históriu. Skontroluj, či je odkaz stále funkčný.")
    st.caption(f"Technická chyba: {e}")
