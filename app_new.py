import streamlit as st
import openai
import os
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Juridiskt AI-system", layout="centered")
st.title("Juridiskt AI-system")

# Get API key from environment variable or let user input it
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = st.text_input("Ange din OpenAI API-nyckel", type="password")
else:
    st.success("API-nyckel hittades i miljövariablerna.")

prompt = st.text_area("Skriv din juridiska fråga här:")

# Select model to use
model = st.selectbox("Välj modell", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"])

if st.button("Skicka") and api_key and prompt:
    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key)
        
        with st.spinner("Bearbetar din fråga..."):
            # Call the OpenAI API
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Display the response
            st.subheader("Svar:")
            st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Ett fel uppstod: {e}")
elif st.button("Skicka"):
    st.warning("Fyll i både API-nyckel och prompt.")

# Add information about the system
with st.expander("Om Juridiskt AI-system"):
    st.markdown("""
    Detta är ett enkelt juridiskt AI-system som använder OpenAI:s språkmodeller 
    för att svara på juridiska frågor. Systemet är avsett för utbildningssyfte 
    och svar bör inte betraktas som juridisk rådgivning.
    
    **Modeller:**
    - GPT-4o: OpenAI:s nyaste och mest avancerade modell
    - GPT-4: Kraftfull modell för komplexa uppgifter
    - GPT-3.5 Turbo: Snabb modell för enklare frågor
    """)