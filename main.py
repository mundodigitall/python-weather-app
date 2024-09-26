import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Solicitar la clave de API al iniciar la aplicación
API_KEY = input("Por favor, introduce tu clave de API de OpenWeatherMap: ")

@app.route('/')
def hello_world():
    return 'Bienvenido a la aplicación del clima!'

@app.route('/clima')
def obtener_clima():
    ciudad = request.args.get('ciudad', 'Madrid')  # Ciudad por defecto: Madrid
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        descripcion = data['weather'][0]['description']
        return f"El clima en {ciudad}: {descripcion}, temperatura: {temp}°C"
    else:
        return "No se pudo obtener la información del clima", 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
