import streamlit as st

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- TVOJA ADRESA TABUĽKY ---
URL_TABULKY = "https://docs.google.com/spreadsheets/d/1K81RIVLwfOKGap8d-1_ERDJvo8CBTWVTDsQZKMOFq8/edit"

st.title("🏋️ Gym Progres - História tréningov")

# --- HLAVNá ČASŤ ---
st.info("Aplikácia slúži na rýchly a stabilný prístup k tvojej tréningovej histórii.")

st.subheader("Prehľad záznamov")
st.write("Kliknutím na tlačidlo nižšie otvoriš kompletnú tabuľku so všetkými zápismi:")

# Veľké, prehľadné tlačidlo pre mobil aj PC
st.markdown(f'<a href="{URL_TABULKY}" target="_blank" style="text-decoration:none;"><button style="padding:14px 28px; cursor:pointer; background-color:#4CAF50; color:white; border:none; border-radius:5px; font-weight:bold; font-size:16px;">OTVORIŤ HISTÓRIU TRÉNINGOV</button></a>', unsafe_allow_html=True)

st.divider()
st.success("Tento prístup je plne stabilný a obchádza akékoľvek chyby pri načítavaní.")
