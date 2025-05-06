import streamlit as st
import os
import json

st.set_page_config(page_title="📊 Strategiöversikt", layout="wide")
st.title("📊 Strategiöversikt – AI-sammanvägning & manuell styrning")

målrot = "./mål"
målmappar = [m for m in os.listdir(målrot) if os.path.isdir(os.path.join(målrot, m))]

åtgärdsalternativ = [
    "Ingen åtgärd",
    "Komplettera bevis",
    "Sök inhibition",
    "Formulera invändning",
    "Begär föreläggandeförlängning"
]

def läs_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def spara_strategi(mål_id, kommentar, åtgärd):
    path = os.path.join(målrot, mål_id, "strategi.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"kommentar": kommentar, "åtgärd": åtgärd}, f, indent=2, ensure_ascii=False)

st.markdown("## 📁 Alla mål – status, flaggor och strategi")
for mål_id in målmappar:
    st.markdown(f"---\n### 🗂️ Mål: **{mål_id}**")

    data_risk = läs_json(os.path.join(målrot, mål_id, "risk.json"))
    data_prej = läs_json(os.path.join(målrot, mål_id, "prejudikat.json"))
    data_dok = läs_json(os.path.join(målrot, mål_id, "dok_status.json"))
    data_strat = läs_json(os.path.join(målrot, mål_id, "strategi.json"))

    # AI-baserad färg
    ai_status = "🟢 Stabil"
    if data_risk.get("profil") == "Hög" or data_dok.get("status") == "saknas":
        ai_status = "🟡 Medelrisk"
    if data_risk.get("profil") == "Hög" and data_dok.get("status") == "saknas":
        ai_status = "🔴 Kritisk"

    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    col1.markdown(f"**📉 Risk:** {data_risk.get('profil','-')}")
    col2.markdown(f"**⚖️ Prejudikat:** {data_prej.get('läge','-')}")
    col3.markdown(f"**📄 Dokstatus:** {data_dok.get('status','-')}")
    col4.markdown(f"**🧠 AI-status:** {ai_status}")

    kommentar = st.text_area("✍️ Kommentar", value=data_strat.get("kommentar", ""), key=f"k_{mål_id}")
    åtgärd = st.selectbox("📌 Åtgärd", åtgärdsalternativ, index=åtgärdsalternativ.index(data_strat.get("åtgärd", "Ingen åtgärd")), key=f"a_{mål_id}")

    if st.button(f"💾 Spara strategi för {mål_id}"):
        spara_strategi(mål_id, kommentar, åtgärd)
        st.success("✅ Sparat.")

    st.markdown(f"🔗 [Öppna dokumentgenerator för {mål_id}](4_📝_Dokumentgenerator)")

