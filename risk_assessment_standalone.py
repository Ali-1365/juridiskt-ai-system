import streamlit as st
import os
from openai import OpenAI

# Import needed functions
from app.utils.pdf.extractor import validate_pdf, extract_text_from_pdf
from app.utils.pdf.analyzer import assess_case_risk

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Set page title
st.set_page_config(
    page_title="Riskbedömning av juridiska dokument",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title("Riskbedömning av juridiska dokument")

st.markdown("""
### Standalone-version av riskbedömningsfunktionen

Denna applikation ger dig möjlighet att ladda upp ett juridiskt dokument för att få 
en AI-driven riskbedömning och prognos för utgången i målet.
""")

# Legal area selection
risk_legal_area = st.selectbox(
    "Juridiskt område",
    ["Allmänt", "Avtalsrätt", "Skadeståndsrätt", "Fastighetsrätt", "Familjerätt", "Straffrätt", "Processrätt"],
    key="risk_legal_area"
)

# File upload section
risk_uploaded_file = st.file_uploader("Ladda upp PDF för riskbedömning", type="pdf", key="risk_pdf")

if risk_uploaded_file is not None:
    try:
        with st.spinner("Analyserar dokument för riskbedömning..."):
            # Validate PDF
            is_valid, error_msg = validate_pdf(risk_uploaded_file)
            
            if not is_valid:
                st.error(f"Ogiltig PDF: {error_msg}")
            else:
                # Extract text
                all_text, pages_text = extract_text_from_pdf(risk_uploaded_file)
                
                if not all_text:
                    st.warning("Kunde inte extrahera text från PDF-filen. Kontrollera att filen innehåller text och inte bara bilder.")
                else:
                    # Show extracted text in collapsible section
                    with st.expander("Visa extraherad text", expanded=False):
                        st.write(all_text[:3000] + ("..." if len(all_text) > 3000 else ""))
                    
                    # Perform risk assessment
                    with st.spinner("Utför riskbedömning och prognos..."):
                        risk_result = assess_case_risk(all_text, risk_legal_area)
                    
                    # Display risk assessment results
                    st.subheader("Riskbedömning och prognos för utfall")
                    
                    # Display success probability as a gauge
                    success_prob = risk_result.get("success_probability", 0.5)
                    success_percent = int(success_prob * 100)
                    
                    # Use columns for better layout
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Create a visual gauge for success probability
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <h4>Sannolikhet för framgång</h4>
                            <div style="font-size: 3rem; font-weight: bold; color: {'green' if success_percent > 66 else 'orange' if success_percent > 33 else 'red'};">
                                {success_percent}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a simple progress bar
                        st.progress(success_prob)
                        
                        # Risk level text
                        risk_level = "Låg" if success_percent > 66 else "Medel" if success_percent > 33 else "Hög"
                        st.markdown(f"<div style='text-align: center;'><b>Risknivå:</b> {risk_level}</div>", unsafe_allow_html=True)
                    
                    with col2:
                        # Show explanation
                        st.markdown("#### Bedömningsförklaring")
                        st.write(risk_result.get("explanation", "Ingen förklaring tillgänglig"))
                    
                    # Show risk factors
                    st.markdown("#### Identifierade riskfaktorer")
                    risk_factors = risk_result.get("risk_factors", [])
                    if risk_factors:
                        for factor in risk_factors:
                            st.markdown(f"- {factor}")
                    else:
                        st.write("Inga specifika riskfaktorer identifierade")
                    
                    # Show recommendations
                    st.markdown("#### Rekommendationer")
                    recommendations = risk_result.get("recommendations", [])
                    if recommendations:
                        for rec in recommendations:
                            st.markdown(f"- {rec}")
                    else:
                        st.write("Inga specifika rekommendationer tillgängliga")
                    
    except Exception as e:
        st.error(f"Ett fel uppstod vid riskbedömning: {str(e)}")

# Add footer with information
st.markdown("---")
st.markdown("""
**Om riskbedömningsfunktionen**

Denna funktion använder AI för att analysera juridiska dokument och ge en bedömning 
av sannolikheten för framgång baserat på textinnehållet. Analysen tar hänsyn till 
bevisläge, argumentation, och rättsliga principer.

*Notera: Detta är ett verktyg för beslutsstöd och ersätter inte professionell juridisk rådgivning.*
""")

# Run this with: streamlit run risk_assessment_standalone.py --server.port=5000