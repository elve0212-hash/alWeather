# Weather CLI

Simple CLI to fetch current weather for a city using wttr.in (no API key required).

Usage

PowerShell:

```powershell
python -m pip install -r requirements.txt
python weather_app.py --city "London"
# or interactive
python weather_app.py
```

Notes

- Uses `wttr.in` JSON endpoint: `https://wttr.in/<city>?format=j1`.
- No API key required. For production usage consider OpenWeatherMap or caching.
