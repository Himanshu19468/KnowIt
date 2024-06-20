import requests
import json

def get_bse_data(symbol):
    api_key = "ZMSBYN43BXXFGRLG"
    base_url = "https://www.alphavantage.co/query"

    # Define the parameters for the API request
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": f"{symbol}.BSE",  # Append .BSE to the stock symbol
        "outputsize": "full",       # Retrieve full historical data
        "apikey": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)

        # Process the data as needed (e.g., extract daily stock prices)
        # For demonstration purposes, let's print the first few data points
        for date, info in data["Time Series (Daily)"].items():
            print(f"Date: {date}, Close Price: {info['4. close']}")

    except Exception as e:
        print(f"Error fetching data: {e}")

# Example usage
get_bse_data("RELIANCE")

