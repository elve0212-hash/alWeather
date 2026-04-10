import argparse
import sys
import requests


def fetch_weather(city: str) -> dict:
    """Fetch weather JSON from wttr.in for the given city."""
    url = f"https://wttr.in/{city}?format=j1"
    resp = requests.get(url, timeout=10, headers={"User-Agent": "weather-app/1.0"})
    resp.raise_for_status()
    return resp.json()


def summarize(data: dict, city: str) -> str:
    cur = data.get("current_condition", [{}])[0]
    temp = cur.get("temp_C", "?")
    desc = cur.get("weatherDesc", [{}])[0].get("value", "")
    humidity = cur.get("humidity", "?")
    wind = cur.get("windspeedKmph", "?")
    return f"Weather in {city}: {desc}, {temp}°C — Humidity {humidity}% — Wind {wind} km/h"


def main(argv=None):
    p = argparse.ArgumentParser(description="Simple weather lookup by city (wttr.in)")
    p.add_argument("--city", "-c", help="City name to lookup (e.g. London)")
    args = p.parse_args(argv)

    city = args.city
    if not city:
        try:
            city = input("Enter city: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("No city provided, exiting.")
            sys.exit(1)

    if not city:
        print("City cannot be empty.")
        sys.exit(1)

    try:
        data = fetch_weather(city)
        print(summarize(data, city))
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(2)
    except ValueError:
        print("Failed to parse weather response.")
        sys.exit(3)


if __name__ == "__main__":
    main()
