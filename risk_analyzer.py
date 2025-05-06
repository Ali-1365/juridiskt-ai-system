"""
risk_analyzer.py
Analyserar juridisk risk per argument, bevis, domstol och processfas.
Returnerar klassificering: Låg / Medel / Hög.
"""

import json

# Grundviktning
VIKTNING = {
    "argument": {"primär": 3, "alternativ": 2, "stödjande": 1},
    "bevis": {"exakt": 3, "indirekt": 2, "stödjande": 1},
    "autenticitet": {"original": 2, "kopia": 1},
    "process": {"huvudförhandling": 3, "överklagande": 2, "inlaga": 1},
    "tidsrisk": {"preskription": 3, "formfel": 2, "brådska": 1}
}

def analysera_argument(argument):
    poäng = VIKTNING["argument"].get(argument.get("viktighet"), 1)
    return poäng

def analysera_bevis(bevis):
    relevans = VIKTNING["bevis"].get(bevis.get("relevans"), 1)
    autent = VIKTNING["autenticitet"].get(bevis.get("autenticitet"), 1)
    return relevans + autent

def analysera_process(process):
    fas = VIKTNING["process"].get(process.get("fas"), 1)
    risk = VIKTNING["tidsrisk"].get(process.get("tidsrisk"), 1)
    return fas + risk

def total_riskprofil(data):
    total = 0
    maxpoäng = 0

    for a in data.get("argument", []):
        total += analysera_argument(a)
        maxpoäng += 3

    for b in data.get("bevisning", []):
        total += analysera_bevis(b)
        maxpoäng += 5

    total += analysera_process(data.get("process", {}))
    maxpoäng += 6

    kvot = total / maxpoäng if maxpoäng else 0
    if kvot >= 0.75:
        return "Låg"
    elif kvot >= 0.4:
        return "Medel"
    else:
        return "Hög"
