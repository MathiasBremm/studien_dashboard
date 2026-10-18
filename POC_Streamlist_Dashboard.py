import pandas as pd
import streamlit as st

st.title("PoC: Studien-Dashboard")

# 1. Haupt-Metriken & Fortschritt
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Notendurchschnitt", value="1.8", delta="-0.1")
with col2:
    st.metric(label="Notentendenz (3 M.)", value="2.0")

st.caption("ECTS-Fortschritt (90 / 180 ECTS)")
st.progress(90 / 180)

# 2. Tabellarische Moduldarstellung
st.subheader("Modulübersicht")
poc_data = {
    "Modulcode": ["DLBDSOOFPP01", "DLBCITSA01"],
    "Modulname": [
        "Objektorientierte Programmierung mit Python",
        "IT-Sicherheit Architektur",
    ],
    "ECTS": [5, 5],
    "Status": ["BESTANDEN", "IN_BEARBEITUNG"],
    "Note": [1.9, None],
}

st.dataframe(pd.DataFrame(poc_data), hide_index=True)