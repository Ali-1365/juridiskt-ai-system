"""
precedent_simulator.py
AI-modul som simulerar prejudikatsanalys och identifierar potentiell rättsbildning.
"""

# Mock-databas för existerande prejudikat (kan ersättas med riktig rättsdatabas)
PREJUDIKAT_DB = [
    {
        "id": "NJA 2021 s. 563",
        "rättsområde": "civilrätt",
        "rättsfråga": "avtalsbrott",
        "avgörande": "HD slog fast att partsavsikt väger tyngre än ordalydelse i vissa kommersiella avtal.",
        "tolkning": "aktiv"
    },
    {
        "id": "HFD 2022 ref. 17",
        "rättsområde": "förvaltningsrätt",
        "rättsfråga": "rätt till sjukpenning",
        "avgörande": "HFD betonade att medicinsk underbyggnad måste vara tydlig även vid komplexa diagnoser.",
        "tolkning": "neutral"
    }
]

def simulera_prejudikat(data):
    rättsfråga = data.get("rättsfråga", "").lower()
    rättsområde = data.get("rättsområde", "").lower()
    träffar = []

    for p in PREJUDIKAT_DB:
        if rättsområde in p["rättsområde"] and rättsfråga in p["rättsfråga"]:
            träffar.append(p)

    prejudikatrisk = "låg"
    if len(träffar) >= 2:
        prejudikatrisk = "möjlig"
    if data.get("domstol", "").lower() == "högsta domstolen" and träffar:
        prejudikatrisk = "hög"

    return {
        "träffade_prejudikat": träffar,
        "simulerat_uttryck": f"Domstolen kan komma att tolka rättsfrågan som '{träffar[0]['tolkning']}' baserat på tidigare praxis." if träffar else "Ingen direkt prejudikatträff hittades.",
        "prejudikatrisk": prejudikatrisk
    }
