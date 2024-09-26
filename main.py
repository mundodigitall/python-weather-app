from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para manejar sesiones

# Plantilla HTML para la página principal
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Aplicación del Clima</title>
</head>
<body>
    <h1>Aplicación del Clima</h1>
    {% if api_key %}
        <form action="/buscar_clima" method="post">
            <input type="text" name="ciudad" placeholder="Introduce una ciudad">
            <input type="submit" value="Buscar Clima">
        </form>
        {% if clima %}
            <h2>{{ clima }}</h2>
        {% endif %}
    {% else %}
        <form action="/set_api_key" method="post">
            <input type="text" name="api_key" placeholder="Introduce tu API Key de OpenWeatherMap">
            <input type="submit" value="Guardar API Key">
        </form>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE, api_key=session.get('api_key'), clima=session.get('clima'))

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    api_key = request.form['api_key']
    session['api_key'] = api_key
    return redirect(url_for('index'))

@app.route('/buscar_clima', methods=['POST'])
def buscar_clima():
    ciudad = request.form['ciudad']
    api_key = session.get('api_key')
    if not api_key:
        return redirect(url_for('index'))

    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        descripcion = data['weather'][0]['description']
        session['clima'] = f"El clima en {ciudad}: {descripcion}, temperatura: {temp}°C"
    else:
        session['clima'] = "No se pudo obtener la información del clima"
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
