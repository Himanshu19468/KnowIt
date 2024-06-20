import hmac
import hashlib
import json
import time
import requests


def place_order_with_amount(api_key, api_secret, pair, side, price, amount, leverage=5):
    """
    Places an order on CoinDCX with a specified amount in USD and leverage.

    Parameters:
        api_key (str): Your CoinDCX API key.
        api_secret (str): Your CoinDCX API secret.
        pair (str): The trading pair (e.g., "B-BTC_USDT").
        side (str): "buy" or "sell".
        price (float): The price at which to place the order.
        amount (float): The amount in USD to trade.
        leverage (int): The leverage to use for the order (default is 5).

    Returns:
        dict: The response from the CoinDCX API.
    """
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"
    timestamp = int(round(time.time() * 1000))

    # Calculate the quantity to trade based on the amount and price
    quantity = (amount * leverage) / price

    body = {
        "timestamp": timestamp,
        "order": {
            "side": side,
            "pair": pair,
            "order_type": "limit_order",  # Use "limit_order" to specify the price
            "price": str(price),  # Ensure price is in string format
            "total_quantity": quantity,
            "leverage": leverage,  # Setting leverage
            "time_in_force": "good_till_cancel",  # Order remains active until canceled
            "hidden": False,
            "post_only": False
        }
    }

    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(bytes(api_secret, encoding='utf-8'), json_body.encode(), hashlib.sha256).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': api_key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    response_data = response.json()

    # Check if the order was successful
    if response.status_code == 200 and response_data.get("status") == "success":
        print("Order placed successfully!")
        return response_data
    else:
        print("Failed to place order. Error:", response_data)
        return response_data


# Example usage:
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    pair = "B-BTC_USDT"  # Example trading pair
    side = "buy"  # "buy" or "sell"
    price = 30000  # Example price per BTC
    amount = 10000  # Amount in USD to trade
    order_response = place_order_with_amount(api_key, api_secret, pair, side, price, amount)
    print(order_response)
