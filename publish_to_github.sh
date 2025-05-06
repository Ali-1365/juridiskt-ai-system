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