
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="🧭 AI-Kontrollpanel", layout="wide")
st.title("🧭 Juridisk AI – Kontrollpanel")

mål_dir = "mål"
if not os.path.isdir(mål_dir):
    st.warning("Ingen målmapp hittades.")
else:
    målmappar = [d for d in os.listdir(mål_dir) if os.path.isdir(os.path.join(mål_dir, d))]
    if not målmappar:
        st.info("Inga registrerade mål.")
    else:
        for mål_id in målmappar:
            base = os.path.join(mål_dir, mål_id)
            try:
                with open(os.path.join(base, "risk.json")) as f: risk = json.load(f)["profil"]
                with open(os.path.join(base, "prejudikat.json")) as f: prejudikat = json.load(f)["läge"]
                with open(os.path.join(base, "dok_status.json")) as f: dok = json.load(f)["status"]
                proc = {}
                try:
                    with open(os.path.join(base, "process.json")) as f:
                        proc = json.load(f)
                except:
                    pass
                kommentar = proc.get("kommentar", "")
                åtgärd = proc.get("åtgärd", "")
                kommun = proc.get("senaste_kommunikation", "")
                deadline = proc.get("senast_inlämning", "")
                handl = proc.get("handläggare", "")

                # Bedöm flaggnivå
                idag = datetime.now().date()
                dl_date = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
                deadline_flag = dl_date and (dl_date - idag).days <= 2
                high_risk = risk == "Hög"
                # Välj bakgrund
                if high_risk and deadline_flag:
                    bg = "background-color: #f8d7da"  # rött
                elif high_risk or deadline_flag:
                    bg = "background-color: #fff3cd"  # gult
                else:
                    bg = "background-color: #d4edda"  # grönt

                # Visa rad
                with st.container():
                    st.markdown(f"<div style='{bg}; padding:10px; border-radius:5px'>", unsafe_allow_html=True)
                    cols = st.columns([2,2,2,2,1])
                    cols[0].markdown(f"**{mål_id}**")
                    cols[1].markdown(f"Risk: {risk} {'🔴' if high_risk else '🟢'}")
                    cols[2].markdown(f"Prejudikat: {prejudikat}")
                    cols[3].markdown(f"Deadline: {deadline} {'⏰' if deadline_flag else ''}")
                    # Detaljer-knapp
                    if cols[4].button("Visa detaljer", key=mål_id):
                        with st.expander("Detaljer för " + mål_id, expanded=True):
                            st.markdown(f"- **Kommentar:** {kommentar or '–'}")
                            st.markdown(f"- **Åtgärd:** {åtgärd or '–'}")
                            st.markdown(f"- **Senaste kommunikation:** {kommun or '–'}")
                            st.markdown(f"- **Handläggare:** {handl or '–'}")
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                continue
