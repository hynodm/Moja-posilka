import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# 1. TVOJA OVERENÁ ADRESA PRE ZÁPIS
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzfu0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21oOZVwJjITiw0sGfVFc/exec"

# 2. ADRESA PRE ČÍTANIE (s vynútenou aktualizáciou dát)
# Používame priamy export do CSV z tvojho konkrétneho hárka (gid=551519505)
READ_URL = f"https://docs.google.com/spreadsheets/d/1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSQZKMOFq8/export?format=csv&gid=551519505&cache={int(time.time())}"
GID = "551519505"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}&cache={int(time.time())}"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_zapis", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    vaha = st.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = st.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("ZAPÍSAŤ TERAZ"):
        if cvik:
            try:
                params = {"kat": kat, "cvik": cvik, "vaha": str(vaha), "opak": str(opak)}
                res = requests.get(WEB_APP_URL, params=params, timeout=10)
                if "Success" in res.text:
                    st.success("✅ Úspešne zapísané!")
                    st.balloons()
                    # Počkáme sekundu, aby Google stihol spracovať zápis pred obnovou tabuľky
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Chyba servera: {res.text}")
            except Exception as e:
                st.error(f"❌ Chyba pripojenia: {e}")
        else:
            st.warning("⚠️ Zadaj názov cviku!")

st.divider()
st.subheader("📊 História tréningov")

try:
    # Načítame dáta s ignorovaním starej pamäte (ttl=0)
    df = pd.read_csv(READ_URL)
    
    if not df.empty:
        # Zobrazíme posledných 15 cvikov, najnovšie navrchu
        st.dataframe(df.tail(15)[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("Tabuľka je zatiaľ prázdna.")
except Exception as e:
    st.info("⌛ História sa pripravuje. Skontroluj, či je tabuľka 'Publikovaná na webe'.")
    # Pre technickú kontrolu (môžeš neskôr odstrániť):
    # st.write(f"Detail chyby: {e}")
