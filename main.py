import requests, os
from twilio.rest import Client

# Your own twilio account
account_sid = "Your own account_sid"
auth_token = "Your own auth_token"

# Your own OpenWeatherMap account
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
OWM_api_key = "Your own OWM_api_key"

# location: Seoul, Korea
weather_parameters = {
    "lat": 37.566536,
    "lon": 126.977966,
    "appid": OWM_api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_Endpoint, params=weather_parameters)
response.raise_for_status()

weather_data = response.json()
weather_data_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_data_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:   # code 700 : raining
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_="+Your twilio number",
        to="+Your phone number"
    )
    print(message.status)
