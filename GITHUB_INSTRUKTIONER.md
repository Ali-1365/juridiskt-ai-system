# Instruktioner för GitHub-publicering

Följ denna guide för att publicera ditt juridiska AI-system på GitHub.

## Förberedelser

1. **Kontrollera att projektet är redo för publicering**

   Kör kontrollen för unika sidtitlar:
   ```bash
   python check_unique_pages.py
   ```

   Skapa en ZIP-kopia av projektet som backup:
   ```bash
   python create_project_zip.py juridiskt_ai_backup.zip
   ```

2. **Skapa ett GitHub-konto**

   Om du inte redan har ett GitHub-konto, besök [GitHub](https://github.com/) och skapa ett konto.

## Metod 1: Via GitHub webbgränssnitt

1. **Skapa ett nytt repository**

   - Gå till [GitHub](https://github.com) och logga in
   - Klicka på "+" ikonen i övre högra hörnet och välj "New repository"
   - Namnge ditt repository (t.ex. "juridiskt-ai-system")
   - Lägg till en beskrivning (t.ex. "Ett avancerat AI-drivet juridiskt analyssystem")
   - Välj "Public" eller "Private" beroende på önskad synlighet
   - Välj "Add a README file" (vi ersätter den senare)
   - Välj en licens (vi har valt MIT i LICENSE-filen)
   - Klicka på "Create repository"

2. **Ladda upp filer**

   - I ditt nya repository, klicka på "Add file" > "Upload files"
   - Dra och släpp projektet, eller välj filer via filväljaren
   - **OBS:** GitHub har en filstorleksgräns på 100 MB. Du kan behöva ladda upp i omgångar.
   - Skriv ett commit-meddelande (t.ex. "Initial upload")
   - Klicka på "Commit changes"

## Metod 2: Via kommandoraden (rekommenderas)

1. **Installera Git**

   Om du inte redan har Git installerat:
   - För Windows: Ladda ner och installera från [git-scm.com](https://git-scm.com/download/win)
   - För macOS: Kör `brew install git` eller ladda ner från [git-scm.com](https://git-scm.com/download/mac)
   - För Linux: Kör `sudo apt-get install git` (Ubuntu/Debian) eller motsvarande

2. **Konfigurera Git**

   ```bash
   git config --global user.name "Ditt Namn"
   git config --global user.email "din.email@exempel.com"
   ```

3. **Skapa ett nytt repository på GitHub**

   - Gå till [GitHub](https://github.com) och logga in
   - Klicka på "+" ikonen i övre högra hörnet och välj "New repository"
   - Namnge ditt repository (t.ex. "juridiskt-ai-system")
   - Lämna allt annat som standard utan att välja README, gitignore eller License
   - Klicka på "Create repository"

4. **Initiera Git-repository lokalt och ladda upp**

   Öppna en terminal/kommandotolk och navigera till projektmappen:

   ```bash
   # Initiera ett git-repository
   git init

   # Lägg till alla filer i projektmappen
   git add .

   # Skapa en initial commit
   git commit -m "Initial commit: Juridiskt AI-system"

   # Koppla din lokala repository till GitHub-repository
   # Ersätt YOUR-USERNAME med ditt GitHub-användarnamn och REPO-NAME med ditt repository-namn
   git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git

   # Ladda upp till GitHub
   git push -u origin master
   # eller om din huvudgren heter 'main':
   # git push -u origin main
   ```

## Efter publicering

1. **Aktivera GitHub Pages (valfritt)**

   För att skapa en enkel webbsida för projektet:
   - Gå till ditt repository på GitHub
   - Klicka på "Settings" > "Pages"
   - Under "Source", välj "main" (eller "master") och "/docs" om du har skapat en docs-katalog
   - Klicka på "Save"

2. **Skapa Releases**

   För att markera versioner av ditt projekt:
   - Gå till ditt repository på GitHub
   - Klicka på "Releases" > "Create a new release"
   - Ange versionsnummer (t.ex. "v1.0.0")
   - Lägg till en titel och beskrivning
   - Du kan ladda upp ZIP-filen som skapades tidigare som en binär release
   - Klicka på "Publish release"

## Kommandrad-skript för snabb publicering

Här är ett skript du kan köra för att snabbt publicera till GitHub (spara som `publish_to_github.sh`):

```bash
#!/bin/bash
# Publicera juridiskt AI-system till GitHub
# Användning: ./publish_to_github.sh "ditt-användarnamn" "repository-namn"

if [ $# -lt 2 ]; then
    echo "Användning: ./publish_to_github.sh \"ditt-användarnamn\" \"repository-namn\""
    exit 1
fi

USERNAME=$1
REPO_NAME=$2

echo "Förbereder publicering till GitHub..."
echo "Användarnamn: $USERNAME"
echo "Repository: $REPO_NAME"

# Skapa backup
echo "Skapar backup..."
python create_project_zip.py juridiskt_ai_backup.zip

# Kontrollera unika sidtitlar
echo "Kontrollerar sidtitlar..."
python check_unique_pages.py

# Initiera git om det inte redan finns
if [ ! -d ".git" ]; then
    echo "Initierar git repository..."
    git init
fi

# Konfigurera git om det behövs
if [ -z "$(git config --get user.name)" ]; then
    echo "Ange ditt namn för git-konfiguration:"
    read GIT_NAME
    git config user.name "$GIT_NAME"
fi

if [ -z "$(git config --get user.email)" ]; then
    echo "Ange din e-post för git-konfiguration:"
    read GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

# Lägg till alla filer
echo "Lägger till filer till git..."
git add .

# Commit
echo "Skapar commit..."
git commit -m "Initial commit: Juridiskt AI-system"

# Lägg till remote och push
echo "Konfigurerar remote repository..."
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"

echo "Publicerar till GitHub..."
git push -u origin master || git push -u origin main

echo "✅ Publicering klar!"
echo "Besök ditt repository på: https://github.com/$USERNAME/$REPO_NAME"
```

## Viktiga anmärkningar

- **API-nycklar:** Var noga med att inte ladda upp känslig information som API-nycklar. Vi har redan konfigurerat `.gitignore` för att undvika detta.
- **Databasfiler:** Var försiktig så att du inte laddar upp databasfiler som kan innehålla känslig användardata.
- **Stora filer:** GitHub har begränsningar för filstorlek. Använd Git LFS för stora filer eller exkludera dem från repository.

---

När du har publicerat projektet, skicka gärna länken till mig så att jag kan ta en titt och ge feedback!