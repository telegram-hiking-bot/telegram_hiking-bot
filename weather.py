import requests

API_KEY = "ae51aaa17bd3f521d112965df4761828"
LAT = -23.1896   # São José dos Campos
LON = -45.8841

def get_hourly_forecast():
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={LAT}&lon={LON}&exclude=current,minutely,daily,alerts&units=metric&appid={API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["hourly"]
import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"Tempo em {city}: {description}, {temperature}°C"
    else:
        return f"Erro ao buscar o clima: {data.get('message', 'Erro desconhecido')}"

