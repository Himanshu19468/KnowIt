import requests
import pandas as pd
import pandas_ta as ta
import time


def current_stamp_to_epoch(delay_minutes=0):
    # Get the current time in seconds since the epoch
    current_time = time.time()

    # Add delay in seconds
    delayed_time = current_time - (delay_minutes * 60)

    return int(delayed_time)


def readData(data_dict):
    df = pd.DataFrame(data_dict['data'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.set_index('time')
    return df


def getData(intervalLength, pairName):
    url = "https://public.coindcx.com/market_data/candlesticks"
    query_params = {
        "pair": pairName,
        "from": current_stamp_to_epoch(200),
        "to": current_stamp_to_epoch(),
        "resolution": intervalLength,  # '1' OR '5' OR '60' OR '1D' "5m"
        "pcode": "f"
    }
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        data = response.json()
        data = readData(data)
        return data, True
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, False


def calaculateRsi(window, intervalLength, pairName):
    data, success = getData(intervalLength, pairName)
    if success:
        serise = ta.rsi(data['close'], length=window)
        return serise.iloc[-2], data, True
    else:
        return -1, False


def getLatestMinutePrice(intervalLength, pairName):
    data, success = getData(intervalLength, pairName)
    if success:
        return data['close'].iloc[-2]
    else:
        getLatestMinutePrice(intervalLength, pairName)


def getLatestPrice():
    data = getData()
    return data['close'].iloc[-1]


if __name__ == "__main__":
    for i in range(0, 1):
        start_time = time.time()
        calaculateRsi()
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Calculate the execution time in milliseconds
        print(getLatestMinutePrice())
        print("Execution time:", execution_time, "milliseconds")
