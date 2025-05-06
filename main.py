import streamlit as st
import os
from datetime import datetime
from utils.auth import check_password
import modules.gpt_assistant as gpt

# Konfigurera sidan
st.set_page_config(
    page_title="Juridiskt AI-system", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kontrollera inloggning
if not check_password():
    st.stop()

# Visa logotyp
logo_path = "assets/logo_placeholder.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=200)

# Huvudrubrik
st.title("⚖️ Juridiskt AI-system")
st.subheader("Intelligenta analyser för juridiska yrkesverksamma")

# Information om systemet
with st.expander("ℹ️ Om systemet", expanded=False):
    st.markdown("""
    ### Systemöversikt
    
    Detta AI-system är utformat för att assistera jurister, domare och juridiska rådgivare med analys, 
    dokumentgenerering och juridiska frågor. Systemet är baserat på OpenAI:s GPT-4o-modell som 
    har specialiserade instruktioner för svensk juridik.
    
    ### Tillgängliga funktioner
    
    - **Juridisk rådgivning**: Ställ juridiska frågor och få välgrundade, faktabaserade svar
    - **Dokumentanalys**: Analysera strukturen i juridiska dokument
    - **Mallgenerering**: Skapa juridiska dokument från mallar
    - **Prejudikatanalys**: Hitta relevanta rättsfall och prejudikat
    
    ### Viktigt att veta
    
    Detta system är ett hjälpmedel och ersätter inte professionell juridisk rådgivning.
    Alla svar ska granskas av behörig jurist innan de används.
    """)

# Huvudinnehåll - enkel introduktion
st.markdown("""
## Välkommen till din juridiska AI-assistent

Välj en funktion i sidomenyn till vänster för att starta. Du har följande alternativ:

1. **📄 Ställ juridisk fråga** - Få svar på juridiska frågor med referenser till lagstiftning
2. **📝 Generera dokument** - Skapa juridiska dokument utifrån mallar
3. **⚖️ Prejudikatanalys** - Identifiera relevanta rättsfall och prejudikat
4. **🔍 Analysera dokument** - Strukturera och analysera juridiska dokument
5. **⚙️ Systeminställningar** - Anpassa systemet efter dina behov
""")

# Visa tillgängliga AI-modeller
with st.expander("🧠 AI-modeller", expanded=False):
    st.subheader("Tillgängliga AI-modeller")
    models = gpt.get_available_models()
    for model in models:
        st.markdown(f"- **{model}**")
    
    st.info("GPT-4o rekommenderas för bästa resultat i komplexa juridiska frågor.")

# Statusrad längst ner med systemversion och datum
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.caption("Juridiskt AI-system v1.0.0")
with col2:
    st.caption(f"Datum: {datetime.now().strftime('%Y-%m-%d')}")