import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gym Progres", layout="centered")

# Prepojenie
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
        
        # Načítanie dát - uisti sa, že v Secrets máš správnu URL v úvodzovkách
        existing_data = conn.read(spreadsheet=st.secrets["gsheets_url"])
        
        # Vytvorenie nového riadku (MUSÍ sa zhodovať so stĺpcami v Google Tabuľke)
        new_row = pd.DataFrame([[dnes, kat, cvik, vaha]], 
                               columns=['Dátum', 'Kategória', 'Cvik', 'Váha'])
        
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # Zápis do Google
        conn.update(spreadsheet=st.secrets["gsheets_url"], data=updated_df)
        st.success("ZAPÍSANÉ DO GOOGLE TABUĽKY! ✅")

st.divider()
st.subheader("📈 História z Google")

try:
    df = conn.read(spreadsheet=st.secrets["gsheets_url"])
    st.dataframe(df.tail(10), use_container_width=True)
except:
    st.info("Zatiaľ žiadne dáta v Google Tabuľke.")
    
