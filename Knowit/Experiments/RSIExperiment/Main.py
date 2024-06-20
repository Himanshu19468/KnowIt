from DataConverter import CommonUtils
from DataConverter import DataframeToClassConvert
from DataConverter import CommonClass
from OfflineDataGetter import YahooFinApi
from PandasIndcator import RSI
from AngleOne.HistoricalData import  HistoricalData2


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
                trade_Amount = CommonUtils.profitCalculate(trade_Amount, profitPercent)
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


def start_end_rsi(ticker_symbol, data, rsi_value, delta, profit, loss, Amount):
    global max_
    rsi = RSI.getRsi(data)
    new_amount, trade_count = RSIRunner(DataframeToClassConvert.DataSteam(data), rsi, rsi_value, delta, profit, loss,
                                        Amount)
    percent = (((new_amount - 400 * trade_count) - Amount) / Amount) * 100
    print(f"{ticker_symbol} rsi {rsi_value} profit {profit} loss {loss} percent {percent} trade count {trade_count}")
    max_ = max(max_, percent)


rsi_values = numbers = list(range(18, 85 + 1))
p = [[3, 1], [1.0, 0.5], [2.5, 1.5], [2, 1]]

ticker_symbol = 'ASHOKA.NS'
start_date = '2024-01-20'
end_date = '2024-03-16'
# data = YahooFinApi.download_15minute_data(ticker_symbol, start_date, end_date)
messages = HistoricalData2.getData("2021-03-08 09:16", "2022-03-13 09:16", "5m", "2885", "NSE")
data = HistoricalData2.zipAll(messages)
rsi = RSI.getRsi(data)

for u in p:
    for t in rsi_values:
        start_end_rsi(ticker_symbol, data, t, 2, u[0], u[1], 100000)

print(max_)
# minute_data = YahooFinApi.download_minute_data(ticker_symbol, start_date, end_date)
# print(minute_data['Close'])
# rsi = RSI.getRsi(minute_data)
# print(len(rsi))
# minute_data = DataframeToClassConvert.DataSteam(minute_data)
# RSIRunner(minute_data, rsi, 40, 2, 2, 1, 100000)
# print(rsi)
