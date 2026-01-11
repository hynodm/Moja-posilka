import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 1. KONFIGURÁCIA (Opravené ID podľa tvojho screenshotu) ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbu0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21o0ZVwJjI-kYy1M560Nl_S7A/exec"
SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVtdSQZKMOFq8"
GID = "551519505"

# --- 2. FORMULÁR PRE ZÁPIS ---
st.title("🏋️ Môj Gym Progres")

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

# --- 3. NAČÍTANIE A ZOBRAZENIE DÁT ---
try:
    # URL pre priamy export do CSV
    read_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}&cache={int(time.time())}"
    df = pd.read_csv(read_url)
    
    # Prevod dátumu na prácu s časom
    df['Dátum_dt'] = pd.to_datetime(df['Dátum'], dayfirst=True, errors='coerce')
    dnes = datetime.now().date()

    # SEKCIA: PRÁVE CVIČÍM (Dnešné záznamy)
    st.subheader("📝 Práve cvičím")
    df_dnes = df[df['Dátum_dt'].dt.date == dnes].sort_values(by='Dátum_dt', ascending=False)
    
    if not df_dnes.empty:
        st.dataframe(df_dnes[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']], use_container_width=True, hide_index=True)
    else:
        st.info("Dnes zatiaľ žiadny zápis. Tvoje dnešné cviky uvidíš tu.")

    st.markdown("---")
    
    # SEKCIA: HISTÓRIA (Predchádzajúce tréningy)
    st.subheader("⏳ História predchádzajúceho tréningu")
    historia_all = df[df['Dátum_dt'].dt.date < dnes]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💪 Ostatné")
        h_ost = historia_all[historia_all['Kategória'] == "Ostatné"]
        if not h_ost.empty:
            posl_den = h_ost['Dátum_dt'].dt.date.max()
            vypis = h_ost[h_ost['Dátum_dt'].dt.date == posl_den]
            st.success(f"Naposledy: {posl_den.strftime('%d.%m.%Y')}")
            st.table(vypis[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']])
        else:
            st.write("Žiadna história pre 'Ostatné'.")

    with col2:
        st.markdown("### 🦵 Ruky a nohy")
        h_ruky = historia_all[historia_all['Kategória'] == "Ruky a nohy"]
        if not h_ruky.empty:
            posl_den = h_ruky['Dátum_dt'].dt.date.max()
            vypis = h_ruky[h_ruky['Dátum_dt'].dt.date == posl_den]
            st.success(f"Naposledy: {posl_den.strftime('%d.%m.%Y')}")
            st.table(vypis[['Dátum', 'Kategória', 'Cvik', 'Váha (kg)', 'Opakovania']])
        else:
            st.write("Žiadna história pre 'Ruky a nohy'.")

except Exception as e:
    st.error(f"Nepodarilo sa načítať dáta: {e}")
