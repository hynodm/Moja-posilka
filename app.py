import streamlit as st
import pandas as pd
import requests
import json

# Základné nastavenie aplikácie
st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# --- KONFIGURÁCIA ---
# Tvoja nová URL adresa, ktorú si práve vygeneroval
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwSB7CigcEIsQPeLqt0_x4b4XZ7vVz7Rz4WgsOc_eDBM1eKfEyOLpyZunMrOSJCpQdt/exec"

# ID tvojej tabuľky (zostáva rovnaké)
SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"

# Odkaz na čítanie dát z hárka "Data"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

# Formulár pre pridanie cviku
with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    submit = st.form_submit_button("Uložiť výkon")
    
    if submit:
        if cvik:
            try:
                # Príprava balíka dát pre Google Tabuľku
                payload = {
                    "kat": kat,
                    "cvik": cvik,
                    "vaha": str(vaha),
                    "opak": str(opak)
                }
                
                # Odoslanie dát cez POST požiadavku
                response = requests.post(WEB_APP_URL, data=json.dumps(payload))
                
                if "Success" in response.text:
                    st.success("✅ HOTOVO! Dáta sú v tabuľke.")
                    st.balloons()
                else:
                    st.error(f"Chyba v skripte: {response.text}")
            except Exception as e:
                st.error(f"Chyba spojenia: {e}")
        else:
            st.warning("⚠️ Nezabudni vyplniť názov cviku!")

st.divider()
st.subheader("📊 História tréningov (Hárok Data)")

# Zobrazenie tabuľky s históriou pod formulárom
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobrazenie posledných 15 záznamov, najnovšie sú hore
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka je zatiaľ prázdna. Skús niečo zapísať!")
except Exception:
    st.info("Čakám na prvý úspešný zápis do hárka 'Data'...")
