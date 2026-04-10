import os
import sys
from flask import Flask, render_template, request
import json

# Ensure project root is on sys.path so imports work when running this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from weather_app import fetch_weather, summarize, get_weather_details

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = ""
    error = None
    message = None
    if request.method == "POST":
        # Clear cache action
        if request.form.get("clear"):
            try:
                from weather_app import clear_cache

                clear_cache()
                message = "Cache cleared."
            except Exception as e:
                error = f"Error clearing cache: {e}"
        else:
            city = request.form.get("city", "").strip()
            if not city:
                error = "Please enter a city."
            else:
                try:
                    data = fetch_weather(city)
                    weather = summarize(data, city)
                    details = get_weather_details(data, city)
                    raw_json = json.dumps(data, indent=2)
                except Exception as e:
                    error = f"Error: {e}"
    return render_template(
        "index.html",
        weather=weather,
        city=city,
        error=error,
        message=message,
        weather_details=locals().get("details"),
        raw_json=locals().get("raw_json"),
    )


if __name__ == "__main__":
    app.run(debug=True)
