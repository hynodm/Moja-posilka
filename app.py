import streamlit as st

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="Gym Progres", layout="wide", page_icon="🏋️")

# --- TVOJE ADRESY ---
URL_FORMULARA = "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/viewform"
URL_TABULKY = "https://docs.google.com/spreadsheets/d/1K81RIVLwfOKGap8d-1_ERDJvo8CBTWVTDsQZKMOFq8/edit"

st.title("🏋️ Gym Progres - Stabilný prístup")

# --- HLAVNÁ ČASŤ ---
st.info("Aplikácia je pripravená. Zápis prebieha cez oficiálny formulár a históriu si môžeš kedykoľvek otvoriť v tabuľke.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Zápis tréningu")
    st.write("Kliknutím na tlačidlo otvoríš formulár pre nový záznam:")
    st.markdown(f'<a href="{URL_FORMULARA}" target="_blank" style="text-decoration:none;"><button style="padding:12px 24px; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px; font-weight:bold; font-size:16px;">OTVORIŤ FORMULÁR</button></a>', unsafe_allow_html=True)

with col2:
    st.subheader("História tréningov")
    st.write("Kompletná tabuľka so všetkými zápismi:")
    st.markdown(f'<a href="{URL_TABULKY}" target="_blank" style="text-decoration:none;"><button style="padding:12px 24px; cursor:pointer; background-color:#4CAF50; color:white; border:none; border-radius:5px; font-weight:bold; font-size:16px;">OTVORIŤ TABUĽKU</button></a>', unsafe_allow_html=True)

st.divider()
st.success("Tento prístup je plne stabilný. Žiadne blokovania od Googlu, žiadne chyby pri načítavaní.")
