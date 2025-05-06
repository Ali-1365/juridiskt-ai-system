#!/usr/bin/env python3
"""
Skript för att skapa en ZIP-fil av hela projektet, med möjlighet att exkludera filer.
Användbart för distribution eller backup.

Användning:
    python create_project_zip.py [output_filename.zip]
"""

import os
import sys
import zipfile
import datetime
import shutil
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
    r'.*\.zip$'
]

def should_exclude(path, exclude_patterns):
    """
    Kontrollerar om en sökväg ska exkluderas baserat på de angivna mönstren.
    """
    path_str = str(path)
    return any(re.search(pattern, path_str) for pattern in exclude_patterns)

def create_zip(output_filename=None, exclude_patterns=None, verbose=True):
    """
    Skapar en ZIP-fil av hela projektet med angivna exkluderingar.
    
    Args:
        output_filename: Namn på ZIP-filen. Om None genereras ett standardnamn.
        exclude_patterns: Lista över regex-mönster för exkludering.
        verbose: Om True, skrivs detaljerad information ut under processen.
    
    Returns:
        Sökvägen till den skapade ZIP-filen.
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
    
    if verbose:
        print(f"Skapar ZIP-fil av projektet: {output_filename}")
        print("Exkluderar följande mönster:")
        for pattern in exclude_patterns:
            print(f"  - {pattern}")
        print("\nLägger till filer...")
    
    # Räkna totalt antal filer för att visa framsteg
    total_files = sum(1 for _ in project_root.rglob('*') if _.is_file() and not should_exclude(_, exclude_patterns))
    added_files = 0
    
    # Skapa ZIP-filen
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in project_root.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path, exclude_patterns):
                # Lägg till filen i ZIP med relativ sökväg
                zipf.write(file_path, file_path.relative_to(project_root))
                added_files += 1
                
                if verbose and added_files % 10 == 0:
                    progress = (added_files / total_files) * 100
                    print(f"Framsteg: {added_files}/{total_files} filer ({progress:.1f}%)", end='\r')
    
    # Visa slutgiltig information
    if verbose:
        zip_size = os.path.getsize(output_filename) / (1024 * 1024)  # Storlek i MB
        print(f"\nZIP-fil skapad: {output_filename}")
        print(f"Storlek: {zip_size:.2f} MB")
        print(f"Totalt antal filer: {added_files}")
    
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
    
    # Kör skriptet för att kontrollera unika titlar om det finns
    if os.path.exists('check_unique_pages.py'):
        print("\nKontrollerar unika sidtitlar före paketering...")
        try:
            import check_unique_pages
            if not check_unique_pages.check_unique_page_titles():
                print("\nVarning: Duplicerade titlar hittades. Det kan orsaka problem i Streamlit.")
                response = input("Vill du fortsätta ändå? (j/n): ").lower()
                if response != 'j':
                    print("Avbryter paketering.")
                    sys.exit(1)
        except ImportError:
            print("Kunde inte importera check_unique_pages.py. Fortsätter utan kontroll.")
    
    # Bestäm filnamn baserat på kommandoradsargument
    output_filename = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Skapa ZIP-filen
    zip_path = create_zip(output_filename)
    
    print(f"\nProjektet har paketerats till: {zip_path}")
    print("Du kan nu distribuera denna ZIP-fil eller ladda upp den till en lagringstjänst.")