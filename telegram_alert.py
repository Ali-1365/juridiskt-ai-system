
import pandas as pd
import requests
import datetime
import json

# Läs konfiguration
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
CHAT_ID = config["chat_id"]

# Läs åtgärdslistan
df = pd.read_excel("kritisk_åtgärdslista.xlsx")
df["Deadline"] = pd.to_datetime(df["Deadline"])

# Filtrera mål med deadline inom 2 dagar
today = datetime.datetime.now().date()
df = df[df["Deadline"].dt.date <= today + datetime.timedelta(days=2)]

if df.empty:
    print("Inga kritiska mål att rapportera.")
else:
    for _, row in df.iterrows():
        message = f"""
⚠️ [AI-Strategi] Mål {row['Mål-ID']}
Riskprofil: {row['Risk']}
Deadline: {row['Deadline'].strftime('%Y-%m-%d')} ⏰
Rekommenderad åtgärd: {row['Åtgärd']}
Kommentar: {row['Kommentar']}
        """
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        r = requests.post(url, data=payload)
        print(f"Skickat till Telegram: {row['Mål-ID']}")
