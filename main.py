import requests
import datetime as dt
import os

discord_channel_url = "https://discord.com/api/v9/channels/1258018140307066992/messages"
headers = {
    "Authorization": os.getenv("DISCORD_AUTH_KEY")
}  # auth key needed to send messages through discord

# for OpenWeather API
parameters = {
    "lat": 10.823099,
    "lon": 106.629662,
    "appid": os.getenv("OPENWEATHER_API_KEY"),
    "cnt": 8,
    "units": "metric",
    "lang": "vi",
}

response = requests.get(
    url="http://api.openweathermap.org/data/2.5/forecast", params=parameters
)


response.raise_for_status()
weather_data = response.json()

message = ""

for forecast in weather_data["list"]:
    if forecast["weather"][0]["id"] < 700 and forecast["dt"] > int(
        dt.datetime.now().timestamp()
    ):
        weather_description = forecast["weather"][0]["description"].capitalize()

        temperature = int(forecast["main"]["temp"])

        time_of_forcast = str(
            dt.datetime.fromtimestamp(forecast["dt"], tz=dt.timezone.utc).astimezone(
                dt.timezone(dt.timedelta(hours=7))
            )
        ).split("+")[0][:-3]

        message += (
            f"{time_of_forcast}: {weather_description}\nTemp: {temperature}°C\n\n"
        )
        # break

        # print(int(dt.datetime.now().timestamp()))

payload = {"content": message + "\n----"}

res = requests.post(discord_channel_url, payload, headers=headers)
