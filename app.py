
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky a odkazy
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"
# Odkaz na tvoj formulár pre zápis (zostáva rovnaký, ten funguje)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie
kat = st.radio("Kategória", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # ID políčok z tvojho formulára
                payload = {
                    "entry.984639089": kat,         
                    "entry.959036654": cvik,        
                    "entry.472178838": str(vaha),   
                    "entry.1345757671": str(opak)   
                }
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri zápise.")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

# Automatické načítanie posledného hárka (Odpovede 2)
try:
    # Skúsime načítať druhý hárok (často má index 1 alebo gid podľa poradia)
    # Ak gid=0 nefunguje správne, skúsime načítať CSV verziu celého zošita
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(CSV_URL)
    
    if not df.empty:
        # Zobrazíme posledných 15 záznamov, najnovšie navrchu
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Zatiaľ žiadne záznamy v novom hárku.")
except Exception as e:
    st.info("História sa pripravuje. Urob prvý zápis a obnov aplikáciu.")
