from flask import Flask, render_template, request
import requests

app = Flask(__name__)

WEATHERAPI_KEY = "44f147163aaa436d858153252250307"

@app.route("/", methods=["GET", "POST"])
def index():
    forecast = None
    city = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={city}&days=3&aqi=no&alerts=no"

        response = requests.get(url)

        if response.ok:
            data = response.json()
            forecast = []

            for day in data["forecast"]["forecastday"]:
                forecast.append({
                    "date": day["date"],
                    "temp": day["day"]["avgtemp_c"],
                    "condition": day["day"]["condition"]["text"],
                    "icon": "https:" + day["day"]["condition"]["icon"]
                })
        else:
            print("API error:", response.status_code, response.text)

    return render_template("index.html", forecast=forecast, city=city)

if __name__ == "__main__":
    app.run(debug=True)
