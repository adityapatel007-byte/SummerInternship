import os
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# A secret key is needed for flashing messages
app.config['SECRET_KEY'] = 'a_super_secret_key' 

# Retrieve API key from environment
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker and API_KEY:
            # API URL for fetching stock quotes
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                
                # Check if the API returned valid data for the ticker
                if "Global Quote" in data and data["Global Quote"]:
                    quote = data["Global Quote"]
                    stock_data = {
                        "symbol": quote.get("01. symbol"),
                        "price": quote.get("05. price"),
                        "change": quote.get("09. change"),
                        "change_percent": quote.get("10. change percent")
                    }
                else:
                    flash(f"Could not find data for the ticker '{ticker}'. Please check the symbol and try again.")
            
            except requests.exceptions.RequestException as e:
                flash(f"Error connecting to the API: {e}")
        else:
            flash("Ticker symbol is required.")
            
    return render_template("index.html", stock_data=stock_data)

if __name__ == "__main__":
    app.run(debug=True)