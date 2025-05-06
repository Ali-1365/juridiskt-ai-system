# Juridiskt AI-system: Deployeringsguide

Denna guide beskriver hur du kan deployera ditt Juridiskt AI-system på olika plattformar.

## 📋 Innehållsförteckning

1. [Deployera på Replit](#deployera-på-replit)
2. [Deployera på Hugging Face Spaces](#deployera-på-hugging-face-spaces)
3. [Deployera på Render.com](#deployera-på-rendercom)
4. [Lokal installation](#lokal-installation)
5. [Konfiguration](#konfiguration)

## 📦 Projektstruktur

```
juridiskt-ai-system/
│
├── main.py                      # Startsida (introduktion/inloggning)
├── requirements_project.txt     # Alla beroenden
├── .streamlit/
│   └── config.toml              # Portinställningar m.m.
├── pages/
│   ├── 01_📄_Ställ_juridisk_fråga.py
│   ├── 02_📜_Juridisk_ordlista.py
│   ├── 03_⚙️_Inställningar.py
│   ├── 04_📤_Exportera_svar.py
│   ├── 05_💾_Spara_historik.py
│   ├── 06_📨_Skicka_som_e-post.py
│   ├── 07_📱_Skicka_som_SMS.py
│   └── 08_🛠️_Adminpanel.py
└── db.py                        # Databashantering
```

## 🔄 Deployera på Replit

Din app är redan uppstartad på Replit. Följande steg hjälper dig att göra den tillgänglig för andra användare:

1. **Publicera din Repl**
   - Klicka på "Share" i Replit UI
   - Välj "Publish Repl"
   - Ange en beskrivning och klicka på "Publish"

2. **Konfigurera hemligheter:**
   - Gå till "Secrets" i vänstra panelen
   - Lägg till alla nödvändiga API-nycklar:
     - `OPENAI_API_KEY`
     - `EMAIL_SENDER`, `EMAIL_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT` (för e-post)
     - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` (för SMS)

3. **Aktivera Always On (kräver Replit Pro)**
   - Detta håller din app igång kontinuerligt

## 🤗 Deployera på Hugging Face Spaces

Hugging Face Spaces erbjuder gratis hosting för Streamlit-appar:

1. **Skapa ett konto på Hugging Face**
   - Besök [huggingface.co](https://huggingface.co) och registrera dig

2. **Skapa ett nytt Space**
   - Klicka på ditt profilfoto > "New Space"
   - Välj "Streamlit" som SDK
   - Ange ett namn för ditt Space

3. **Ladda upp filer**
   - Du kan ladda upp filer via webbgränssnittet eller använda Git

4. **Viktiga filer att inkludera:**
   - `app.py` (kopiera innehållet från main.py)
   - `requirements.txt` (kopiera från requirements_project.txt)
   - Alla filer i pages/-mappen
   - `.streamlit/config.toml`

5. **Konfigurera hemligheter**
   - I Spaces UI, gå till "Settings" > "Repository secrets"
   - Lägg till alla nödvändiga API-nycklar (samma som för Replit)

## 🌐 Deployera på Render.com

Render erbjuder mer professionell hosting:

1. **Skapa ett GitHub-repo**
   - Ladda upp alla projektfiler till ett nytt GitHub-repository

2. **Registrera dig på Render.com**
   - Besök [render.com](https://render.com) och skapa ett konto

3. **Skapa ny Web Service**
   - Klicka på "New" > "Web Service"
   - Koppla ditt GitHub-repo

4. **Konfigurera tjänsten**
   - Namnge din tjänst
   - Startkommando: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`
   - Build Command: `pip install -r requirements_project.txt`

5. **Konfigurera miljövariabler**
   - I Render UI, gå till "Environment" > "Environment Variables"
   - Lägg till alla nödvändiga API-nycklar (samma som för Replit)

6. **Deployera**
   - Klicka på "Create Web Service"

## 💻 Lokal installation

För att köra applikationen lokalt:

1. **Klona repo eller ladda ner filerna**

2. **Installera beroenden**
   ```bash
   pip install -r requirements_project.txt
   ```

3. **Skapa .env-fil**
   Skapa en fil med namnet `.env` i projektets rotkatalog med följande innehåll:
   ```
   OPENAI_API_KEY=din_openai_nyckel
   EMAIL_SENDER=din_email@domain.com
   EMAIL_PASSWORD=ditt_lösenord
   SMTP_SERVER=smtp.domain.com
   SMTP_PORT=587
   TWILIO_ACCOUNT_SID=din_twilio_sid
   TWILIO_AUTH_TOKEN=din_twilio_token
   TWILIO_PHONE_NUMBER=din_twilio_nummer
   ```

4. **Starta applikationen**
   ```bash
   streamlit run main.py
   ```

## ⚙️ Konfiguration

### API-nycklar och hemligheter

För att alla funktioner ska fungera behöver du:

1. **OpenAI API-nyckel**
   - Registrera på [OpenAI](https://platform.openai.com)
   - Skapa en API-nyckel under "API Keys"

2. **E-postkonfiguration**
   - För Gmail: 
     - `EMAIL_SENDER`: Din Gmail-adress
     - `EMAIL_PASSWORD`: Ett "App Password" (inte ditt vanliga lösenord)
     - `SMTP_SERVER`: smtp.gmail.com
     - `SMTP_PORT`: 587

3. **Twilio-konfiguration (för SMS)**
   - Registrera på [Twilio](https://www.twilio.com)
   - Från Twilio Console, hämta:
     - Account SID
     - Auth Token
     - Twilio Phone Number (köp ett nummer)

### Databasinställningar

Applikationen använder SQLite som standard. För produktionsmiljö rekommenderas:

1. **PostgreSQL**
   - Installera PostgreSQL
   - Uppdatera anslutningssträngen i `db.py`

## 🛠️ Felsökning

### Vanliga problem

1. **App startar inte**
   - Kontrollera att alla beroenden är installerade
   - Verifiera att `main.py` finns i rotkatalogen

2. **OpenAI-problem**
   - Kontrollera att API-nyckeln är korrekt och har tillräckligt med krediter

3. **E-post- eller SMS-fel**
   - Verifiera att alla hemligheter är korrekt konfigurerade
   - För Gmail, se till att "Less secure app access" är aktiverat

För ytterligare hjälp, kontakta systemadministratören eller skapa ett issue på GitHub-repot.