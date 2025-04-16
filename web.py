import requests

def get_weather_info(city="Ottawa", country="CA", api_key="YOUR_API_KEY"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            return f"{desc}, {temp}°C"
        else:
            return "Unable to fetch weather info"
    except:
        return "Weather service error"
