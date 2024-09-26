import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Reemplaza esto con tu propia API key de OpenWeatherMap
API_KEY = "tu_api_key_aqui"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('index.html', weather_data=weather_data)

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
    return None

if __name__ == '__main__':
    app.run(debug=True)