import numpy as np
from Historic_Crypto import HistoricalData
from CoinDcx import *
import multiprocessing

import pandas_ta as ta
from backtesting import Backtest
from backtesting import Strategy

from AngleOne.HistoricalData.HistoricalData2 import *
from DataConverter import CommonUtils
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def hawkes_process(df, kappa: float):
    norm_lookback = 336
    df['atr'] = ta.atr(np.log(df['High']), np.log(df['Low']), np.log(df['Close']), norm_lookback)
    data = (np.log(df['High']) - np.log(df['Low'])) / df['atr']
    assert (kappa > 0.0)
    alpha = np.exp(-kappa)
    arr = data.to_numpy()
    output = np.zeros(len(data))
    output[:] = np.nan
    for i in range(1, len(data)):
        if np.isnan(output[i - 1]):
            output[i] = arr[i]
        else:
            output[i] = output[i - 1] * alpha + arr[i]
    return pd.Series(output, index=data.index) * kappa


def calculate_ti(data):
    # Calculate SMA(7) and SMA(65)
    data.ta.sma(length=7, append=True)
    data.ta.sma(length=65, append=True)

    # Calculate TI
    data['TI'] = (data['SMA_7'] / data['SMA_65']) * 100

    return data


class RsiOscillator(Strategy):
    buyRSIvalue = 32
    buyRSIvalueDelta = 0.5
    rsi_window = 11
    tp = 5
    sl = 2.5
    period = 1
    period2 = 1
    val = 1

    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.df['Close']), self.rsi_window)
        # self.ma = self.I(ta.ema, pd.Series(self.data.df['Close']), self.period)
        # self.ma2 = self.I(ta.ema, pd.Series(self.data.df['Close']), self.period2)
        # supertrend_df = ta.supertrend(pd.Series(self.data.df['High']), pd.Series(self.data.df['Low']), pd.Series(self.data.df['Close']))
        # print(list(supertrend_df.columns))
        # self.supertrend = self.I(lambda x: supertrend_df["SUPERTd_7_3.0"].to_numpy(), supertrend_df["SUPERTd_7_3.0"])
        sp = calculate_ti(self.data.df)
        self.p = self.I(lambda x: sp.to_numpy(), sp,overlay=False)

    def next(self):
        price = self.data['Close'][-1]

        if CommonUtils.betweenDeltaInclusive(self.rsi[-1], self.buyRSIvalue, self.buyRSIvalueDelta,
                                             self.buyRSIvalueDelta):
            if not self.position:
                self.buy(sl=(1 - (self.sl / 1000)) * price, tp=(1 + (self.tp / 1000)) * price)


#
Itr = 0
max_ = 0
max_string = "Hello"


def run(args):
    global Itr, max_, max_string
    df, buyRSIvalue, buyRSIvalueDelta, rsi_window, tp, sl, leverage, period, period2, val = args
    bt = Backtest(df, RsiOscillator, cash=10_000, margin=1 / leverage)
    strategy_kwargs = {
        'buyRSIvalue': buyRSIvalue,
        'buyRSIvalueDelta': buyRSIvalueDelta,
        'rsi_window': rsi_window,
        'tp': tp,
        'sl': sl,
        'period': period,
        'period2': period2,
        'val': val
    }
    stats = bt.run(**strategy_kwargs)
    stockReturn = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
    Itr += 1
    if max_ < float(stats["Return [%]"]):
        max_ = float(stats["Return [%]"])
        max_string = f"""{stats["_strategy"]} {stockReturn} % {stats["Return [%]"]}"""
    if Itr % 50 == 0:
        print(f"Total run function calls: {Itr}")
        print("max string",max_string)
    print(f"""{stats["_strategy"]} {stockReturn} % {stats["Return [%]"]}, {stats["Max. Drawdown [%]"]}""")
    print(max_string)
    print(stats)
    bt.plot()


if __name__ == "__main__":
    ticker = "BTC-USDT"
    granularity = 300
    start_date = "2023-11-19-00-00"  # YYYY-MM-DD-HH-MM
    end_date = "2023-11-21-00-00"
    df = HistoricalData(ticker=ticker, granularity=granularity, start_date=start_date,
                        end_date=end_date, verbose=False).retrieve_data()
    factor = 100000
    df["Close"] /= factor
    df["Low"] /= factor
    df["Open"] /= factor
    df["High"] /= factor
    print(df.head())
    buyRSIvalue = [29]
    buyRSIvalueDelta = 2.5
    rsi_window = [9]
    tp = [40]
    sl = 5
    start_time = time.time()
    # Create a pool of worker processes
    flag = False
    if flag:
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        # Prepare the arguments
        args = []
        totalIteration = 0
        for buyRsiValue_ in buyRSIvalue:
            for rsiWindow_ in rsi_window:
                for takeProfit in tp:
                    sl = [5]
                    for stopLoss in sl:
                        for i in range(1, 201):
                            for j in range(1, 201):
                                totalIteration += 1
                                args.append(
                                    (df, buyRsiValue_, buyRSIvalueDelta, rsiWindow_, takeProfit, stopLoss, 1, i, j))
        # Run the tasks in parallel
        print(f"start total Iteration {totalIteration}")
        pool.map(run, args)

        # Close the pool and wait for the work to finish
        pool.close()
        pool.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken by the for loop: {elapsed_time:.2f} seconds")
        print("last-----", max_string)
    else:
        ticker = "B-BTC_USDT"
        granularity = "5"  # '1' OR '5' OR '60' OR '1D'
        start_date = "2024-03-12 00:00"  # YYYY-MM-DD-HH-MM
        end_date = "2024-06-02 00:00"
        df = help(start_date, end_date, ticker, granularity)
        factor = 100000
        df["Close"] /= factor
        df["Low"] /= factor
        df["Open"] /= factor
        df["High"] /= factor
        df = df.set_index('time')
        print(df.shape)
        print(df.columns)
        print(df.head())
        u = np.arange(1, 2001, 1)

        run((df, 59, 2.5, 11, 25, 5, 1, 3, 1, 1))

    # time.sleep(60)

    # while(True):
    #     new = LiveCryptoData('BTC-USDT', verbose=False).return_data()
    #     print(new)
