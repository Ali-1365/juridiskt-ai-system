#!/usr/bin/env python3
"""
Verktyg för att kontrollera unika sidtitlar i Streamlit-applikationen.
Detta script verifierar att inga duplicerade page_title eller st.title() finns i systemet.

Användning:
    python check_unique_pages.py
"""

import os
import re
import sys
from collections import defaultdict
from termcolor import colored
import glob

def scan_files(directory="."):
    """Söker rekursivt genom directory efter .py-filer"""
    return glob.glob(f"{directory}/**/*.py", recursive=True) + glob.glob(f"{directory}/*.py")

def extract_streamlit_titles(filepath):
    """Extraherar page_title och st.title() från en Python-fil"""
    page_title = None
    st_title = None
    
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            
            # Sök efter page_title
            page_title_match = re.search(r'page_title\s*=\s*["\']([^"\']+)["\']', content)
            if page_title_match:
                page_title = page_title_match.group(1)
                
                # Ta bort eventuellt "| Juridiskt AI-system" suffix för jämförelse
                if " | " in page_title:
                    page_title = page_title.split(" | ")[0].strip()
            
            # Sök efter st.title()
            st_title_match = re.search(r'st\.title\(["\']([^"\']+)["\']', content)
            if st_title_match:
                st_title = st_title_match.group(1)
                
                # Om titeln börjar med emoji, ta bort den för jämförelse
                emoji_pattern = re.compile(r'[\U00010000-\U0010ffff][\u200d]*[\U00010000-\U0010ffff]*')
                st_title = emoji_pattern.sub('', st_title).strip()
                
    except Exception as e:
        print(f"Fel vid läsning av {filepath}: {e}")
        
    return page_title, st_title

def check_unique_page_titles():
    """Kontrollerar att alla page_title och st.title() är unika"""
    all_files = scan_files()
    
    # Samla alla page_title och st.title från filer
    page_titles = {}
    st_titles = {}
    
    # Samla också information om vilka sidor som saknar titlar
    missing_page_title = []
    missing_st_title = []
    
    for file in all_files:
        if "pycache" in file or ".git" in file:
            continue
            
        page_title, st_title = extract_streamlit_titles(file)
        
        # Registrera titlar om de finns
        if page_title:
            if page_title in page_titles:
                page_titles[page_title].append(file)
            else:
                page_titles[page_title] = [file]
        else:
            missing_page_title.append(file)
            
        if st_title:
            if st_title in st_titles:
                st_titles[st_title].append(file)
            else:
                st_titles[st_title] = [file]
        else:
            missing_st_title.append(file)
    
    # Hitta duplicerade titlar
    duplicated_page_titles = {title: files for title, files in page_titles.items() if len(files) > 1}
    duplicated_st_titles = {title: files for title, files in st_titles.items() if len(files) > 1}
    
    # Skriv ut resultaten
    print("\n" + "="*80)
    print(colored("KONTROLLRAPPORT: UNIKA SIDTITLAR", "cyan", attrs=["bold"]))
    print("="*80)
    
    print("\n" + "-"*40)
    print(colored("PAGE_TITLE KONTROLL", "yellow", attrs=["bold"]))
    print("-"*40)
    
    if duplicated_page_titles:
        print(colored("\n❌ DUPLICERADE PAGE_TITLE HITTADES:", "red", attrs=["bold"]))
        for title, files in duplicated_page_titles.items():
            print(f"\n  {colored(title, 'red')} används i följande filer:")
            for file in files:
                print(f"    - {file}")
    else:
        print(colored("\n✅ ALLA PAGE_TITLE ÄR UNIKA!", "green", attrs=["bold"]))
    
    print("\n" + "-"*40)
    print(colored("ST.TITLE() KONTROLL", "yellow", attrs=["bold"]))
    print("-"*40)
    
    if duplicated_st_titles:
        print(colored("\n❌ DUPLICERADE ST.TITLE() HITTADES:", "red", attrs=["bold"]))
        for title, files in duplicated_st_titles.items():
            print(f"\n  {colored(title, 'red')} används i följande filer:")
            for file in files:
                print(f"    - {file}")
    else:
        print(colored("\n✅ ALLA ST.TITLE() ÄR UNIKA!", "green", attrs=["bold"]))
    
    # Summering
    print("\n" + "="*80)
    print(colored("SAMMANFATTNING", "cyan", attrs=["bold"]))
    print("="*80)
    
    print(f"\nTotalt antal filer: {len(all_files)}")
    print(f"Unika page_title: {len(page_titles)}")
    print(f"Unika st.title(): {len(st_titles)}")
    
    if duplicated_page_titles or duplicated_st_titles:
        print("\n" + colored("⚠️  ÅTGÄRD KRÄVS: Titlar måste vara unika för att undvika Streamlit URL-konflikter!", "red", attrs=["bold"]))
        return False
    else:
        print("\n" + colored("✅ INGA PROBLEM HITTADES: Alla titlar är unika!", "green", attrs=["bold"]))
        return True

if __name__ == "__main__":
    print("\nKontrollerar unika titlar i Streamlit-applikationen...")
    if check_unique_page_titles():
        sys.exit(0)
    else:
        # Returnera error code om dubblett hittas
        sys.exit(1)