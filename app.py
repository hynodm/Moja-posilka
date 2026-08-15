import streamlit as st

st.set_page_config(page_title="Gym Progres", page_icon="🏋️")

st.title("🏋️ Gym Progres")

st.info("Vyberte akciu:")

# Použijeme natívne tlačidlá Streamlit, ktoré sa správajú v mobiloch lepšie
if st.link_button("📝 OTVORIŤ FORMULÁR", "https://docs.google.com/forms/d/e/1FAIpQLSe_bSMHDGEvmPZUP4ZBQ2nq-Yos_3OZww5jLe9ZKzjgQk4W0A/viewform"):
    pass

if st.link_button("📊 OTVORIŤ TABUĽKU", "https://docs.google.com/spreadsheets/d/1K81RIVLwfOKGap8d-1_ERDJvo8CBTWVTDsQZKMOFq8/edit"):
    pass

st.divider()
st.write("Ak sa tabuľka neotvorí, prosím, otvorte ju manuálne priamo v aplikácii Google Tabuľky vo svojom telefóne.")
