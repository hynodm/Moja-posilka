
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nastavenie aplikácie
st.set_page_config(page_title="Gym Progres", layout="centered")

FILE = 'treningy.csv'

# Ak súbor neexistuje, vytvoríme ho
if not os.path.exists(FILE):
    pd.DataFrame(columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania']).to_csv(FILE, index=False)

st.title("🏋️‍♂️ Môj Gym Progres")

# Výber kategórie
kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

# Formulár na zápis
with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        dnes = datetime.now().strftime("%d.%m.%Y")
        novy_riadok = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], 
                                   columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
        novy_riadok.to_csv(FILE, mode='a', header=False, index=False)
        st.success("Zapísané!")

st.divider()
st.subheader("📈 Tvoj progres")

# Zobrazenie histórie
df = pd.read_csv(FILE)
if not df.empty:
    filtered_df = df[df['Kategória'] == kat]
    st.write(f"Posledné tréningy ({kat}):")
    st.dataframe(filtered_df.tail(10), use_container_width=True)
