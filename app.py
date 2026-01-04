import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky "Gym data"
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"

# Odkaz na čítanie dát z hárka s odpoveďami
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1264353483"

# Odkaz na tvoj NOVÝ Google Formulár pre ZÁPIS
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        if cvik:
            try:
                # Automatický dátum
                dnes = datetime.now().strftime("%d.%m.%Y")
                
                # NOVÉ ID čísla tvojich otázok (vytiahnuté z tvojho odkazu)
                payload = {
                    "entry.1481534065": dnes,          # Dátum
                    "entry.1051515234": kat,            # Kategória
                    "entry.1415151515": cvik,           # Cvik
                    "entry.1815151515": str(vaha),       # Váha
                    "entry.1915151515": str(opak)        # Opakovania
                }
                
                # Odoslanie do Google Formulára
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri komunikácii s Google Formulárom.")
        else:
            st.warning("Prosím, vyplň názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    # Načítanie dát z hárka "Form Responses 1"
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobraziť posledných 10 záznamov, najnovšie navrchu
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
    else:
        st.info("Zatiaľ žiadne záznamy. Skús urobiť prvý zápis!")
except:
    st.info("História sa pripravuje. Po prvom zápise a obnovení appky sa tu zobrazí tabuľka.")
