import types


def test_summarize():
    from weather_app import summarize

    data = {
        "current_condition": [
            {
                "temp_C": "15",
                "weatherDesc": [{"value": "Sunny"}],
                "humidity": "30",
                "windspeedKmph": "5",
            }
        ]
    }

    out = summarize(data, "TestCity")
    assert "Sunny" in out and "15°C" in out


def test_fetch_weather_monkeypatched(monkeypatch):
    import requests

    class DummyResponse:
        def __init__(self):
            self._json = {
                "current_condition": [
                    {
                        "temp_C": "20",
                        "weatherDesc": [{"value": "Cloudy"}],
                        "humidity": "50",
                        "windspeedKmph": "10",
                    }
                ]
            }

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    def fake_get(url, timeout, headers):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    from weather_app import fetch_weather

    data = fetch_weather("SomeCity")
    assert isinstance(data, dict)
    assert "current_condition" in data


def test_disk_cache(monkeypatch, tmp_path):
    import requests
    import os

    cache_file = tmp_path / ".weather_cache.json"

    class DummyResponseA:
        def __init__(self):
            self._json = {"current_condition": [{"temp_C": "20", "weatherDesc": [{"value": "Cloudy"}], "humidity": "50", "windspeedKmph": "10"}]}

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    class DummyResponseB(DummyResponseA):
        def __init__(self):
            self._json = {"current_condition": [{"temp_C": "99", "weatherDesc": [{"value": "Storm"}], "humidity": "1", "windspeedKmph": "200"}]}

    def fake_get_a(url, timeout, headers):
        return DummyResponseA()

    def fake_get_b(url, timeout, headers):
        return DummyResponseB()

    # Ensure module uses our temp cache file
    import weather_app
    weather_app._CACHE_FILE = str(cache_file)

    # First call returns A
    monkeypatch.setattr(requests, "get", fake_get_a)
    data1 = weather_app.fetch_weather("CacheCity", ttl=60)
    assert data1["current_condition"][0]["temp_C"] == "20"

    # Now replace HTTP result but cached value should persist
    monkeypatch.setattr(requests, "get", fake_get_b)
    data2 = weather_app.fetch_weather("CacheCity", ttl=60)
    assert data2["current_condition"][0]["temp_C"] == "20"

    # Expire cache by using ttl=0
    data3 = weather_app.fetch_weather("CacheCity", ttl=0)
    assert data3["current_condition"][0]["temp_C"] == "99"


def test_clear_cache(tmp_path):
    import weather_app
    p = tmp_path / ".weather_cache.json"
    weather_app._CACHE_FILE = str(p)
    # create a fake cache file
    p.write_text('{"x": 1}', encoding="utf-8")
    assert p.exists()
    weather_app.clear_cache()
    # either removed or emptied
    if p.exists():
        assert p.read_text(encoding="utf-8") in ("{}", "")
