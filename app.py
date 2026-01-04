import streamlit as st
import pandas as pd
import requests

# Základné nastavenie aplikácie
st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# --- KONFIGURÁCIA ---
# Tvoja nová URL adresa z poslednej správy
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxCROtSStArcNvfGoq4DD_Dd-h_4vV8-YoUkqRdCzlDUhPPRCHXJzjzAH1QbAoegoDu/exec"

# ID tvojej tabuľky
SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"

# Odkaz na čítanie dát priamo z hárka "Data"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie tréningu
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

# Formulár pre zápis výkonu
with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Príprava parametrov na odoslanie (kat, cvik, vaha, opak)
                params = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                
                # Odoslanie dát cez GET (najistejšia metóda pre Google Script)
                response = requests.get(WEB_APP_URL, params=params)
                
                if "Success" in response.text:
                    st.success("✅ Úspešne zapísané do tabuľky!")
                    st.balloons()
                else:
                    st.error(f"⚠️ Server vrátil správu: {response.text}")
            except Exception as e:
                st.error(f"❌ Chyba spojenia: {e}")
        else:
            st.warning("⚠️ Prosím, zadaj názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

# Načítanie a zobrazenie histórie z tabuľky
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobrazenie posledných 15 záznamov, najnovšie sú navrchu
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka 'Data' je zatiaľ prázdna.")
except Exception:
    st.info("⌛ História sa zobrazí po prvom úspešnom zápise.")
