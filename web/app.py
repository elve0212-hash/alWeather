import os
import sys
from flask import Flask, render_template, request

# Ensure project root is on sys.path so imports work when running this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from weather_app import fetch_weather, summarize

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
                except Exception as e:
                    error = f"Error: {e}"
    return render_template("index.html", weather=weather, city=city, error=error, message=message)


if __name__ == "__main__":
    app.run(debug=True)
