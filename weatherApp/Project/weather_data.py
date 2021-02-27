import urllib.request
import json


def get_weatherData(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data
