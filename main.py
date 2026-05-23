import requests
import os
from datetime import datetime
from twilio.rest import Client

today = datetime.today()

api_id = os.environ.get("OWM_API_ID")
account_sid = os.environ.get("T_ACCOUNT_SID")
auth_token = os.environ.get("T_AUTH_TOKEN")
client = Client(account_sid, auth_token)

parameter = {
    "lat": 10,
    "lon": 15,
    "appid": api_id
}

response = requests.get("https://api.openweathermap.org/data/3.0/onecall", params=parameter)
response.raise_for_status()
weather_data = response.json()

is_raining_today = False
weather_data = [hourly_weather for hourly_weather in weather_data["hourly"] if datetime.fromtimestamp(hourly_weather["dt"]).strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d")]

for hourly_weather in weather_data:
    weather_id = int(hourly_weather["weather"][0]["id"])
    if weather_id >= 500:
        is_raining_today = True

if is_raining_today:
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+919884276761",
        body="Its going to rain today. Remember to bring an ☂️!"
    )
    print(message.body)
