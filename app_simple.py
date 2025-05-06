"""
Juridiskt AI-system
Enkel OpenAI-integration för juridiska frågor.
"""
import os
import streamlit as st
import openai

# Konfigurera sidan
st.set_page_config(page_title="Juridiskt AI-system", layout="centered")
st.title("Juridiskt AI-system")

# Få API-nyckel från miljövariabel eller låt användaren skriva in den
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = st.text_input("Ange din OpenAI API-nyckel", type="password")
else:
    st.success("API-nyckel hittades i miljövariablerna.")

prompt = st.text_area("Skriv din juridiska fråga här:")

# Välj modell att använda
model = st.selectbox("Välj modell", ["gpt-4", "gpt-3.5-turbo"])

submit_button = st.button("Skicka", key="submit_button")

if submit_button:
    if api_key and prompt:
        try:
            # Sätt API-nyckeln
            openai.api_key = api_key
            
            with st.spinner("Bearbetar din fråga..."):
                # Anropa OpenAI API
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Visa svaret
                st.subheader("Svar:")
                st.write(response.choices[0].message["content"])
        except Exception as e:
            st.error(f"Ett fel uppstod: {e}")
    else:
        st.warning("Fyll i både API-nyckel och prompt.")