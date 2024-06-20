from DataConverter import CommonUtils
from DataConverter import DataframeToClassConvert
from DataConverter import CommonClass
from AngleOne.HistoricalData.HistoricalData2 import *
from PandasIndcator import RSI


def RSIRunner(securityPriceSteam: DataframeToClassConvert.DataSteam
              , RSISteamArray: list, buyRSIvalue: float, buyRSIvalueDelta: float, profitPercent: float,
              lossPercent: float, Amount: float):
    trade_Amount = Amount
    trade_count = 0
    tradeClose = True
    tradeInfoObject = None
    for i in range(0, len(RSISteamArray)):
        if RSISteamArray[i] == -1:
            continue
        if CommonUtils.betweenDeltaInclusive(RSISteamArray[i], buyRSIvalue, buyRSIvalueDelta,
                                             buyRSIvalueDelta) and tradeClose:  # make new trade if needed
            tradeClose = False
            tradeInfoObject = CommonClass.Trade('long', securityPriceSteam.closeSteam[i], -1, trade_Amount, False)
            # print(f" opened new trade")

        elif not tradeClose:  # closing old trade
            if CommonUtils.takeProfitBuy(tradeInfoObject, securityPriceSteam.closeSteam[i], profitPercent):
                trade_Amount = CommonUtils.profitCalculate(trade_Amount, profitPercent) - 400
                # print(f"new amount after profit {trade_Amount} ")
                trade_count += 1
                tradeClose = True

            if CommonUtils.takeLossBuy(tradeInfoObject, securityPriceSteam.closeSteam[i], lossPercent):
                trade_Amount = CommonUtils.lossCalculate(trade_Amount, lossPercent)
                # print(f"new amount after loss {trade_Amount}")
                trade_count += 1
                tradeClose = True

    return trade_Amount, trade_count









max_ = 0
line_ = ""


def start_end_rsi(ticker_symbol, data, rsi_value, delta, profit, loss, Amount):
    global max_, line_
    rsi = RSI.getRsi(data)
    new_amount, trade_count = RSIRunner(DataframeToClassConvert.DataSteam(data), rsi, rsi_value, delta, profit, loss,
                                        Amount)
    percent = (((new_amount - 400 * trade_count) - Amount) / Amount) * 100
    if max_ < percent:
        max_ = percent
        line_ = f"{ticker_symbol} rsi {rsi_value} profit {profit} loss {loss} percent {percent} trade count {trade_count}"


rsi_values = numbers = list(range(18, 85 + 1))
p = [[3, 1], [1.0, 0.5], [2.5, 1.5], [2, 1]]



import csv

output_file_path = '/Users/mmt11312/Desktop/Knowit/AngleOne/CommonUtil/equity.csv'

with open(output_file_path, mode='r', newline='') as file:
    reader = csv.reader(file)

    # Skip the header
    next(reader, None)
    # Iterate over each row in the CSV
    flag = True
    i = 0
    for row in reader:
        ticker_symbol = row[1]
        start_date = '2023-07-08 09:16'
        end_date = '2024-04-23 09:16'

        messages = getData(start_date, end_date, "1h", row[0], row[7])
        df = zipAll(messages)
        rsi = RSI.getRsi(df)
        for pp in rsi:
            print(pp)
        for u in p:
            for t in rsi_values:
                start_end_rsi(ticker_symbol, df, t, 2, u[0], u[1], 100000)
        print(str(i) + " "+ line_)
        i += 1
        max_ = 0

