import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="centered")

FILE = 'treningy.csv'

if not os.path.exists(FILE):
    pd.DataFrame(columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania']).to_csv(FILE, index=False)

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    c1, c2 = st.columns(2)
    vaha = c1.number_input("Váha (kg)", step=2.5)
    opak = c2.number_input("Opakovania", step=1, min_value=1)
    
    if st.form_submit_button("Uložiť"):
        dnes = datetime.now().strftime("%d.%m.%Y")
        novy = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
        novy.to_csv(FILE, mode='a', header=False, index=False)
        st.success("Zapísané!")

st.divider()
df = pd.read_csv(FILE)
if not df.empty:
    st.subheader(f"História: {kat}")
    f_df = df[df['Kategória'] == kat]
    st.dataframe(f_df.tail(10), use_container_width=True)
  
