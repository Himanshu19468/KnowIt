import pandas as pd


def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def getRsi(data):
    data['RSI'] = calculate_rsi(data['Close'])
    data = data.fillna(-1)
    return data['RSI'].values


if __name__ == "__main__":  # test
    data = pd.DataFrame({'Close': [50, 51, 52, 48, 47, 45, 46, 47, 49, 50, 48, 49, 52, 51]})
    data['RSI'] = calculate_rsi(data['Close'])
    data = data.fillna(-1)
    print(data['RSI'])
