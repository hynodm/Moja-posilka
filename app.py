
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Nastavenie vzhľadu
st.set_page_config(page_title="Gym Progres", layout="centered")

# Prepojenie na Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏋️‍♂️ Môj Gym Progres")

kat = st.radio("Čo dnes cvičíš?", ["Ruky a Nohy", "Ostatné"], horizontal=True)

with st.form("zapis_form", clear_on_submit=True):
    cvik = st.text_input("Názov cviku")
    col1, col2 = st.columns(2)
    vaha = col1.number_input("Váha (kg)", min_value=0.0, step=2.5)
    opak = col2.number_input("Opakovania", min_value=1, step=1)
    
    if st.form_submit_button("Uložiť výkon"):
        dnes = datetime.now().strftime("%d.%m.%Y")
        
        # Načítanie existujúcich dát z Google tabuľky
        existing_data = conn.read(spreadsheet=st.secrets["gsheets_url"])
        
        # Pridanie nového tréningu
        new_row = pd.DataFrame([[dnes, kat, cvik, vaha, opak]], 
                               columns=['Dátum', 'Kategória', 'Cvik', 'Váha', 'Opakovania'])
        
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # Zápis späť do Google Sheets
        conn.update(spreadsheet=st.secrets["gsheets_url"], data=updated_df)
        st.success("Zapísané do Google Tabuliek!")

st.divider()
st.subheader("📈 Tvoj pokrok")

# Zobrazenie histórie z Google Sheets
try:
    df = conn.read(spreadsheet=st.secrets["gsheets_url"])
    if not df.empty:
        f_df = df[df['Kategória'] == kat]
        st.dataframe(f_df.tail(15), use_container_width=True)
except:
    st.info("Zatiaľ tu nie sú žiadne dáta. Zapíš svoj prvý cvik!")
