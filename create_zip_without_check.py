#!/usr/bin/env python3
"""
Skript för att skapa en ZIP-fil av hela projektet utan kontroller.
"""

import os
import sys
import zipfile
import datetime
from pathlib import Path
import re

# Standardexkluderingar - filer och mappar som aldrig ska inkluderas
DEFAULT_EXCLUDES = [
    # Generella exkluderingar
    r'__pycache__',
    r'\.git',
    r'\.DS_Store',
    r'\.gitignore',
    r'\.env',
    r'\.venv',
    r'env',
    r'venv',
    r'\.idea',
    r'\.vscode',
    r'\.pytest_cache',
    
    # Specifika för detta projekt
    r'juridisk_ai\.db',
    r'.*\.db$',
    r'exports/.*',
    r'temp/.*',
    r'logs/.*',
    r'uploads/.*',
    r'\.streamlit/secrets\.toml$',
    
    # Själva ZIP-skaparen
    r'create_project_zip\.py$',
    r'create_zip_without_check\.py$',
    r'check_unique_pages\.py$',
    r'.*\.zip$'
]

def should_exclude(path, exclude_patterns):
    """
    Kontrollerar om en sökväg ska exkluderas baserat på de angivna mönstren.
    """
    path_str = str(path)
    return any(re.search(pattern, path_str) for pattern in exclude_patterns)

def create_zip(output_filename=None, exclude_patterns=None):
    """
    Skapar en ZIP-fil av hela projektet med angivna exkluderingar.
    """
    # Använd standardexkluderingar om inga anges
    if exclude_patterns is None:
        exclude_patterns = DEFAULT_EXCLUDES
    
    # Generera standardfilnamn om inget anges
    if output_filename is None:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"juridiskt_ai_system_{timestamp}.zip"
    
    # Se till att filnamnet slutar med .zip
    if not output_filename.endswith('.zip'):
        output_filename += '.zip'
    
    # Hämta projektets rotkatalog
    project_root = Path('.')
    
    print(f"Skapar ZIP-fil av projektet: {output_filename}")
    
    # Skapa ZIP-filen
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in project_root.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path, exclude_patterns):
                # Lägg till filen i ZIP med relativ sökväg
                zipf.write(file_path, file_path.relative_to(project_root))
    
    # Visa slutgiltig information
    zip_size = os.path.getsize(output_filename) / (1024 * 1024)  # Storlek i MB
    print(f"ZIP-fil skapad: {output_filename}")
    print(f"Storlek: {zip_size:.2f} MB")
    
    return output_filename

def create_empty_dirs():
    """Skapar nödvändiga tomma kataloger som kan saknas"""
    dirs_to_create = [
        'exports',
        'temp',
        'logs', 
        'uploads',
        'data',
        '.streamlit'
    ]
    
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
        # Skapa en .gitkeep-fil om den inte finns
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                pass

if __name__ == "__main__":
    # Skapa nödvändiga tomma kataloger
    create_empty_dirs()
    
    # Bestäm filnamn baserat på kommandoradsargument
    output_filename = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Skapa ZIP-filen
    zip_path = create_zip(output_filename)
    
    print(f"Projektet har paketerats till: {zip_path}")
    print("Du kan nu distribuera denna ZIP-fil eller ladda upp den till en lagringstjänst.")