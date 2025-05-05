import datetime
import geocoder
import json
import time
from web import get_weather_info

_last_weather = None
_last_weather_time = 0

LOG_FILE = "logs/context_log.txt"

def log_context(msg: str):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
    # print(msg)

def inject_context(system_prompt: str) -> str:
    global _last_weather, _last_weather_time

    # Time
    now = datetime.datetime.now()
    now_str = now.strftime("%A, %B %d, %Y %I:%M %p")
    log_context(f"[Time] {now_str}")

    # Location
    g = geocoder.ip('me')
    city = g.city or "Toronto"
    country = g.country or "CA"
    location = f"{city}, {country}"
    log_context(f"[Location] {location}")

    # Weather (cached for 10 min)
    if time.time() - _last_weather_time > 600 or not _last_weather:
        try:
            with open("config.json") as f:
                api_key = json.load(f).get("weather_api_key", "")
            _last_weather = get_weather_info(city, country, api_key)
            _last_weather_time = time.time()
            log_context(f"[Weather - fetched] {_last_weather}")
        except Exception as e:
            _last_weather = "unknown"
            log_context(f"[Weather - error] {e}")
    else:
        log_context(f"[Weather - cached] {_last_weather}")

    # Inject all values
    return (
        system_prompt
        .replace("{current_time}", now_str)
        .replace("{location}", location)
        .replace("{weather}", _last_weather)
    )
