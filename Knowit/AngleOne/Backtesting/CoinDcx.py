import requests
from datetime import datetime
import time
import json
import pandas as pd
from AngleOne.CommonUtil import CommonUtil


def convert_to_epoch(date_str):
    """
    Convert a date string in the format YYYY-MM-DD-HH-MM to epoch time.

    Parameters:
    date_str (str): Date string in the format YYYY-MM-DD-HH-MM

    Returns:
    int: Epoch time in seconds
    """
    date_format = "%Y-%m-%d %H:%M"
    date_dt = datetime.strptime(date_str, date_format)
    return int(time.mktime(date_dt.timetuple()))


def readData(data_dict):
    df = pd.DataFrame(data_dict['data'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    return df


def getData(start_date, end_date, ticker, resolution):
    url = "https://public.coindcx.com/market_data/candlesticks"
    query_params = {
        "pair": ticker,
        "from": start_date,
        "to": end_date,
        "resolution": resolution,  # '1' OR '5' OR '60' OR '1D'

    }
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        data = response.json()
        df = readData(data)
        return df
    else:
        print(f"Error: {response.status_code}, {response.text}")


def help(startDate, endDate, ticker, resolution):
    DateList = CommonUtil.break_dates(startDate, endDate, 100)
    dfs = []
    for dates in DateList:
        dfs.append(getData(convert_to_epoch(dates[0]), convert_to_epoch(dates[1]), ticker, resolution))
        print("ok")
    df = pd.concat(dfs)
    df = df.rename(columns={'open': 'Open', 'high': 'High', 'close': 'Close', 'low': 'Low', 'volume': 'Volume'})
    return df

def marketData():
    url = "https://api.coindcx.com/exchange/v1/markets_details"

    response = requests.get(url)
    data = response.json()
    print(data)


if __name__ == "__main__":
    ticker = "B-BTC_USDT"
    granularity = "5"  # '1' OR '5' OR '60' OR '1D'
    start_date = "2023-11-19 00:00"  # YYYY-MM-DD-HH-MM
    end_date = "2024-06-02 00:00"
    #help(start_date, end_date, ticker, granularity)
    #marketData()
