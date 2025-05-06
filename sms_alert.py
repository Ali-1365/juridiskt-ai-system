
import pandas as pd
from datetime import datetime, timedelta
from twilio.rest import Client
import json

# Läs konfiguration
with open("twilio_config.json", "r") as f:
    config = json.load(f)

account_sid = config["account_sid"]
auth_token = config["auth_token"]
from_number = config["from_number"]
to_number = config["to_number"]

client = Client(account_sid, auth_token)

# Läs Excel och filtrera kritiska mål
df = pd.read_excel("kritisk_åtgärdslista.xlsx")
df["Deadline"] = pd.to_datetime(df["Deadline"])
today = datetime.now().date()
df = df[df["Deadline"].dt.date <= today + timedelta(days=2)]

# Skicka SMS för varje kritiskt mål
if df.empty:
    print("Inga kritiska mål att skicka.")
else:
    for _, row in df.iterrows():
        msg = f"Mål {row['Mål-ID']} – {row['Risk']} risk, deadline {row['Deadline'].strftime('%Y-%m-%d')}. Åtgärd: {row['Åtgärd']}."
        message = client.messages.create(
            body=msg,
            from_=from_number,
            to=to_number
        )
        print(f"SMS skickat för {row['Mål-ID']}")
