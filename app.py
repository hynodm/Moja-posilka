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
        cvik_input = st.text_input("Názov cviku")
    with col_b:
        vaha_input = st.number_input("Váha (kg)", min_value=0.0, step=0.5)
    with col_c:
        opak_input = st.number_input("Opakovania", min_value=0, step=1)
    
    if st.form_submit_button("ZAPÍSAŤ DO TABUĽKY"):
        if cvik_input:
            # Pripravíme dáta - posielame ich s viacerými názvami kľúčov pre istotu
            payload = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik_input,
                "vaha": vaha_input,
                "opak": opak_input,
                # Pridávame aj slovenské názvy, ak by ich skript vyžadoval
                "Cvik": cvik_input,
                "Váha (kg)": vaha_input,
                "Opakovania": opak_input
            }
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success(f"✅ Zapísané do tabuľky: {cvik_input}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Chyba komunikácie: {response.status_code}")
            except Exception as e:
                st.error(f"Chyba: {e}")
        else:
            st.warning("Zadaj názov cviku.")

st.markdown("---")

# --- 2. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # Načítanie čerstvých dát
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    
    # Prevod dátumu (ošetrenie chýb)
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    dnesny_den = datetime.now().date()

    # --- SEKCIA: PRÁVE CVIČÍM ---
    st.subheader("📝 Práve cvičím")
    # Filtrujeme presne dnešný dátum
    df_dnes = df[df['Dátum_dt'].dt.date == dnesny_den].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(
            df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], 
            use_container_width=True, hide_index=True
        )
    else:
        st.info("Dnes zatiaľ žiadny záznam. Skús zapísať cvik hore.")

    st.markdown("---")
    
    # --- SEKCIA: HISTÓRIA ---
    st.subheader("⏳ História predchádzajúceho tréningu")
    hist_all = df[df['Dátum_dt'].dt.date < dnesny_den]

    c1, c2 = st.columns(2)

    def render_history(stlp, meno_kat, data):
        with stlp:
            st.markdown(f"### {meno_kat}")
            filtered = data[data['Kategória'] == meno_kat]
            if not filtered.empty:
                last_date = filtered['Dátum_dt'].dt.date.max()
                vypis = filtered[filtered['Dátum_dt'].dt.date == last_date]
                st.success(f"Naposledy: {last_date.strftime('%d.%m.%Y')}")
                st.table(vypis[['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
            else:
                st.write("Žiadne záznamy.")

    render_history(c1, "Ostatné", hist_all)
    render_history(c2, "Ruky a nohy", hist_all)

except Exception as e:
    st.error(f"Dáta sa nepodarilo spracovať: {e}")
