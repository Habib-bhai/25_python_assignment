import requests
from pprint import pprint

API_KEY =  "5e2163d9fbbf011f78d48f0a8d891329"
city_name = input("Enter city name: ")

base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
weather_data = requests.get(base_url).json()

pprint(weather_data)