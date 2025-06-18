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
