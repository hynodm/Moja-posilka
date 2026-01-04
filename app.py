
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# Odkaz na tvoj NOVÝ formulár "Do posilky"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

# ID tvojej novej tabuľky (z tvojho obrázka 1000013554)
# Ak si vytvoril úplne novú tabuľku, skontroluj, či ID v adrese zostalo rovnaké.
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Payload s NOVÝMI ID kódmi
                payload = {
                    "entry.984639089": kat,         # Kategória
                    "entry.472178838": cvik,        # Cvik
                    "entry.959036654": str(vaha),   # Váha
                    "entry.1345757671": str(opak)   # Opakovanie
                }
                
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ DO NOVEJ TABUĽKY!")
                st.balloons()
            except:
                st.error("Chyba pri zápise.")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História (Nový hárok)")

try:
    # Skúsime načítať dáta. Ak si prepojil formulár s existujúcou tabuľkou, 
    # možno budeme musieť neskôr doladiť gid= číslo.
    df = pd.read_csv(READ_URL)
    if not df.empty:
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Zatiaľ žiadne záznamy.")
except:
    st.info("História sa zobrazí po prvom zápise.")
