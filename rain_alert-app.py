import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import os

load_dotenv()
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv('API_KEY')

weather_params = {
    "lat": 13.082680,
    "lon": 80.270721,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()

weather_data = response.json()
# print(weather_data)

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

def send_alert_mail():
    EMAIL_ADDRESS = "vishvender.soyogender18@gmail.com"
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    TO_EMAIL = "vishvender.soyogender18@gmail.com" 

    subject = "Rain alert application testing.."
    body = "It's going to rain today. Remember to bring an ☔️."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if will_rain:
    send_alert_mail()


