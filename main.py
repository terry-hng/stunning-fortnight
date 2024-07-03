import requests
import datetime as dt
import os

weather_icons_to_emoji = {
    "01d": "☀️",  # clear sky day
    "01n": "🌙",  # clear sky night
    "02d": "⛅",  # few clouds day
    "02n": "🌥️",  # few clouds night
    "03d": "🌥️",  # scattered clouds day
    "03n": "🌥️",  # scattered clouds night
    "04d": "☁️",  # broken clouds day
    "04n": "☁️",  # broken clouds night
    "09d": "🌧️",  # shower rain day
    "09n": "🌧️",  # shower rain night
    "10d": "🌦️",  # rain day
    "10n": "🌧️",  # rain night
    "11d": "⛈️",  # thunderstorm day
    "11n": "⛈️",  # thunderstorm night
    "13d": "🌨️",  # snow day
    "13n": "🌨️",  # snow night
    "50d": "🌫️",  # mist day
    "50n": "🌫️",  # mist night
}

discord_channel_url = "https://discord.com/api/v9/channels/1258018140307066992/messages"
headers = {
    "Authorization": os.environ.get(DISCORD_AUTH_KEY)
}  # auth key needed to send messages through discord

# for OpenWeather API
parameters = {
    "lat": 10.823099,
    "lon": 106.629662,
    "appid": os.environ.get(OPENWEATHER_API_KEY),
    "cnt": 6,
    "units": "metric",
    # "lang": "vi",
}

response = requests.get(
    url="http://api.openweathermap.org/data/2.5/forecast", params=parameters
)


response.raise_for_status()
weather_data = response.json()

# with open("data.json", "w") as file:
#     file.write(str(weather_data).replace("'", '"'))

message = f"> Weather forecast for {dt.datetime.now().strftime("%A, %B %d")}\n\n"

for forecast in weather_data["list"]:
    if forecast["dt"] > int(dt.datetime.now().timestamp()):
        weather_description = forecast["weather"][0]["description"].capitalize()

        temperature = int(forecast["main"]["temp"])

        time_of_forcast = (
            str(
                dt.datetime.fromtimestamp(
                    forecast["dt"], tz=dt.timezone.utc
                ).astimezone(dt.timezone(dt.timedelta(hours=7)))
            )
            .split(" ")[1]
            .split("+")[0][:-3]
        )

        weather_emoji = weather_icons_to_emoji[forecast["weather"][0]["icon"]]

        message += (
            f"- {time_of_forcast}: **{weather_description}**  {weather_emoji}\n\t\t\t\tTemp: {temperature}°C\n\n"
        )
        # break

        # print(int(dt.datetime.now().timestamp()))

payload = {"content": message + "---\n"}

res = requests.post(discord_channel_url, payload, headers=headers)
