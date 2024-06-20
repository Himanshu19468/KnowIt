import yfinance as yf


def download_data(ticker, start_date, end_date, interval):
    """
    Download minute-level stock data.

    Parameters:
    - ticker: The ticker symbol of the stock (e.g., 'RELIANCE.NS'.). or check on yahoo 
    - start_date: The start date of the period (format: 'YYYY-MM-DD').
    - end_date: The end date of the period (format: 'YYYY-MM-DD').
    - interval : 1m', '2m', '5m', '15m', '30m', '60m','90m , 1h, 1d, 5d, 1wk , 1mo, 3mo

    Returns:
    - data: DataFrame containing the historical stock data.
    """
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data


def download_minute_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "1m")
    return data

def download_15minute_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "15m")
    return data

def download_5minute_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "5m")
    return data

def download_30minute_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "30m")
    return data

def download_1hminute_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "1h")
    return data


def download_day_data(ticker, start_date, end_date):
    data = download_data(ticker, start_date, end_date, "1d")
    return data


if __name__ == "__main__": # test
    ticker_symbol = 'RELIANCE.NS'
    start_date = '2024-02-01'
    end_date = '2024-03-2'
    minute_data = download_day_data(ticker_symbol, start_date, end_date)
    for column_name in minute_data:
        print(column_name)
    print(minute_data.head())
