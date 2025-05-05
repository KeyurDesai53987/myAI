# myAI - Personal LLM-Powered Assistant

myAI is a personalized local AI assistant that supports voice, mood, weather, and even a Telegram bot interface. It can be run using either `llama-cpp-python` with GGUF models or Hugging Face Transformers + BitsAndBytes.

---

## 🔧 Features

- Chat via terminal or Telegram
- Switchable LLM backends: `llama-cpp` or `transformers` (via config)
- Mood detection with tone-aware replies
- Dynamic injection of:
  - Current time 🕒
  - Location 🌍
  - Weather ☁️
- Assistant personalization via system prompts
- Telegram bot with memory per user
- Assistant styles: Best Friend, Girlfriend, Spiritual Guide, etc.

---

## 📦 Requirements

- Python 3.10+
- `llama-cpp-python` (for GGUF models) OR `transformers`, `accelerate`, `bitsandbytes`
- `geocoder` for location detection
- `requests` for weather API
- `python-telegram-bot`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit `config.json`:

```json
{
  "llm_backend": "hf",  // or "llama-cpp"
  "hf_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "model_path": "models/phi-2.Q4_K_M.gguf",
  "telegram_token": "YOUR_BOT_TOKEN",
  "weather_api_key": "YOUR_OPENWEATHER_KEY",
  "default_user": "Keyur",
  "default_assistant": "Isha"
}
```

---

## ▶️ Running

### Terminal chat:
```bash
python main.py
```

### Telegram bot:
```bash
python tele_bot.py
```

---

## 📁 Folder Structure

- `main.py` – terminal-based assistant
- `tele_bot.py` – Telegram bot
- `llm_engine/` – backend loading (cpp or hf)
- `prompts/` – assistant and user profiles
- `web.py` – weather helper
- `context_injection.py` – inject time/location/weather into prompts
- `telegram_history/` – stores user chat history and names

---

## ✨ Assistant Profiles

Edit `prompts/assistant_profiles.json` to create custom assistant personalities. Supports `{user_name}`, `{current_time}`, `{location}`, `{weather}` placeholders.

---

## ☁️ Weather Support

Free from [OpenWeather](https://openweathermap.org/api), use `/data/2.5/weather` endpoint and set your key in `config.json`.

---

## 📬 Contact

Built with ❤️ by Keyur Desai