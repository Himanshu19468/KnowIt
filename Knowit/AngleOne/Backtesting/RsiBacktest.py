import csv
import warnings

import pandas_ta as ta
from backtesting import Backtest
from backtesting import Strategy
from niftystocks import ns
from openpyxl import Workbook

from AngleOne.HistoricalData.HistoricalData2 import *
from DataConverter import CommonUtils

output_file_path = '/Users/mmt11312/Desktop/Knowit/AngleOne/CommonUtil/equity.csv'
import multiprocessing as mp

# Suppress DeprecationWarnings
warnings.filterwarnings("ignore", category=UserWarning)


class RsiOscillator(Strategy):
    buyRSIvalue = 20
    buyRSIvalueDelta = 2.5
    rsi_window = 14
    tp = 5
    sl = 2.5

    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.df['Close']), self.rsi_window)
        # self.rsi = self.I(RSI.getRsi(self.data.df))

    def next(self):
        price = self.data['Close'][-1]

        if CommonUtils.betweenDeltaInclusive(self.rsi[-1], self.buyRSIvalue, self.buyRSIvalueDelta,
                                             self.buyRSIvalueDelta) and not self.position:
            self.buy(sl=(1 - (self.sl / 100)) * price, tp=(1 + (self.tp / 100)) * price)


wb = Workbook()
ws = wb.active


def saveToExcel(row):
    ws.append(row)


mp.set_start_method('fork')

with open(output_file_path, mode='r', newline='') as file:
    reader = csv.reader(file)
    ans = ns.get_nifty500()
    # Skip the header
    next(reader, None)
    # Iterate over each row in the CSV
    flag = True
    i = 1
    for row in reader:
        ticker_symbol = row[1]
        nsme = row[2]
        if not nsme in ans:
            continue
        if (not nsme in ans) or row[0] != '20825':
            continue
        start_date = '2023-12-08 09:16'
        end_date = '2024-04-24 09:16'
        messages = getData(start_date, end_date, "30m", row[0], row[7])
        df = zipAll(messages)
        bt = Backtest(df, RsiOscillator, cash=10_000)
        stats = bt.optimize(
            buyRSIvalue=range(20, 85, 1),
            rsi_window=range(10, 20, 1),
            maximize='Return [%]')
        print(i, float(stats['Return [%]']), row[0], nsme, stats['_strategy'])
        temp = [i, float(stats['Return [%]']), row[0], nsme, str(stats['_strategy'])]
        saveToExcel(temp)
        i += 1
        if (flag):
            print(stats)
            bt.plot()
            break

wb.save('returns_nifty_500_5min.xlsx')
