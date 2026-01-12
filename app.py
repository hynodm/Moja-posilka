import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# Nastavenie širokého rozloženia
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- KONFIGURÁCIA ---
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
            # Vytvorenie dátumu v presnom formáte, aký máš v tabuľke
            now = datetime.now()
            payload = {
                "datum": now.strftime("%-d.%-m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik,
                "vaha": vaha,
                "opak": opak
            }
            try:
                # Odoslanie s časovým limitom (timeout), aby apka nezamrzla
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success(f"✅ Úspešne zapísané: {cvik}")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(f"Chyba servera: {response.status_code}")
            except Exception as e:
                st.error(f"Nepodarilo sa odoslať dáta: {e}")
        else:
            st.warning("Napíš názov cviku.")

st.markdown("---")

# --- 2. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # Vynútené načítanie čerstvých dát pridaním unikátneho parametra
    df = pd.read_csv(f"{CSV_URL}&nocache={int(time.time())}")
    
    # Robustnejší prevod dátumu - skúsi viaceré formáty, ktoré sa v tabuľke môžu objaviť
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    
    # Odstránenie riadkov, kde sa dátum nepodarilo spracovať
    df = df.dropna(subset=['Dátum_dt'])
    
    dnesny_datum = datetime.now().date()

    # --- SEKCIA: PRÁVE CVIČÍM ---
    st.subheader("📝 Práve cvičím")
    # Filtrujeme presne podľa dnešného dňa
    df_dnes = df[df['Dátum_dt'].dt.date == dnesny_datum].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(
            df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("Dnes v apke zatiaľ nič nevidno. Skús zapísať cvik cez formulár vyššie.")

    st.markdown("---")
    
    # --- SEKCIA: HISTÓRIA ---
    st.subheader("⏳ História predchádzajúceho tréningu")
    hist_vsetko = df[df['Dátum_dt'].dt.date < dnesny_datum]

    col1, col2 = st.columns(2)

    def zobraz_kategoriu(stlpik, nazov_kat, data):
        with stlpik:
            st.markdown(f"### {nazov_kat}")
            filtrovane = data[data['Kategória'] == nazov_kat]
            if not filtrovane.empty:
                posl_den = filtrovane['Dátum_dt'].dt.date.max()
                vypis = filtrovane[filtrovane['Dátum_dt'].dt.date == posl_den]
                st.success(f"Naposledy: {posl_den.strftime('%d.%m.%Y')}")
                st.table(vypis[['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
            else:
                st.write("Žiadna história.")

    zobraz_kategoriu(col1, "Ostatné", hist_vsetko)
    zobraz_kategoriu(col2, "Ruky a nohy", hist_vsetko)

except Exception as e:
    st.error(f"Chyba pri spracovaní dát: {e}")
