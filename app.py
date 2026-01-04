import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gym Progres", layout="centered", page_icon="🏋️‍♂️")

# Tvoja najnovšia adresa, ktorá ti v prehliadači fungovala
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzfu0UnPyfyVgCwYB0O4Qthf59UC-v9_Ykjsk3B2NxlwyHt21oOZVwJjITiw0sGfVFc/exec"

SHEET_ID = "1K81rRIVLwfOKGap8d-1_ERdJVo8CBTWVTdSZKMOFq8"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_zapis", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    vaha = st.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = st.number_input("Opakovania", min_value=1, step=1)
    
    # ZMENENÉ TLAČIDLO (na kontrolu aktualizácie)
    if st.form_submit_button("ZAPÍSAŤ TERAZ"):
        if cvik:
            try:
                params = {"kat": kat, "cvik": cvik, "vaha": str(vaha), "opak": str(opak)}
                res = requests.get(WEB_APP_URL, params=params, timeout=10)
                if "Success" in res.text:
                    st.success("✅ Úspešne zapísané!")
                    st.balloons()
                else:
                    st.error(f"❌ Server vrátil: {res.text}")
            except Exception as e:
                st.error(f"❌ Chyba pripojenia: {e}")
        else:
            st.warning("⚠️ Zadaj názov cviku!")

st.divider()
try:
    df = pd.read_csv(READ_URL)
    if not df.empty:
        st.dataframe(df.tail(10)[::-1], use_container_width=True)
except:
    st.info("⌛ História sa načíta po úspešnom zápise.")
