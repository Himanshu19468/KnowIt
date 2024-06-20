import time

import numpy as np
import vectorbt as vbt
from AngleOne.Backtesting import CoinDcx
import copy
import multiprocessing
import warnings

warnings.filterwarnings('ignore')

bestStats = None
bestStrategyParamsObject = None


class StrategyParams:
    def __init__(self, buyRsi, buyRsiDelta, rsiWindow, takeProfit, stopLoss, iteration, simulationOn):
        self.buyRsiDelta = buyRsiDelta
        self.buyRsi = buyRsi
        self.rsiWindow = rsiWindow
        self.takeProfit = takeProfit
        self.stopLoss = stopLoss
        self.iteration = iteration
        self.simulationOn = simulationOn

    def print_attributes(self):
        # Using the __dict__ attribute to access instance variables
        attributes = ', '.join(f"{key}: {value}" for key, value in self.__dict__.items())
        print(attributes)


def getBestStats(stats, strategyParamsObject: StrategyParams):
    global bestStats, bestStrategyParamsObject
    if bestStats is None:
        bestStats = copy.deepcopy(stats)
        bestStrategyParamsObject = copy.deepcopy(strategyParamsObject)
        return

    returnKey = "Total Return [%]"
    if float(bestStats[returnKey]) > float(stats[returnKey]):
        return
    elif float(bestStats[returnKey]) < float(stats[returnKey]):
        bestStats = copy.deepcopy(stats)
        bestStrategyParamsObject = copy.deepcopy(strategyParamsObject)
        return

    winRateKey = "Win Rate [%]"
    if float(bestStats[winRateKey]) > float(stats[winRateKey]):
        return
    elif float(bestStats[winRateKey]) < float(stats[winRateKey]):
        bestStats = copy.deepcopy(stats)
        bestStrategyParamsObject = copy.deepcopy(strategyParamsObject)
        return

    maxDrawDownKey = "Max Drawdown [%]"
    if float(bestStats[maxDrawDownKey]) > float(stats[maxDrawDownKey]):
        return
    elif float(bestStats[maxDrawDownKey]) < float(stats[maxDrawDownKey]):
        bestStats = copy.deepcopy(stats)
        bestStrategyParamsObject = copy.deepcopy(strategyParamsObject)
        return


def getEntries(data, buyRsi, buyRsiDelta, window):
    rsi = vbt.RSI.run(data, window=window)
    rsi = rsi.rsi
    lower_bound = buyRsi - buyRsiDelta
    upper_bound = buyRsi + buyRsiDelta
    entries = (rsi >= lower_bound) & (rsi <= upper_bound)
    return entries


globalIteration = 0


def runSimulation(takeProfit, stopLoss, entries, closeData, strategyParamsObject: StrategyParams):
    global bestStats, bestStrategyParamsObject, globalIteration
    globalIteration += 1
    pf = vbt.Portfolio.from_signals(
        closeData,
        entries=entries,
        direction='longonly',
        sl_stop=stopLoss,
        tp_stop=takeProfit
    )
    if strategyParamsObject.simulationOn:
        getBestStats(stats=pf.stats(), strategyParamsObject=strategyParamsObject)
        if globalIteration % 100 == 0:
            print("  ")
            print(
                f' Iteration {globalIteration} Total return {bestStats["Total Return [%]"]} benchmark {bestStats["Benchmark Return [%]"]}  maxDrawDown {bestStats["Max Drawdown [%]"]} winRate {bestStats["Win Rate [%]"]}')
            strategyParamsObject.print_attributes()
            print("  ")
    else:
        print(pf.stats())


def master(arguments):
    data, strategyParamsObject = arguments
    closedData = data["Close"] / 100000
    entries = getEntries(data=closedData, buyRsi=strategyParamsObject.buyRsi,
                         buyRsiDelta=strategyParamsObject.buyRsiDelta, window=strategyParamsObject.rsiWindow)
    runSimulation(takeProfit=strategyParamsObject.takeProfit, stopLoss=strategyParamsObject.stopLoss, entries=entries,
                  closeData=closedData, strategyParamsObject=strategyParamsObject)


if __name__ == "__main__":
    start_date = '2023-11-27 09:16'
    end_date = '2024-05-24 09:16'
    ticker = "B-BTC_USDT"
    resolution = "5"
    btc_data = CoinDcx.help(startDate=start_date, endDate=end_date, ticker=ticker, resolution=resolution)
    simulationOn = True
    if simulationOn:
        buyRsiValues = np.arange(10, 90, 1, dtype=float)
        buyRsiDelta = 2.5
        windowValues = np.arange(4, 25, 1, dtype=int)
        takeProfitValues = np.arange(0.005, 0.05, 0.005, dtype=float)
        stopLossValues = np.arange(0.005, 0.05, 0.005, dtype=float)
        print(f"total cpu count {multiprocessing.cpu_count()}")
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        totalInterations = 0
        args = []
        for buyRsi in buyRsiValues:
            for window in windowValues:
                for takeProfit in takeProfitValues:
                    for stopLoss in stopLossValues:
                        totalInterations += 1
                        paramsObj = StrategyParams(buyRsi=buyRsi, buyRsiDelta=buyRsiDelta, rsiWindow=window,
                                                   takeProfit=takeProfit,
                                                   stopLoss=stopLoss, iteration=totalInterations,
                                                   simulationOn=simulationOn)
                        args.append((btc_data, paramsObj))

        print(f"total iterations required {totalInterations}")
        start_time = time.time()
        print(f"IterationPerCPU {int(totalInterations/multiprocessing.cpu_count())}")
        pool.map(master, args)
        pool.close()
        pool.join()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken by the for loop: {elapsed_time:.2f} seconds")

    else:
        buyRsi = 59.0
        buyRsiDelta = 2.5
        window = 11
        takeProfit = 0.025
        stopLoss = 0.005
        paramsObj = StrategyParams(buyRsi=buyRsi, buyRsiDelta=buyRsiDelta, rsiWindow=window, takeProfit=takeProfit,
                                   stopLoss=stopLoss, iteration=100, simulationOn=simulationOn)

        master((btc_data, paramsObj))
