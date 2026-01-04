
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gym Progres", layout="centered")

# Odkaz na tvoj formulár "Zápis do posilky"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf8M1syqL9A66Tl8MlBm7ntKD1tV8NcYi8WDSc1ewzeXZ7YzA/formResponse"

# ID tvojej tabuľky (zo súboru Zápis do posilky - Odpovede z formulára 1)
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
                # Payload s ID kódmi upravenými podľa tvojho poradia v tabuľke
                # Kategória (984639089), Opakovanie (1345757671), Cvik (472178838), Váha (959036654)
                payload = {
                    "entry.984639089": kat,         # Stĺpec B: Kategória
                    "entry.1345757671": str(opak),  # Stĺpec C: Opakovanie
                    "entry.472178838": cvik,        # Stĺpec D: Cvik
                    "entry.959036654": str(vaha)    # Stĺpec E: Váha
                }
                
                requests.post(FORM_URL, data=payload)
                st.success("✅ ZAPÍSANÉ!")
                st.balloons()
            except:
                st.error("Chyba pri zápise.")
        else:
            st.warning("Napíš názov cviku!")

st.divider()
st.subheader("📊 História")

try:
    # Načítame dáta a uistíme sa, že berieme tie správne stĺpce
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # Zobraziť len relevantné stĺpce, ak by tam bol chaos
        st.dataframe(df.tail(15)[::-1], use_container_width=True)
    else:
        st.info("Tabuľka je prázdna.")
except:
    st.info("História sa načíta po úspešnom zápise.")
