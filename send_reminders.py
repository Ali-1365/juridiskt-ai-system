
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import json

# Läs konfiguration
with open("config.json", "r") as f:
    config = json.load(f)

SMTP_SERVER = config["email_settings"]["smtp_server"]
SMTP_PORT = config["email_settings"]["smtp_port"]
SENDER_EMAIL = config["email_settings"]["sender_email"]
APP_PASSWORD = config["email_settings"]["app_password"]
RECIPIENTS = config["recipients"]

# Läs Excel-filen
today = datetime.date.today()
df = pd.read_excel("kritisk_åtgärdslista.xlsx")

# Filtrera mål med deadline inom 2 dagar och inte markerade som 'klar'
df["Deadline"] = pd.to_datetime(df["Deadline"]).dt.date
filtered = df[
    (df["Deadline"] <= today + datetime.timedelta(days=2)) &
    (df["Dokumentstatus"].str.lower() != "klar")
]

if not filtered.empty:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[AI-Strategi] {len(filtered)} kritiska mål inför deadline – {today.strftime('%-d %B %Y')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)

    html = "<h3>Kritiska mål (AI-strategi)</h3><ul>"
    for _, row in filtered.iterrows():
        html += f"<li><strong>Mål:</strong> {row['Mål-ID']}<br>"
        html += f"<strong>Riskprofil:</strong> {row['Risk']}<br>"
        html += f"<strong>Deadline:</strong> {row['Deadline']} ⏰<br>"
        html += f"<strong>Rekommenderad åtgärd:</strong> {row.get('Åtgärd', '–')}<br>"
        html += f"<strong>Kommentar:</strong> {row.get('Kommentar', '–')}</li><br>"

    html += "</ul><p>Vänligen prioritera dessa mål för omedelbar åtgärd.</p>"

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
