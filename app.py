import streamlit as st
import pandas as pd
import requests

# Základné nastavenie aplikácie
st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# --- KONFIGURÁCIA ---
# Tvoja najnovšia URL adresa, ktorú si práve poslal
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzfu0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21oOZVwJjITiw0sGfVFc/exec"

# ID tvojej tabuľky
SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"
# Odkaz na čítanie dát z hárka "Data"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

# Formulár na zápis výkonu
with st.form("gym_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť do tabuľky"):
        if cvik:
            try:
                # Parametre, ktoré posielame (musia presne sedieť s Apps Scriptom)
                payload = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                # Odoslanie dát cez GET požiadavku
                response = requests.get(WEB_APP_URL, params=payload, timeout=10)
                
                if "Success" in response.text:
                    st.success("✅ Úspešne zapísané do tabuľky!")
                    st.balloons()
                else:
                    st.error(f"❌ Server vrátil správu: {response.text}")
            except Exception as e:
                st.error(f"❌ Chyba spojenia: {e}")
        else:
            st.warning("⚠️ Prosím, zadaj názov cviku!")

st.divider()
st.subheader("📊 Posledné záznamy")

# Zobrazenie histórie z tabuľky
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobrazenie posledných 10 záznamov (najnovšie hore)
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka je zatiaľ prázdna.")
except Exception:
    st.info("⌛ História sa zobrazí po prvom úspešnom zápise.")
