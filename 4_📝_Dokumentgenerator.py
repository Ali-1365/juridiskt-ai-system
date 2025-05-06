import streamlit as st
from modules.doc_strategy_optimizer import skapa_word_dokument, skapa_pdf_via_weasyprint, generera_html_version
import os
import json
import tempfile

st.set_page_config(page_title="📝 Dokumentgenerator", layout="wide")
st.title("📝 Dokumentgenerator – AI-styrd dokumentproduktion")

# 📁 Läs tillgängliga målmappar
målrot = "./mål"
målmappar = [m for m in os.listdir(målrot) if os.path.isdir(os.path.join(målrot, m))]

mål_id = st.selectbox("📁 Välj mål (från ./mål/)", målmappar)

# Förifyll strategidata via JSON
strategidata = {"riskprofil": "ok", "prejudikat": "låg"}
dokstatus = {"status": "saknas", "bevis": "saknas"}

if mål_id:
    sökväg = os.path.join(målrot, mål_id)
    try:
        with open(os.path.join(sökväg, "risk.json"), "r", encoding="utf-8") as f:
            strategidata["riskprofil"] = json.load(f).get("profil", "ok")
        with open(os.path.join(sökväg, "prejudikat.json"), "r", encoding="utf-8") as f:
            strategidata["prejudikat"] = json.load(f).get("läge", "låg")
        with open(os.path.join(sökväg, "dok_status.json"), "r", encoding="utf-8") as f:
            dokstatus = json.load(f)
    except:
        st.warning("⚠️ Kunde inte läsa JSON-filer i målmappar.")

titel = st.text_input("🧾 Dokumenttitel", f"Yttrande för mål {mål_id}")

st.markdown(f"### 📉 Riskprofil: **{strategidata['riskprofil']}**")
st.markdown(f"### ⚖️ Prejudikatläge: **{strategidata['prejudikat']}**")
st.markdown(f"### 📄 Dokumentstatus: **{dokstatus.get('status', 'ok')}**")
st.markdown(f"### 🧾 Bevisstatus: **{dokstatus.get('bevis', 'ok')}**")

st.markdown("## ✍️ Skriv innehåll (punktvis):")
punkttext = st.text_area("Ange varje punkt på ny rad", height=200)
punkter = [p.strip() for p in punkttext.split("\n") if p.strip()]

st.markdown("## 📎 Bilageindex")
bilagor = []
antal = st.number_input("Hur många bilagor vill du inkludera?", 0, 20, 0)
for i in range(antal):
    namn = st.text_input(f"Bilaga {i+1} – namn", key=f"namn_{i}")
    beskrivning = st.text_input(f"Bilaga {i+1} – beskrivning", key=f"beskrivning_{i}")
    if namn and beskrivning:
        bilagor.append({"namn": namn, "beskrivning": beskrivning})

if st.button("📤 Generera Word och PDF"):
    with tempfile.TemporaryDirectory() as tmpdir:
        word_path = os.path.join(tmpdir, "dokument.docx")
        skapa_word_dokument(titel, punkter, strategidata, bilagor, word_path)
        html_str = generera_html_version(titel, punkter, strategidata, bilagor)
        pdf_path = os.path.join(tmpdir, "dokument.pdf")
        skapa_pdf_via_weasyprint(html_str, pdf_path)

        st.success("✅ Dokument genererade!")
        with open(word_path, "rb") as f:
            st.download_button("📥 Ladda ned Word (.docx)", f, file_name=f"{mål_id}_strategi.docx")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Ladda ned PDF", f, file_name=f"{mål_id}_strategi.pdf")
