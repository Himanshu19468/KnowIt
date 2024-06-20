import hmac
import hashlib
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "20128446895570498b729be12a50fcc8325794f79825dc3c"
secret = "d103831a78f70aabdfd2162d111bbfd5b64da65c11565458e0630f356f15fa35"
secret_bytes = bytes(secret, encoding='utf-8')
secret_bytes = bytes(secret_bytes)


def createOrders(pricePerUnit, pair, orderType, leverage, walletAmount, minimumMultipleQuantity):
    try:
        totalAmountAfterLeverage = walletAmount * leverage
        totalQuantiyCanBuy = totalAmountAfterLeverage / pricePerUnit
        multipleOfQuantity = totalQuantiyCanBuy / minimumMultipleQuantity
        quantity_to_buy = (int(multipleOfQuantity)) * minimumMultipleQuantity
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp,  # EPOCH timestamp in seconds
            "order": {
                "side": "buy",  # buy OR sell
                "pair": pair,  # instrument.string
                "order_type": orderType,  # market_order OR limit_order
                "price": str(pricePerUnit),  # numeric value
                "total_quantity": quantity_to_buy,  # numerice value
                "leverage": leverage,  # numerice value
                "notification": "email_notification",  # no_notification OR email_notification OR push_notification
                "time_in_force": "good_till_cancel",  # good_till_cancel OR fill_or_kill OR immediate_or_cancel
                "hidden": False,  # True or False
                "post_only": False  # True or False
            }
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        print(data)
        success = True
        return data, success
    except:
        success = False
        return None, success


od = "52b116b2-2590-11ef-a228-33edf381c0b2"


def printData(data):
    for i in data:
        print(json.dumps(i, indent=4))


def cancelOrder(order_id):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "id": order_id  # order.id
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/cancel"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    try:
        printData(data)
    except:
        print("printing another way", data)
    return data


def listPositions():
    try:
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp,  # EPOCH timestamp in seconds
            "page": "1",  # no. of pages needed
            "size": "10"  # no. of records needed
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        success = True
        return data, success
    except:
        success = False
        return None, success


def cancel_all_open_positions():
    try:
        timeStamp = int(round(time.time() * 1000))

        body = {
            "timestamp": timeStamp  # EPOCH timestamp in seconds
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/cancel_all_open_orders"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        success = True
        return data, success
    except:
        success = False
        return None, success


def getAllOrders(orderStatus):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "status": orderStatus,  # Comma separated statuses as open,filled,cancelled
        "side": "buy",  # buy OR sell
        "page": "1",  # // no.of pages needed
        "size": "10"  # // no.of records needed
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    try:
        success = True
        return data, success
    except:
        success = False
        return data, success


def exitPosition(order_id):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "id": order_id  # position.id
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/exit"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    try:
        printData(data)
    except:
        print("printing another way", data)
    return data


def createTfAndSl(positionId, takeProfitPrice, stopLossPrice):
    try:
        print(positionId, takeProfitPrice, stopLossPrice)
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp,  # EPOCH timestamp in seconds
            "id": positionId,  # position.id
            "take_profit": {
                "stop_price": str(takeProfitPrice),
                "limit_price": str(takeProfitPrice),  # required for take_profit_limit orders
                "order_type": "take_profit_market"  # take_profit_limit OR take_profit_market
            },
            "stop_loss": {
                "stop_price": str(stopLossPrice),
                "limit_price": str(stopLossPrice),  # required for stop_limit orders
                "order_type": "stop_market"  # stop_limit OR stop_market
            }
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/create_tpsl"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        success = True
        return data, success
    except:
        return [], False


def getTrade(order_id):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "pair": "B-BTC_USDT",  # instrument.pair
        "order_id": order_id,  # order.id
        "from_date": "2023-01-01",  # format YYYY-MM-DD
        "to_date": "2024-06-08",  # format YYYY-MM-DD
        "page": "1",  # no. of pages needed
        "size": "10"  # no. of records needed
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/trades"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    try:
        printData(data)
    except:
        print("printing another way", data)


def getTransaction():
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "position_ids": "17baebc0-4d92-4194-829a-d14016253751",  # Comma separated position.id
        "stage": "all",  # all OR default OR funding
        "page": "1",  # no. of pages needed
        "size": "10"  # no. of records needed
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/transactions"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    printData(data)


def balanceGetter():
    try:
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/users/balances"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        allCoinsData = response.json()
        success = True
        return allCoinsData, success
    except:
        success = False
        return None, success


if __name__ == "__main__":
    usdt = 40
    price_perunit = 69412.00
    # createOrders(usdt, price_perunit)
    odi = "12152150-259c-11ef-b31f-d3c57c7af42f"
    data, _ = getAllOrders("filled")
    # print(data)
    # data, _ = listPositions()  # to get active position use active_pos and "avg_price": 69288.9,
    # printData(data)
    # getTrade(odi)
    # getTransaction()
    data, success = listPositions()
    data,success = balanceGetter()
    printData(data)
