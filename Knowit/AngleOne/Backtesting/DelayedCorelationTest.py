import vectorbt as vbt
import numpy as np
import pandas as pd
from AngleOne.HistoricalData.HistoricalData2 import *
from DataConverter import CommonUtils
from numba import njit




@njit
def adjust_sl_func_nb(c):
    # Calculate current profit
    return 0.025, True


@njit
def adjust_tp_func_nb(c):
    # Set take profit at 5% above entry price
    print(c)
    return 0.05, True


@njit
def rsi_entry_signal_nb(c, rsi_threshold=45):
    return c.rsi < rsi_threshold


def fun():
    start_date = '2023-12-08 09:16'
    end_date = '2024-04-24 09:16'
    messages = getData(start_date, end_date, "30m", "20825", "NSE")
    df = zipAll(messages)
    rsi = vbt.RSI.run(df['Close'], window=np.arange(2, 20, 1))

    entries = []
    exits = []
    rsi_val = 11
    rsi_delta = 2.5
    initial_capital = 1000000
    for i in rsi.rsi:
        if CommonUtils.betweenDeltaInclusive(i, rsi_val, rsi_delta, rsi_delta):
            entries.append(True)
        else:
            entries.append(False)
        exits.append(False)

    print("ok 1")
    portfolio = vbt.Portfolio.from_signals(
        df['Close'], entries, exits,
        direction='longonly',
        adjust_sl_func_nb=adjust_sl_func_nb,
        adjust_tp_func_nb=adjust_tp_func_nb
    )
    print("ok 2")

    stats = portfolio.stats()
    print(stats)

    portfolio.plot().show()




fun()
