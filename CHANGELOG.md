# Juridiskt AI-system: Ändringslogg

## [1.0.0] - 2025-05-06
### Första versionen
- Grundläggande funktionalitet för juridisk AI-assistent
- Frågeställning och svar med OpenAI
- Stöd för svenska, engelska och persiska
- Säker autentisering

### Funktioner
- **01_📄_Ställ_juridisk_fråga.py**: Huvudgränssnitt för att ställa juridiska frågor
- **02_📜_Juridisk_ordlista.py**: Sökbar ordlista med juridiska termer
- **03_⚙️_Inställningar.py**: Konfiguration av språk och AI-modell
- **04_📤_Exportera_svar.py**: Exportera svar till DOCX och PDF
- **05_💾_Spara_historik.py**: Spara och exportera frågehistorik
- **06_📨_Skicka_som_e-post.py**: Skicka svar via e-post
- **07_📱_Skicka_som_SMS.py**: Skicka svar via SMS med Twilio
- **08_🛠️_Adminpanel.py**: Administratörspanel med statistik och systemöversikt

### Tekniska detaljer
- Streamlit för användargränssnittet
- SQLite-databas för historik
- OpenAI API för AI-funktionalitet
- Stöd för dokumentexport (DOCX, PDF)
- Email- och SMS-integrationer