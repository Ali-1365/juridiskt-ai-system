import streamlit as st
import json
import os

st.set_page_config(page_title="📊 Strategikarta", layout="wide")
st.title("📊 Strategikarta – AI-kopplad målanalys")

def färgklass(status):
    return {
        "Låg": "🟢",
        "Medel": "🟡",
        "Hög": "🔴",
        "möjlig": "🟡",
        "hög": "🔴",
        "ok": "🟢",
        "under arbete": "🟡",
        "saknas": "🔴"
    }.get(status, "⚪")

@st.cache_data
def läs_json(filväg):
    try:
        with open(filväg, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 📁 Hämta alla mappar i ./mål/
målrot = "./mål"
if not os.path.exists(målrot):
    st.warning("Målmapp saknas – skapa mappstrukturen './mål/Txxxx/' med JSON-filer.")
    st.stop()

målmappar = [m for m in os.listdir(målrot) if os.path.isdir(os.path.join(målrot, m))]

tabell_data = []
for mål in målmappar:
    sökväg = os.path.join(målrot, mål)
    riskdata = läs_json(os.path.join(sökväg, "risk.json"))
    prejudikatdata = läs_json(os.path.join(sökväg, "prejudikat.json"))
    dokstatus = läs_json(os.path.join(sökväg, "dok_status.json"))

    risk = riskdata.get("profil", "ok")
    prejudikat = prejudikatdata.get("läge", "låg")
    dokument = dokstatus.get("status", "saknas")
    bevis = dokstatus.get("bevis", "under arbete")

    kritisk = "⚠️" if risk == "Hög" and dokument == "saknas" else ""

    tabell_data.append({
        "Mål": f"**{mål}** {kritisk}",
        "📉 Riskprofil": f"{färgklass(risk)} {risk}",
        "⚖️ Prejudikatläge": f"{färgklass(prejudikat)} {prejudikat}",
        "🧾 Bevisstatus": f"{färgklass(bevis)} {bevis}",
        "📄 Dokumentstatus": f"{färgklass(dokument)} {dokument}"
    })

st.markdown("## 🔍 Översikt över strategiska indikatorer per mål")
st.dataframe(tabell_data, use_container_width=True)
