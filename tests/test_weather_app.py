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
