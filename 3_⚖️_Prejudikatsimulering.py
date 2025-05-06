import streamlit as st
import json
from modules.precedent_simulator import simulera_prejudikat

st.set_page_config(page_title="⚖️ Prejudikatsimulering", layout="wide")
st.title("⚖️ Prejudikatsimulering – AI-stöd för rättsutveckling")

st.markdown("Analysera om din rättsfråga kan bli prejudikat. Ladda upp en JSON-fil eller fyll i data manuellt.")

col1, col2 = st.columns(2)
with col1:
    domstol = st.text_input("Domstol (t.ex. Högsta domstolen)")
    rättsområde = st.text_input("Rättsområde (civilrätt, förvaltningsrätt...)")
with col2:
    rättsfråga = st.text_input("Rättsfråga (t.ex. avtalsbrott, sjukpenning)")

uploaded_file = st.file_uploader("📄 Ladda upp JSON-fil för simulering", type=["json"])
data = {}

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        st.success("JSON inläst.")
    except Exception as e:
        st.error(f"Kunde inte läsa fil: {e}")

elif rättsfråga and rättsområde:
    data = {
        "domstol": domstol,
        "rättsområde": rättsområde,
        "rättsfråga": rättsfråga,
        "argument": "Manuell inmatning"
    }

if data:
    st.markdown("## 🧠 Simulerat utfall")
    resultat = simulera_prejudikat(data)

    st.markdown(f"### 🧩 Prejudikatrisk: **{resultat['prejudikatrisk'].upper()}**")
    st.markdown(f"🧾 **Simulerad tolkning:** {resultat['simulerat_uttryck']}")

    if resultat['träffade_prejudikat']:
        st.markdown("### 📚 Matchade prejudikat:")
        for p in resultat['träffade_prejudikat']:
            st.markdown(f"- **{p['id']}** – {p['avgörande']} ({p['tolkning']})")
    else:
        st.warning("Inga direkta prejudikat identifierades.")
else:
    st.info("Fyll i formulär eller ladda upp en fil för att simulera.")
