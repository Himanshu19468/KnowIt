import time

import PriceGetter
from DataConverter import CommonUtils
import CoindcxInteraction
from datetime import datetime, timedelta


def rsiCheck(intervalLength, buyRsiValue, buyRsiDelta, windowLength, pairName):
    latestClosedCandleRsiValue, priceData, success = PriceGetter.calaculateRsi(window=windowLength,
                                                                               intervalLength=intervalLength,
                                                                               pairName=pairName)
    if success:
        if CommonUtils.betweenDeltaInclusive(value=latestClosedCandleRsiValue, num=buyRsiValue, loweDelta=buyRsiDelta,
                                             higherDelta=buyRsiDelta):
            return latestClosedCandleRsiValue, priceData, True
        else:
            return latestClosedCandleRsiValue, priceData, False
    else:
        time.sleep(1)
        return rsiCheck(intervalLength=intervalLength, buyRsiValue=buyRsiValue, buyRsiDelta=buyRsiDelta,
                        windowLength=windowLength, pairName=pairName)


def checkBuySignal(intervalLength, buyRsiValue, buyRsiDelta, windowLength, pairName):
    return rsiCheck(intervalLength=intervalLength, buyRsiValue=buyRsiValue, buyRsiDelta=buyRsiDelta,
                    windowLength=windowLength, pairName=pairName)


def checkAnyLatestOpenPosition(positions):
    key = "active_pos"
    for position in positions:
        if position[key] > 0.0:
            return True

    return False


def checkOpenPosition():
    positions, success = CoindcxInteraction.listPositions()
    if success:
        if checkAnyLatestOpenPosition(positions):
            print("already have a open position")
            return True
        else:
            print("not have any open position")
            return False
    else:
        time.sleep(1)
        return checkOpenPosition()


def getOpenPositions():
    positions, success = CoindcxInteraction.listPositions()
    if success and len(positions) > 0 and positions[0]["active_pos"] > 0:
        return positions[0]
    else:
        time.sleep(1)
        return getOpenPositions()


def checkOpenOrder():
    openOrderkey = "open"
    orders, success = CoindcxInteraction.getAllOrders(openOrderkey)
    if success:
        if len(orders) > 0:
            return True
        else:
            return False
    else:
        time.sleep(1)
        return checkOpenPosition()


def takeProfitOrder(positionId, takeProfitPrice, stopLossPrice):
    data, success = CoindcxInteraction.createTfAndSl(positionId=positionId, takeProfitPrice=takeProfitPrice,
                                                     stopLossPrice=stopLossPrice)
    if success:
        return data, success
    else:
        time.sleep(1)
        return takeProfitPrice()


def cancelAllOpenPositios():
    data, success = CoindcxInteraction.cancel_all_open_positions()
    if success:
        print("all open positions cancelled")
    else:
        time.sleep(1)
        cancelAllOpenPositios()


def createOrder(pricePerUnit, pair, orderType, leverage, walletAmount, minimumMultipleQuantity):
    data, success = CoindcxInteraction.createOrders(pricePerUnit=pricePerUnit, pair=pair, orderType=orderType,
                                                    leverage=leverage,
                                                    walletAmount=walletAmount,
                                                    minimumMultipleQuantity=minimumMultipleQuantity)
    if success:
        return data
    else:
        time.sleep(1)
        print("unable to make order")
        createOrder(pricePerUnit, pair, orderType, leverage, walletAmount, minimumMultipleQuantity)


def getAllBalance():
    allCoinsData, success = CoindcxInteraction.balanceGetter()
    if success:
        return allCoinsData
    else:
        time.sleep(1)
        return getAllBalance()


def getUSDTData():
    allCoinsData = getAllBalance()
    for coin in allCoinsData:
        if coin["currency"] == "USDT":
            return coin["balance"], coin["locked_balance"], coin["currency"]

    return 0, 0, "USDT"


if __name__ == "__main__":
    # checkOpenPosition()
    print(datetime.now())
