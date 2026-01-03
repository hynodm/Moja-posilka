
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# ID tvojej tabuľky "Gym data"
SHEET_ID = "1oCkoXdoXdPpP-mdc8s9qPhQjTRUfzHcGTxeIySehyh8"

# Odkaz na čítanie konkrétneho hárka "Form Responses 1" (gid=1264353483)
# Toto zabezpečí, že v aplikácii uvidíš to, čo prišlo cez formulár
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1264353483"

# Odkaz na tvoj Google Formulár pre ZÁPIS
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdR2AkDaoNk9Z0OCdglFkwrQJMGOjNF9PAc5IncDW0HEyarJw/formResponse"

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
                
                # Dáta pre Google formulár
                payload = {
                    "entry.1481534065": dnes,
                    "entry.1051515234": kat,
                    "entry.1415151515": cvik,
                    "entry.1815151515": str(vaha),
                    "entry.1915151515": str(opak)
                }
                
                # Odoslanie
                requests.post(FORM_URL, data=payload)
                st.success("✅ ÚSPEŠNE ZAPÍSANÉ DO GYM DATA!")
                st.balloons()
                st.info("Záznam sa v histórii nižšie objaví po obnovení stránky.")
            except:
                st.error("Chyba pri komunikácii s Google Formulárom.")
        else:
            st.warning("Prosím, vyplň názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    # Načítanie dát z nového hárka
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobraziť posledných 15 tréningov, najnovšie navrchu
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Zatiaľ žiadne záznamy v hárku s odpoveďami.")
except Exception as e:
    st.info("História sa pripravuje. Skús urobiť prvý zápis a obnoviť aplikáciu.")
