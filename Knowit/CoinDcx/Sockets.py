import socketio
import hmac
import hashlib
import json
import time
import asyncio
from datetime import datetime
from socketio.exceptions import TimeoutError
import os
import pandas as pd
import aiohttp

socketEndpoint = 'wss://stream.coindcx.com'
sio = socketio.AsyncClient()

key = "20128446895570498b729be12a50fcc8325794f79825dc3c"
secret = "d103831a78f70aabdfd2162d111bbfd5b64da65c11565458e0630f356f15fa35"

# python3
secret_bytes = bytes(secret, encoding='utf-8')
channelName = "coindcx"
body = {"channel": channelName}
json_body = json.dumps(body, separators=(',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()


async def ping_task():
    while True:
        await asyncio.sleep(25)
        try:
            await sio.emit('ping', {'data': 'Ping message'})
        except Exception as e:
            print(f"Error sending ping: {e}")


@sio.event
async def connect():
    print("I'm connected!")
    current_time = datetime.now()
    print("Connected Time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

    await sio.emit('join', {'channelName': "coindcx", 'authSignature': signature, 'apiKey': key})
    await sio.emit('join', {'channelName': "B-BTC_USDT@trades-futures"})


@sio.on('new-trade')
async def on_message(response):
    current_time = datetime.now()
    print("dataReceived time :", current_time.strftime("%Y-%m-%d %H:%M:%S"))

    process_trade_event(response)


csv_file_path = "trade_data.csv"
columns = ["timestamp", "received_timestamp", "price", "quantity", "market", "symbol", "price_reason"]
df = pd.DataFrame(columns=columns)
if not os.path.exists(csv_file_path):
    df.to_csv(csv_file_path, index=False)


def process_trade_event(event):
    global df
    trade_data = json.loads(event['data'])

    # Extract relevant fields
    trade = {
        "timestamp": trade_data["T"],
        "received_timestamp": trade_data["RT"],
        "price": float(trade_data["p"]),
        "quantity": float(trade_data["q"]),
        "market": trade_data["m"],
        "symbol": trade_data["s"],
        "price_reason": trade_data["pr"]
    }

    # Convert to DataFrame
    trade_df = pd.DataFrame([trade])

    # Append to the main DataFrame
    df = pd.concat([df, trade_df], ignore_index=True)

    # Save the updated DataFrame to CSV (append mode)
    trade_df.to_csv(csv_file_path, mode='a', header=False, index=False)


async def main():
    try:
        await sio.connect(socketEndpoint, transports='websocket')
        # Wait for the connection to be established
        asyncio.create_task(ping_task())

        await sio.wait()
        while True:
            sio.event('new-trade', {'channelName': "B-BTC_USDT@trades-futures"})
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        raise  # re-raise the exception to see the full traceback


# Run the main function

if __name__ == '__main__':
    asyncio.run(main())
