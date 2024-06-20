import time
from datetime import datetime, timedelta
import threading
import MainFunctions


def get_next_run_time(interval_minutes):
    # Get the current time
    now = datetime.now()

    # Calculate the number of minutes to add to reach the next multiple of the interval
    minutes_to_add = (interval_minutes - (now.minute % interval_minutes)) % interval_minutes
    next_run_time = now + timedelta(minutes=minutes_to_add)

    # Set the seconds and microseconds to zero to align with the interval mark
    next_run_time = next_run_time.replace(second=0, microsecond=0)

    # If the next run time is in the past, add the interval to it
    if next_run_time <= now:
        next_run_time += timedelta(seconds=int(interval_minutes * 60 + 2))

    return next_run_time


def calculateRelativePrice(price, percent):
    newPrice = price + ((price * percent) / 100)
    return newPrice


def make_divisible_by_0_1(price):
    # Round the price to the nearest multiple of 0.1
    rounded_price = round(price * 10) / 10.0
    return rounded_price


def takeProfitAndStopLossLoop(interval_minutes, takeProfitPercent, stopLossPercent):
    nowTime = datetime.now()
    print(f"Inside take profit and sl function {nowTime}")
    while True:
        time.sleep(int(interval_minutes * 60))
        nowTime = datetime.now()
        print(f"takeProfitAndStopLoss task started {nowTime}")
        positionDetails = MainFunctions.getOpenPositions()
        print(positionDetails)
        averagePrice = positionDetails["avg_price"]
        positionId = positionDetails["id"]
        profitPrice = make_divisible_by_0_1(calculateRelativePrice(averagePrice, takeProfitPercent))
        stopLossPrice = make_divisible_by_0_1(calculateRelativePrice(averagePrice, -stopLossPercent))
        data, success = MainFunctions.takeProfitOrder(positionId=positionId, takeProfitPrice=profitPrice,
                                                      stopLossPrice=stopLossPrice)
        if success:
            print(data)
            break
    nowTime = datetime.now()
    print(f"takeProfitAndStopLoss task ended here  {nowTime}")


def task5m(interval_minutes, task_name, checkFunctionTuple, createOrderTuple, takeProfitStopLossTuple):
    intervalLength, buyRsiValue, buyRsiDelta, windowLength, pairName = checkFunctionTuple
    orderType, leverage, walletAmount, minimumMultipleQuantity = createOrderTuple
    takeProfitPercent, stopLossPercent = takeProfitStopLossTuple
    while True:
        next_run_time = get_next_run_time(interval_minutes)
        time_to_sleep = (next_run_time - datetime.now()).total_seconds()
        time.sleep(max(0, time_to_sleep))
        nowTime = datetime.now()
        print(f"5 minute task started at {nowTime}")
        start_time = time.time()
        latestClosedCandleRsiValue, priceData, buySignal = MainFunctions.checkBuySignal(intervalLength=intervalLength,
                                                                                        buyRsiValue=buyRsiValue,
                                                                                        buyRsiDelta=buyRsiDelta,
                                                                                        windowLength=windowLength,
                                                                                        pairName=pairName)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print(latestClosedCandleRsiValue)
        print("Execution time: ", execution_time, "milliseconds")
        if buySignal:
            if MainFunctions.checkOpenPosition():
                print("already have a open position not taking any action")
            else:
                print(f"No open position")
                if MainFunctions.checkOpenPosition():
                    print(f"cancelling all open positions")
                    MainFunctions.cancelAllOpenPositios()
                else:
                    print(f"not cancelling any position ")
                pricePerUnit = float(priceData['close'].iloc[-2])
                balance, lockedAmount, currency = MainFunctions.getUSDTData()
                walletAmountUSDT = balance
                data = MainFunctions.createOrder(pricePerUnit=pricePerUnit, pair=pairName, orderType=orderType,
                                                 leverage=leverage,
                                                 walletAmount=float(walletAmountUSDT),
                                                 minimumMultipleQuantity=float(minimumMultipleQuantity))
                print(data)
                print(f"trade done please check")
                takeProfitAndStopLossThread = threading.Thread(target=takeProfitAndStopLossLoop,
                                                               args=(0.25, takeProfitPercent, stopLossPercent))
                takeProfitAndStopLossThread.start()
                takeProfitAndStopLossThread.join()

        else:
            print(f"RSINotMET")
        nowTime = datetime.now()
        print(f"5 minute task ended   at {nowTime}")


def helpExternalSlAndTp(interval, takeProfitPercent, stopLossPercent):
    takeProfitAndStopLossThread = threading.Thread(target=takeProfitAndStopLossLoop,
                                                   args=(interval, takeProfitPercent, stopLossPercent))
    takeProfitAndStopLossThread.start()
    takeProfitAndStopLossThread.join()


if __name__ == "__main__":
    # pair information start
    intervalLength = "5m"
    buyRsiValue = 59.0
    buyRsiDelta = 2.5
    windowLength = 11
    takeProfitPercent = 2.5
    stopLossPercent = 0.5
    pairName = "B-BTC_USDT"
    orderType = "limit_order"
    leverage = 10
    balance, lockedAmount, currency = MainFunctions.getUSDTData()
    walletAmount = balance
    minimumMultipleQuantity = 0.001
    checkFunctionTuple = (intervalLength, buyRsiValue, buyRsiDelta, windowLength, pairName)
    createOrderTuple = (orderType, leverage, walletAmount, minimumMultipleQuantity)
    takeProfitStopLossTuple = (takeProfitPercent, stopLossPercent)
    # pair information ends
    flag = False
    if flag:
        helpExternalSlAndTp(0.25, takeProfitPercent, stopLossPercent)
    # start and join 5m thread
    thread_5_minutes = threading.Thread(target=task5m, args=(
        5, "5-Minute", checkFunctionTuple, createOrderTuple, takeProfitStopLossTuple))
    thread_5_minutes.start()
    thread_5_minutes.join()
