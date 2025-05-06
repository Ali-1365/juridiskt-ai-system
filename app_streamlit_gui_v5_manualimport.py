import streamlit as st

from modules import (
    pdf_parser,
    structure_analyzer,
    basic_fault_detector,
    evidence_analyzer,
    advanced_fault_detector,
    argumentation_analyzer,
    response_analyzer,
    contract_checker,
    strategy_module,
    verification_module,
    gpt_assistant,
    precedent_matcher,
    outcome_predictor,
    template_generator
)

st.set_page_config(page_title="Juridisk AI V1–V4", layout="wide")
st.title("⚖️ Juridisk AI – V1 till V4")

flik = st.sidebar.selectbox("📂 Välj funktion", [
    "📁 Målval & metadata",
    "📄 PDF-analys (V1)",
    "🧠 Djupanalys (V2)",
    "🧩 Strategimodul (V3)",
    "📌 Föreläggandesvar",
    "🧠 GPT-rådgivare",
    "🔍 Rättsfallssökning (V4)",
    "🎯 Prognosmodul (V4)",
    "📄 Mallgenerator (V4)"
])

if flik == "📁 Målval & metadata":
    st.subheader("📁 Hantera mål")
    st.info("Här kan du skapa, ladda och visa metadata för varje mål. (Integreras med målhanterare)")

elif flik == "📄 PDF-analys (V1)":
    st.subheader("📄 Ladda PDF och analysera")
    uploaded_file = st.file_uploader("Ladda upp PDF", type=["pdf"])
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
        st.text_area("Extraherad text", text, height=300)
        st.markdown("### 📌 Strukturanalys")
        st.json({"struktur": structure_analyzer.__doc__})
        st.markdown("### ⚠️ Formaliafel")
        st.json({"formalia": basic_fault_detector.__doc__})

elif flik == "🧠 Djupanalys (V2)":
    st.subheader("🧠 Juridisk djupanalys")
    text = st.text_area("Klistra in text för analys", height=300)
    if st.button("Analysera"):
        st.markdown("### 📚 Bevisanalys")
        st.write(evidence_analyzer.__doc__)
        st.markdown("### ⚖️ Felbedömning")
        st.write(advanced_fault_detector.__doc__)
        st.markdown("### 💬 Argumentanalys")
        st.write(argumentation_analyzer.__doc__)
        st.markdown("### 🔄 Bemötandeanalys")
        st.write(response_analyzer.__doc__)

elif flik == "🧩 Strategimodul (V3)":
    st.subheader("🧩 AI-strategi för process")
    st.write(strategy_module.__doc__)
    st.markdown("### 📜 Avtalsgranskning")
    st.write(contract_checker.__doc__)

elif flik == "📌 Föreläggandesvar":
    st.subheader("📌 Generera föreläggandesvar")
    target = st.text_input("Mottagare (ex. Förvaltningsrätten)")
    deadline = st.date_input("Svar senast")
    if st.button("Generera svar"):
        st.success("Modulen är aktiverad – funktionalitet byggs ut i nästa steg.")

elif flik == "🧠 GPT-rådgivare":
    st.subheader("🧠 Fråga GPT om beslut, JO-anmälan eller lagtolkning")
    user_input = st.text_area("Skriv din fråga eller klistra in beslut", height=300)
    model = st.selectbox("Välj modell", ["gpt-4", "gpt-3.5-turbo"])
    if st.button("Analysera med GPT"):
        svar = gpt_assistant.query_gpt(user_input, model=model)
        st.markdown("### 🧾 Svar:")
        st.write(svar)

elif flik == "🔍 Rättsfallssökning (V4)":
    st.subheader("🔍 Rättsfallsdetektor – HFD, NJA m.m.")
    query = st.text_input("Ange rättsfråga eller nyckelord")
    if st.button("Sök rättsfall"):
        träffar = precedent_matcher.match_precedents(query)
        st.write(träffar)

elif flik == "🎯 Prognosmodul (V4)":
    st.subheader("🎯 Utfallsprognos")
    text = st.text_area("Klistra in beslut eller text", height=250)
    if st.button("Gör prognos"):
        resultat = outcome_predictor.predict_outcome(text)
        st.json(resultat)

elif flik == "📄 Mallgenerator (V4)":
    st.subheader("📄 Generera dokumentmall (Markdown)")
    typ = st.selectbox("Typ av dokument", ["överklagande"])
    namn = st.text_input("Ditt namn")
    datum = st.text_input("Datum för beslut")
    lagrum = st.text_input("Lagrum")
    grund = st.text_input("Skäl för överklagande")
    if st.button("Skapa mall"):
        data = {"namn": namn, "datum": datum, "lagrum": lagrum, "grund": grund}
        mall = template_generator.generate_template(typ, data)
        st.code(mall, language="markdown")

elif flik == "📄 Mallgenerator (V4)":
    st.subheader("📄 Generera dokumentmall (Markdown & DOCX)")
    typ = st.selectbox("Typ av dokument", ["överklagande"])
    namn = st.text_input("Ditt namn")
    datum = st.text_input("Datum för beslut")
    lagrum = st.text_input("Lagrum")
    grund = st.text_input("Skäl för överklagande")
    myndighet = st.text_input("Beslutsmyndighet")
    mottagare = st.text_input("Mottagare (ex. Förvaltningsrätten)")

    if st.button("Skapa mall"):
        data = {
            "namn": namn, "datum": datum, "lagrum": lagrum,
            "grund": grund, "beslutsmyndighet": myndighet,
            "mottagare": mottagare
        }
        mall = template_generator.generate_template(typ, data)
        st.code(mall, language="markdown")

    if st.button("Exportera som DOCX"):
        from template_generator_docx import generate_docx
        filepath = generate_docx(data, template_type=typ, filename="utkast.docx")
        st.success("DOCX skapat!")
        st.download_button("Ladda ned DOCX", data=open(filepath, "rb"), file_name="utkast.docx")

elif flik == "☁️ Manuell import":
    st.subheader("☁️ Manuell filuppladdning och AI-sortering")

    uploaded_file = st.file_uploader("Ladda upp PDF eller DOCX för AI-klassificering", type=["pdf", "docx"])
    if uploaded_file:
        file_ext = uploaded_file.name.split(".")[-1]
        tmp_path = f"/mnt/data/{uploaded_file.name}"
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extrahera text
        if file_ext == "pdf":
            from text_extractor import extract_text_from_pdf
            text = extract_text_from_pdf(tmp_path)
        elif file_ext == "docx":
            from text_extractor import extract_text_from_docx
            text = extract_text_from_docx(tmp_path)
        else:
            st.error("Filtyp ej stödd.")
            st.stop()

        # Klassificera mål
        from målklassificerare import klassificera_mål
        kända_mål = ["T1456-23", "Ö2152-25", "T2694-24"]
        klassificerat_mål = klassificera_mål(text, kända_mål)

        # Visa förhandsgranskning
        st.markdown("### 📄 Textutdrag")
        st.text(text[:1500])  # Visa första delen

        st.markdown("### 🧠 AI-förslag på mål:")
        if klassificerat_mål != "oklart":
            st.success(f"Föreslaget mål: {klassificerat_mål}")
            godkänn = st.checkbox("✔️ Jag godkänner att filen sparas i målmapp")
            if godkänn and st.button("Spara fil"):
                import os
                mål_path = f"./mål/{klassificerat_mål}/"
                os.makedirs(mål_path, exist_ok=True)
                dest = os.path.join(mål_path, uploaded_file.name)
                os.rename(tmp_path, dest)
                st.success(f"Filen sparades i {mål_path}")
        else:
            st.warning("Kunde inte avgöra vilket mål filen tillhör. Vänligen kontrollera manuellt.")
