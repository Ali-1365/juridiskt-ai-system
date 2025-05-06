# Juridiskt AI-system 

Ett avancerat AI-drivet juridiskt analyssystem anpassat för svenska rättsväsendet.

![Juridiskt AI-system](generated-icon.png)

## Översikt

Juridiskt AI-system är en kraftfull plattform som kombinerar modern AI-teknik med gedigen juridisk expertis för att assistera domare, advokater och andra juridiska yrkesutövare i deras dagliga arbete.

### Huvudfunktioner

- **Juridisk fråga-svar**: Ställ frågor på naturligt språk och få välgrundade svar med referenser
- **Dokumentgenerator**: Skapa standardiserade juridiska dokument utifrån mallar
- **Rättsfallsanalys**: Sök och analysera rättsfall för att identifiera prejudikat
- **Dokumentanalys**: Ladda upp och analysera juridiska texter för att extrahera nyckelpoänger
- **Statistik och insikter**: Visualisera trender och mönster i din juridiska verksamhet
- **Exportfunktionalitet**: Spara alla resultat som DOCX, PDF eller textfil
- **Användarkonton**: Stöd för olika användarroller med anpassade behörigheter

## Installation

### Förutsättningar

- Python 3.10+
- Streamlit
- OpenAI API-nyckel

### Steg för steg

1. Klona detta repository:
   ```
   git clone https://github.com/användare/juridiskt-ai-system.git
   cd juridiskt-ai-system
   ```

2. Installera beroenden:
   ```
   pip install -r requirements.txt
   ```

3. Konfigurera API-nycklar:
   ```
   # Skapa en .env-fil med dina API-nycklar
   echo "OPENAI_API_KEY=din_nyckel_här" > .env
   ```

4. Starta applikationen:
   ```
   streamlit run main.py
   ```

## Användning

### Inloggning

Applikationen har tre inbyggda användarroller:
- **Admin**: Fullständig åtkomst till alla funktioner och administration
- **Domare**: Åtkomst till domar, prejudikat och rättsfallsanalys
- **Ombud**: Basåtkomst till juridiska frågor och dokumentgenerering

Standardinloggningsuppgifter:
- Användarnamn: `admin`, Lösenord: `password123`

### Huvudfunktioner

1. **Juridisk rådgivning**: Ställ juridiska frågor och få svar baserade på svensk lagstiftning
2. **Dokumenthantering**: Generera och analysera juridiska dokument
3. **Rättsfallsanalys**: Sök och jämför relevanta rättsfall
4. **Systeminställningar**: Konfigurera API-nycklar, exportformat och UI-preferenser

## Projektstruktur

```
juridiskt-ai-system/
├── main.py               # Huvudapplikation och inloggning
├── pages/                # Streamlit-sidor för olika funktioner
├── modules/              # Funktionsmoduler (AI, dokumentgenerering, etc.)
├── utils/                # Hjälpfunktioner och verktyg
├── assets/               # Statiska tillgångar (bilder, ikoner, etc.)
├── data/                 # Datakällor och exempel
├── exports/              # Exporterade filer
├── templates/            # Dokumentmallar
├── config.json           # Konfigurationsfil
├── users.json            # Användarinformation
└── requirements.txt      # Projektberoenden
```

## Utveckling

### Teknisk översikt

- **Frontend**: Streamlit (Python-baserat)
- **AI-integration**: OpenAI GPT-4o
- **Datalagring**: SQLite-databas för historik och användardata
- **Dokumenthantering**: DOCX, PDF och textfilsgenerering

### Utvecklingsstrategi

Se [ROADMAP.md](ROADMAP.md) för planerade funktioner och utvecklingsmål.

## Dokumentation

- **Användardokumentation**: Se `docs/user_guide.md`
- **Utvecklardokumentation**: Se `docs/developer_guide.md`
- **API-dokumentation**: Se `docs/api_reference.md`

## Licens

Detta projekt är licensierat under MIT-licensen - se [LICENSE](LICENSE) för detaljer.

## Kontakt

För frågor och support, vänligen kontakta:
- E-post: support@juridiskt-ai.se
- GitHub: [Skapa en issue](https://github.com/användare/juridiskt-ai-system/issues)

---

*Ansvarsfriskrivning: Detta system ger inte juridisk rådgivning och ersätter inte professionell juridisk hjälp.*