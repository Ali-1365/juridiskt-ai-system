import streamlit as st
import json
from modules.risk_analyzer import total_riskprofil, analysera_argument, analysera_bevis, analysera_process

st.set_page_config(page_title="🎯 Prognos och Risk", layout="wide")
st.title("🎯 Riskanalys och Prognos – Juridiskt AI-stöd")

st.markdown("Ladda upp en JSON-fil eller fyll i data manuellt för att analysera risken i ett juridiskt mål eller inlaga.")

målnummer = st.text_input("📁 Målnummer")
inlaga_id = st.text_input("🗂 Inlaga-ID")

uploaded_file = st.file_uploader("Ladda upp JSON-fil (struktur: argument, bevisning, process)", type=["json"])
data = {}

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        st.success("Filinnehåll inläst!")
    except Exception as e:
        st.error(f"Fel vid inläsning: {e}")

if data:
    st.subheader("🔍 Riskklassificering")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📑 Argument")
        for a in data.get("argument", []):
            poäng = analysera_argument(a)
            st.write(f"• [{a.get('typ')}] – {a.get('viktighet')} → Poäng: {poäng}")

    with col2:
        st.markdown("### 📎 Bevisning")
        for b in data.get("bevisning", []):
            poäng = analysera_bevis(b)
            st.write(f"• [{b.get('typ')}] – {b.get('relevans')}, {b.get('autenticitet')} → Poäng: {poäng}")

    with col3:
        st.markdown("### ⏳ Process")
        poäng = analysera_process(data.get("process", {}))
        st.write(f"Fas: {data['process'].get('fas')} / Risk: {data['process'].get('tidsrisk')} → Poäng: {poäng}")

    st.divider()
    profil = total_riskprofil(data)
    färg = {"Låg": "✅", "Medel": "⚠️", "Hög": "❌"}
    st.markdown(f"## Samlad riskprofil för `{målnummer}` / `{inlaga_id}`: {färg.get(profil, '')} **{profil}**")

else:
    st.info("Ladda upp en JSON-fil för att köra analysen.")
