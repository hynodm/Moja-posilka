import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- 2. KONFIGURÁCIA GOOGLE FORMULÁRA ---
# Adresa pre odosielanie dát do formulára
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/formResponse"

# Mapovanie ID políčok z tvojho formulára
ENTRY_DATUM = "entry.1160346068"
ENTRY_KATEGORIA = "entry.312830153"
ENTRY_CVIK = "entry.83240949"
ENTRY_VAHA = "entry.1078103613"
ENTRY_OPAK = "entry.166466953"

# Odkaz na CSV pre načítanie histórie (pôvodný)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLiDDAemHUDJrBs4brpOvaMqO_Bzbn3pkMhq64HFU_1QJqRMbGVeKpx66m01aH_02pG3Nsc3j-4f51/pub?output=csv"

st.title("🏋️ Môj Gym Progres")

# --- 3. FORMULÁR PRE ZÁPIS ---
kat = st.radio("Vyber kategóriu", ["Ostatné", "Ruky a nohy"], horizontal=True)

with st.form("gym_zapis", clear_on_submit=True):
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        cvik_input = st.text_input("Názov cviku")
    with col_b:
        vaha_input = st.number_input("Váha (kg)", min_value=0.0, step=0.5)
    with col_c:
        opak_input = st.number_input("Opakovania", min_value=0, step=1)
        
    submit = st.form_submit_button("ZÁPISAŤ DO TABUĽKY")

if submit:
    if not cvik_input.strip():
        st.warning("⚠️ Vyplň názov cviku!")
    else:
        dnes = datetime.now().strftime("%Y-%m-%d")
        
        # Dáta v štruktúre pre Google Formulár
        form_data = {
            ENTRY_DATUM: dnes,
            ENTRY_KATEGORIA: kat,
            ENTRY_CVIK: cvik_input.strip(),
            ENTRY_VAHA: str(vaha_input),
            ENTRY_OPAK: str(opak_input)
        }
        
        try:
            res = requests.post(FORM_URL, data=form_data)
            if res.status_code == 200:
                st.success(f"✅ Uložené: {cvik_input} - {vaha_input} kg x {opak_input}")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Chyba servera: {res.status_code}")
        except Exception as e:
            st.error(f"Chyba spojenia: {e}")

st.divider()

# --- 4. ZOZNAM A HISTÓRIA CVIKOV ---
def vykresli_historiu(df, nadpis):
    st.subheader(nadpis)
    
    cviky = sorted(df['Cvik'].dropna().unique())
    vybrany_cvik = st.selectbox(f"Vyber cvik ({nadpis})", cviky, key=f"sel_{nadpis}")
    
    if vybrany_cvik:
        df_cvik = df[df['Cvik'] == vybrany_cvik].copy()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("📋 **Míľniky (Max Váha):**")
            max_vahy = df_cvik.groupby('Váha')['Dátum'].min().reset_index()
            max_vahy = max_vahy.sort_values(by='Váha', ascending=False)
            st.dataframe(max_vahy, hide_index=True, use_container_width=True)
            
        with col2:
            st.write("📈 **Progres váhy v čase:**")
            chart_data = df_cvik.groupby('Dátum')['Váha'].max().reset_index()
            st.line_chart(chart_data, x='Dátum', y='Váha')
            
        st.write("📜 **Kompletná história cviku:**")
        st.dataframe(df_cvik[['Dátum', 'Váha', 'Opakovanie']].sort_values(by='Dátum', ascending=False), hide_index=True, use_container_width=True)

try:
    data = pd.read_csv(CSV_URL)
    data.columns = [c.strip() for c in data.columns]
    
    # Filtrovanie kategórií
    df_ruky_nohy = data[data['Kategória'] == 'Ruky a nohy']
    df_ostatne = data[data['Kategória'] != 'Ruky a nohy']
    
    tab1, tab2 = st.tabs(["💪 Ruky a nohy", "🥊 Ostatné"])
    
    with tab1:
        if not df_ruky_nohy.empty:
            vykresli_historiu(df_ruky_nohy, "Ruky a nohy")
        else:
            st.info("Žiadne dáta v kategórii Ruky a nohy.")
            
    with tab2:
        if not df_ostatne.empty:
            vykresli_historiu(df_ostatne, "Ostatné")
        else:
            st.info("Žiadne dáta v kategórii Ostatné.")

except Exception as e:
    st.error(f"Nepodarilo sa načítať históriu z Google Tabuľky: {e}")
