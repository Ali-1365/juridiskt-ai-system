import streamlit as st
import os
from utils.openai_client import get_openai_client
from utils.notification import show_success, show_error, show_warning, show_info

# Konfigurera sidan
st.set_page_config(page_title="Juridiskt AI-system", layout="wide")

# Grundläggande felhantering för API-nyckel
try:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API-nyckel saknas. Vänligen konfigurera API-nyckeln i Secrets.")
        st.stop()

    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Fel vid initialisering av OpenAI-klienten: {str(e)}")
    st.stop()

# Huvudgränssnitt
st.title("Juridiskt AI-system")
st.write("Välkommen till det juridiska AI-systemet!")

# Test av API-anslutning
if st.button("Testa API-anslutning"):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Test"}]
        )
        st.success("✅ API-anslutning fungerar!")
    except Exception as e:
        st.error(f"❌ API-fel: {str(e)}")


# Hälsokontroll-endpoint för t.ex. deployment
query_params = st.query_params
if 'health' in query_params or query_params.get('') == ['/']:
    st.write("OK")
    st.stop()

# Enkelt lösenordsskydd
def check_password():
    """Returnerar `True` om användaren har angett rätt lösenord."""

    # Tillgängliga användare (enkelt format för demo)
    USERS = {
        "admin": "password123",
        "user": "user123",
    }

    def login_form():
        """Visar inloggningsformulär."""
        with st.form("login"):
            st.subheader("Logga in")
            username = st.text_input("Användarnamn")
            password = st.text_input("Lösenord", type="password")
            submitted = st.form_submit_button("Logga in")

            if submitted:
                if username in USERS and password == USERS[username]:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.success("Inloggad!")
                    return True
                else:
                    st.error("Felaktigt användarnamn eller lösenord")
                    return False
            return False

    # Kontrollera om användaren redan är autentiserad
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_form()
        st.stop()  # Stoppa exekvering om inloggning inte lyckats

    return True

# Kontrollera om användaren är inloggad
check_password()

# Visa ett välkomstmeddelande och utloggningsknapp
col1, col2 = st.columns([5,1])
with col1:
    st.title("Juridiskt AI-system")
with col2:
    if st.button("Logga ut", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()

# Lägger till tydligare instruktioner
st.markdown("""
### Välkommen till Juridiskt AI-system!

Detta system hjälper dig att få svar på juridiska frågor med hjälp av OpenAI API.

**Instruktioner:**
1. Skriv din fråga i textfältet nedan
2. Klicka på "Skicka till OpenAI"-knappen
3. Invänta svaret från AI-systemet

**Exempel på frågor du kan ställa:**
- Vad är skillnaden mellan tingsrätt och hovrätt?
- Förklara vad prejudikat betyder
- Vilka är de viktigaste momenten i en rättegång?
""")

st.markdown("---")

#if not api_key:
#    st.error("OpenAI API-nyckel saknas. Kontrollera dina secrets eller miljövariabler.")
#    st.stop()

# Initiera OpenAI-klienten
#client = OpenAI(api_key=api_key)

# Visa att API-nyckeln fungerar (ta bort i produktion)
st.success("✅ Ansluten till OpenAI API")

# Inställningar i sidofältet
with st.sidebar:
    st.markdown("## ⚙️ Inställningar")

    # Språkval
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "Svenska"

    st.session_state.selected_language = st.selectbox(
        "Språk",
        ["Svenska", "English", "فارسی (Persian)"],
        index=["Svenska", "English", "فارسی (Persian)"].index(st.session_state.selected_language)
    )

    # AI-modellval
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gpt-4o"

    st.session_state.selected_model = st.selectbox(
        "AI-modell",
        ["gpt-4o", "gpt-3.5-turbo"],
        index=["gpt-4o", "gpt-3.5-turbo"].index(st.session_state.selected_model)
    )

    st.markdown("---")
    st.markdown("### Om appen")
    st.markdown("""
    Detta är ett juridiskt AI-system som hjälper dig med juridiska frågor. 
    Systemet använder OpenAI:s API för att generera svar.

    **Version**: 2.0
    **Uppdaterad**: 2025-05-06
    """)

# Rensa-knapp i session state
if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# Funktion för att rensa textfältet
def clear_text():
    st.session_state.prompt = ""

# Funktion för att hantera fördefinierade exempel
def use_template(template_text):
    st.session_state.prompt = template_text

# Funktion för att skicka till OpenAI
def send_to_openai():
    if st.session_state.prompt.strip():
        with st.spinner("Genererar svar..."):
            try:
                # Använd den valda modellen från sidofältet
                # OBS: gpt-4o är den nyaste OpenAI-modellen, släppt 13 maj 2024
                selected_model = st.session_state.selected_model

                # Anpassa systemmessaget efter valt språk
                system_message = ""
                if st.session_state.selected_language == "Svenska":
                    system_message = "Du är en juridisk AI-assistent som hjälper till med svenska juridiska frågor. Svara på svenska."
                elif st.session_state.selected_language == "English":
                    system_message = "You are a legal AI assistant helping with legal questions. Answer in English."
                elif st.session_state.selected_language == "فارسی (Persian)":
                    system_message = "شما یک دستیار حقوقی هوش مصنوعی هستید که به سوالات حقوقی کمک می کنید. به فارسی پاسخ دهید."

                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": st.session_state.prompt}
                    ]
                )
                st.session_state.generated_response = response.choices[0].message.content

                # Spara till historik
                if st.session_state.prompt not in st.session_state.prompt_history:
                    st.session_state.prompt_history.append(st.session_state.prompt)

                # Visa svaret med formatering
                st.success("Svar:")
                st.markdown(st.session_state.generated_response)

                # Visa kopiera-knapp med JavaScript
                st.markdown("""
                <div class="stButton">
                <button
                    onclick="
                        navigator.clipboard.writeText(`%s`);
                        this.innerText='✓ Kopierat!';
                        setTimeout(() => this.innerText='📋 Kopiera svar', 2000)
                    "
                    style="
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 24px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                        width: 100%%;
                    "
                >
                    📋 Kopiera svar
                </button>
                </div>
                """ % st.session_state.generated_response.replace("`", "\\`"), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Något gick fel vid anrop till OpenAI: {str(e)}")
                st.error(f"Feldetaljer: {type(e).__name__}")
    else:
        st.warning("Prompten får inte vara tom.")

# Resterande app-logik
st.markdown("### Skriv din fråga här:")

# Fördefinierade exempel-knappar
st.markdown("#### Fördefinierade frågor:")
templates_col1, templates_col2 = st.columns(2)

with templates_col1:
    if st.button("❓ Vad är prejudikat?", use_container_width=True):
        use_template("Vad är prejudikat och hur påverkar det rättssystemet i Sverige?")

    if st.button("📝 Skapa ett överklagande", use_container_width=True):
        use_template("Hjälp mig skapa ett överklagande för ett parkeringsböter. Jag fick böter trots att skyltningen var otydlig.")

with templates_col2:
    if st.button("⚖️ Skillnad mellan domstolar", use_container_width=True):
        use_template("Förklara skillnaden mellan tingsrätt, hovrätt och Högsta domstolen i Sverige.")

    if st.button("📋 Juridisk ordlista", use_container_width=True):
        use_template("Skapa en lista med 10 viktiga juridiska begrepp och deras förklaringar som är relevanta för svenska domstolsprocesser.")

st.markdown("---")

# Textområde med rensa-knapp
col1, col2 = st.columns([4, 1])
with col1:
    prompt = st.text_area("", height=150, placeholder="Skriv din juridiska fråga här...", key="prompt")
with col2:
    st.write("")
    st.write("")
    if st.button("🧹 Rensa", use_container_width=True):
        clear_text()

# Visa vald modell och språk
st.info(f"🤖 Använder modell: **{st.session_state.selected_model}** | 🌐 Språk: **{st.session_state.selected_language}**")

# Skicka-knapp
if st.button("📤 Skicka till OpenAI", use_container_width=True):
    send_to_openai()

# Historik-sektion om det finns historik
if st.session_state.prompt_history:
    with st.expander("Tidigare frågor"):
        for i, previous_prompt in enumerate(st.session_state.prompt_history):
            if st.button(f"Använd igen: {previous_prompt[:50]}...", key=f"history_{i}"):
                st.session_state.prompt = previous_prompt
                st.rerun()