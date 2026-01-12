import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA ---
# Tvoja nová adresa Apps Scriptu
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyXtr0a9zWSuUjlb0GrlqVaXpOKqMqtYunMFzkEjizX451UcdhMLvbbPsvcz3hXRlBv/exec"
# Tvoj verejný CSV odkaz
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
            # Payload presne pre JSON.parse v Google Apps Scripte
            payload = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "kategoria": kat,
                "cvik": cvik_input,
                "vaha": float(vaha_input),
                "opak": int(opak_input)
            }
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if "Success" in response.text:
                    st.success(f"✅ Úspešne zapísané: {cvik_input}")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(f"Odpoveď servera: {response.text}")
            except Exception as e:
                st.error(f"Chyba pri odosielaní: {e}")
        else:
            st.warning("Prosím, zadaj názov cviku.")

st.markdown("---")

# --- 4. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # Načítanie s potlačením cache pre okamžité zmeny
    df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
    
    # Prevod dátumu (ošetrenie chýb)
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Dátum_dt'])
    
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
        st.info("Dnes zatiaľ žiadny zápis.")

    st.markdown("---")
    
    # --- SEKCIA: HISTÓRIA ---
    st.subheader("⏳ História predchádzajúceho tréningu")
    historia_all = df[df['Dátum_dt'].dt.date < dnes]

    col1, col2 = st.columns(2)

    def render_history_table(target_col, category_name, source_data):
        with target_col:
            st.markdown(f"### {category_name}")
            category_filtered = source_data[source_data['Kategória'] == category_name]
            if not category_filtered.empty:
                last_workout_date = category_filtered['Dátum_dt'].dt.date.max()
                display_df = category_filtered[category_filtered['Dátum_dt'].dt.date == last_workout_date]
                st.success(f"Naposledy: {last_workout_date.strftime('%d.%m.%Y')}")
                st.table(display_df[['Dátum', 'Cvik', 'Váha (kg)', 'Opakovania']])
            else:
                st.write("Žiadna história.")

    render_history_table(col1, "Ostatné", historia_all)
    render_history_table(col2, "Ruky a nohy", historia_all)

except Exception as e:
    st.error(f"Chyba pri spracovaní dát: {e}")
