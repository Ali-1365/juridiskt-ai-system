import streamlit as st
from openai import OpenAI
import os
from db import init_db

# Initialize database
init_db()

# Configure the page
st.set_page_config(
    page_title="Juridiskt AI-system",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enkel lösenordsinloggning - bör ersättas med en säkrare lösning
USERS = {"admin": "password123", "user": "user123"}

def login():
    """Handle user login"""
    with st.form("login"):
        st.subheader("Logga in")
        username = st.text_input("Användarnamn")
        password = st.text_input("Lösenord", type="password")
        if st.form_submit_button("Logga in"):
            if username in USERS and USERS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Inloggad!")
                st.rerun()
            else:
                st.error("Felaktigt användarnamn eller lösenord")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

if "model" not in st.session_state:
    st.session_state.model = "gpt-4o"

if "language" not in st.session_state:
    st.session_state.language = "Svenska"

# Handle authentication
if not st.session_state.authenticated:
    login()
    st.stop()

# If we've made it this far, user is authenticated
st.title("Juridiskt AI-system")
st.write(f"Välkommen, {st.session_state.username}!")

# Main page content - basic description
st.markdown("""
## Välkommen till Juridiskt AI-system

Detta system hjälper dig med juridiska frågor och analys. Använd sidomenyn för att:

- Ställ juridiska frågor och få AI-assisterade svar
- Läs om juridiska termer i vår ordlista
- Anpassa dina inställningar

Systemet använder OpenAI's modeller för att ge svar baserat på juridisk information.
""")

# Sidebar with additional options
st.sidebar.header("Navigering")
st.sidebar.info("""
Välj funktion i menyn till vänster:

📄 Ställ fråga - Fråga AI-systemet
📜 Juridisk ordlista - Hitta definitioner
⚙️ Inställningar - Anpassa systemet
""")