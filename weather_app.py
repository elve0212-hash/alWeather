import argparse
import sys
import re
import json
import os
import time
import requests


def _normalize_city(city: str) -> str:
    """Normalize city input for consistent caching and safe URL usage."""
    if not city:
        return ""
    s = city.strip()
    # replace whitespace with + for wttr.in and remove control chars
    s = re.sub(r"\s+", "+", s)
    s = re.sub(r"[\x00-\x1f\x7f]+", "", s)
    return s


def _raw_fetch_weather(city: str) -> dict:
    """Perform the actual HTTP request to wttr.in (no caching)."""
    url = f"https://wttr.in/{city}?format=j1"
    resp = requests.get(url, timeout=10, headers={"User-Agent": "weather-app/1.0"})
    resp.raise_for_status()
    return resp.json()


_CACHE_FILE = None
_CACHE_TTL = 300  # seconds


def _cache_path():
    global _CACHE_FILE
    if _CACHE_FILE:
        return _CACHE_FILE
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    path = os.path.join(root, ".weather_cache.json")
    _CACHE_FILE = path
    return path


def _read_cache() -> dict:
    path = _cache_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_cache(d: dict) -> None:
    path = _cache_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f)
    except Exception:
        pass


def clear_cache() -> None:
    """Remove the cache file if it exists (best-effort)."""
    path = _cache_path()
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        try:
            # fallback: overwrite with empty dict
            _write_cache({})
        except Exception:
            pass


def fetch_weather(city: str, ttl: int = None) -> dict:
    """Fetch weather for a city, using a simple disk-backed TTL cache.

    `ttl` overrides the module default for tests.
    """
    norm = _normalize_city(city)
    if not norm:
        raise ValueError("empty city")

    if ttl is None:
        ttl = _CACHE_TTL

    now = int(time.time())
    cache = _read_cache()
    entry = cache.get(norm)
    if entry:
        ts = entry.get("ts", 0)
        if now - ts < ttl:
            return entry.get("data")

    data = _raw_fetch_weather(norm)
    try:
        cache[norm] = {"ts": now, "data": data}
        _write_cache(cache)
    except Exception:
        pass
    return data


def summarize(data: dict, city: str) -> str:
    cur = data.get("current_condition", [{}])[0]
    temp = cur.get("temp_C", "?")
    desc = ""
    try:
        desc = cur.get("weatherDesc", [{}])[0].get("value", "")
    except Exception:
        desc = ""
    humidity = cur.get("humidity", "?")
    wind = cur.get("windspeedKmph", "?")
    return f"Weather in {city}: {desc}, {temp}°C — Humidity {humidity}% — Wind {wind} km/h"


def get_weather_details(data: dict, city: str) -> dict:
    """Return structured weather details extracted from wttr.in JSON."""
    cur = data.get("current_condition", [{}])[0]
    desc = ""
    try:
        desc = cur.get("weatherDesc", [{}])[0].get("value", "")
    except Exception:
        desc = ""

    return {
        "city": city,
        "description": desc,
        "temp_C": cur.get("temp_C", "?"),
        "feels_like_C": cur.get("FeelsLikeC", cur.get("FeelsLikeF", "?")),
        "humidity": cur.get("humidity", "?"),
        "wind_kmph": cur.get("windspeedKmph", "?"),
        "precip_mm": cur.get("precipMM", "?"),
        "uv_index": cur.get("uvIndex", "?"),
        "visibility": cur.get("visibility", "?"),
        "raw": data,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Simple weather lookup by city (wttr.in)")
    p.add_argument("--city", "-c", help="City name to lookup (e.g. London)")
    p.add_argument("--clear-cache", dest="clear_cache", action="store_true", help="Clear disk cache and exit")
    args = p.parse_args(argv)

    city = args.city
    if args.clear_cache:
        clear_cache()
        print("Cache cleared.")
        sys.exit(0)
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
    except ValueError as e:
        print(f"Input error: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()
