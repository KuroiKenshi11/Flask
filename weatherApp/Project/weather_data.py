import urllib.request
import json


def get_weatherData(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = urllib.request.urlopen(url)
    weather = json.loads(response.read())
    weather_info = {
        "city_name": weather["name"],
        "temp": str("{:.1f}").format((int(weather["main"]["temp"]) - 273)),
        "coord_lon": weather["coord"]["lon"],
        "coord_lat": weather["coord"]["lat"],
        "id": weather["id"],
        "main_weather": weather["weather"][0]["main"],
        "description": weather["weather"][0]["description"],
        "temp_feels_like": weather["main"]["feels_like"],
        "temp_min": str("{:.1f}").format((int(weather["main"]["temp_min"]) - 273)),
        "temp_max": str("{:.1f}").format((int(weather["main"]["temp_max"]) - 273)),
        "pressure": weather["main"]["pressure"],
        "humidity": weather["main"]["humidity"],
        "visibility": weather["visibility"],
        "wind_speed": weather["wind"]["speed"],
        "wind_deg": weather["wind"]["deg"],
        "clouds": weather["clouds"]["all"],
        "timezone": weather["timezone"],
        "country_code": weather["sys"]["country"],
    }
    return weather_info
