# Systemöversikt: Juridiskt AI-system

## Huvudnavigation och sidstruktur

Nedan följer en komplett översikt över alla sidor i systemet, deras titlar, menyplacering och huvudfunktioner.

| Filnamn | Menyvisning | Sidtitel (`st.title()`) | Funktionsbeskrivning |
|---------|-------------|--------------------------|----------------------|
| **Huvudsidor** | | | |
| `main.py` | *Startsida* | Juridiskt AI-system | Inloggning och huvudentré till systemet |
| `0_📊_Strategiöversikt.py` | 📊 Strategiöversikt | Strategiöversikt | Sammanfattning av juridiska strategier och planering |
| `0_🧭_AI-kontrollpanel.py` | 🧭 AI-kontrollpanel | AI-kontrollpanel | Hantering av AI-parametrar och inställningar |
| `1_📊_Strategikarta.py` | 📊 Strategikarta | Strategikarta | Visualisering av juridiska strategier |
| `2_🎯_Prognos_och_Risk.py` | 🎯 Prognos och Risk | Prognos och Risk | Riskbedömning och prognosverktyg |
| `3_⚖️_Prejudikatsimulering.py` | ⚖️ Prejudikatsimulering | Prejudikatsimulering | Simulering av prejudikat och rättsfall |
| `4_📝_Dokumentgenerator.py` | 📝 Dokumentgenerator | Dokumentgenerator | Generering av juridiska dokument |
| **Undersidor (pages/)** | | | |
| `pages/01_📄_Ställ_fråga.py` | 📄 Ställ fråga | Ställ juridisk fråga | Ställ allmänna frågor till AI-assistenten |
| `pages/01_📄_Ställ_juridisk_fråga.py` | 📄 Ställ juridisk fråga | Ställ juridisk fråga | Ställ specifika juridiska frågor till systemet |
| `pages/02_📝_Generera_dokument.py` | 📝 Generera dokument | Generera juridiska dokument | Skapa standardiserade juridiska dokument |
| `pages/02_📜_Juridisk_ordlista.py` | 📜 Juridisk ordlista | Juridisk ordlista | Förklaringar av juridiska termer och begrepp |
| `pages/03_🔍_Analysera_dokument.py` | 🔍 Analysera dokument | Analysera juridiska dokument | Ladda upp och analysera juridiska texter |
| `pages/03_⚙️_Appinställningar.py` | ⚙️ Appinställningar | Appinställningar | Personliga preferenser och inställningar |
| `pages/03_⚖️_Prejudikatanalys.py` | ⚖️ Prejudikatanalys | Prejudikatanalys | Analys av rättsfall och domar |
| `pages/04_📤_Exportera_svar.py` | 📤 Exportera svar | Exportera svar | Exportera AI-svar till olika format |
| `pages/04_🔍_Rättsfallsökning.py` | 🔍 Rättsfallsökning | Rättsfallsökning | Sök i databas med rättsfall |
| `pages/04_⚙️_Systemadmin.py` | ⚙️ Systemadmin | Systemadmin | Administrativa verktyg för systemet |
| `pages/05_Dokument.py` | Dokument | Dokument | Visa sparade dokument |
| `pages/05_⚙️_Kontoinställningar.py` | ⚙️ Kontoinställningar | Kontoinställningar | Hantera användarkonto och personliga inställningar |
| `pages/05_💾_Spara_historik.py` | 💾 Spara historik | Spara historik | Hantera och exportera användarhistorik |
| `pages/06_Prejudikat.py` | Prejudikat | Prejudikat | Databas med prejudikat |
| `pages/06_📨_Skicka_som_e-post.py` | 📨 Skicka som e-post | Skicka som e-post | Skicka genererade dokument via e-post |
| `pages/07_📱_Skicka_som_SMS.py` | 📱 Skicka som SMS | Skicka som SMS | Skicka meddelanden via SMS |
| `pages/08_🛠️_Adminpanel.py` | 🛠️ Adminpanel | Adminpanel | Administratörspanel för systemövervakning |

## Funktionsmoduler

| Modulfil | Huvudfunktion | Beskrivning |
|----------|---------------|-------------|
| `utils.py` | Hjälpfunktioner | Generella hjälpfunktioner för systemet |
| `db.py` | Databashantering | Hantering av databasoperationer |
| `utils/auth.py` | Autentisering | Användarhantering och säkerhet |
| `modules/gpt_assistant.py` | AI-integration | Integration med OpenAI API |
| `modules/structure_analyzer.py` | Dokumentanalys | Analys av juridiska dokuments struktur |
| `modules/template_generator.py` | Mallgenerering | Generering av dokumentmallar |
| `risk_analyzer.py` | Riskanalys | Bedömning av juridiska risker |
| `precedent_simulator.py` | Prejudikatsimulering | Simulering av prejudikat |
| `template_generator_docx.py` | DOCX-generering | Skapande av Word-dokument |

## Datalagring

| Datatyp | Lagringsplats | Beskrivning |
|---------|---------------|-------------|
| Användarinformation | `users.json` / databas | Användardata, lösenord och roller |
| Interaktionshistorik | Databas | Sparade frågor och svar |
| Dokument | Databas / `exports/` | Genererade och analyserade dokument |
| Rättsfall | Databas / JSON-filer | Prejudikat och domstolsbeslut |
| Konfigurationsdata | `config.json` | Systeminställningar |

## Behörighetsroller

Systemet stödjer följande användarroller med olika behörighetsnivåer:

1. **Admin** 
   - Fullständig åtkomst till alla funktioner
   - Kan hantera användare och system
   - Kan se systemstatistik

2. **Domare**
   - Åtkomst till rättsanalys och prejudikat
   - Kan generera juridiska dokument
   - Har tillgång till historikfunktioner

3. **Ombud** (Advokat)
   - Kan ställa juridiska frågor
   - Har tillgång till dokumentgenerering
   - Begränsad åtkomst till systemfunktioner

4. **Användare**
   - Basåtkomst till juridiska frågor
   - Kan exportera svar och historik
   - Begränsad åtkomst till avancerade funktioner

## Autentiseringsflöde

1. Användaren möts av inloggningssidan (`main.py`)
2. Efter framgångsrik inloggning:
   - Användarens roll fastställs
   - Session-data initieras
   - Användaren dirigeras till huvudpanelen baserat på roll

## Sidgrupperingar

Systemet grupperar sina funktioner logiskt:

1. **Strategi & Planering** (0-1)
   - Strategiöversikt
   - AI-kontrollpanel
   - Strategikarta

2. **Analys & Prognos** (2-3)
   - Prognos och Risk
   - Prejudikatsimulering
   - Prejudikatanalys

3. **Dokumenthantering** (4, 01-02)
   - Dokumentgenerator
   - Generera dokument
   - Analysera dokument

4. **Rättsresurser** (03-04)
   - Rättsfallsökning
   - Juridisk ordlista
   - Prejudikat

5. **Kommunikation** (05-07)
   - Exportera svar
   - Skicka som e-post
   - Skicka som SMS

6. **Konfiguration** (03-08)
   - Appinställningar
   - Systemadmin
   - Kontoinställningar
   - Adminpanel

---

**Notera:** Denna översikt är aktuell per 2025-05-06 och uppdateras vid större systemförändringar.