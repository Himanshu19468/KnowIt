from DataConverter import CommonClass


def betweenInclusive(num, low, high):
    if low <= num <= high:
        return True
    return False


def betweenDeltaInclusive(value, num, loweDelta, higherDelta):
   return betweenInclusive(value, num - loweDelta, num + higherDelta)


def takeProfitBuy(tradeInfo: CommonClass.Trade, securityPrice, profitPercent):
    bought_price = tradeInfo.bought
    if (securityPrice - bought_price) * 100 >= profitPercent * bought_price:
        return True

    return False


def takeLossBuy(tradeInfo: CommonClass.Trade, securityPrice, lossPercent):
    bought_price = tradeInfo.bought
    if (securityPrice - bought_price) * 100 <= - lossPercent * bought_price:
        return True
    return False


def profitCalculate(amount, profitPercent):
    return amount + (amount * (profitPercent / 100))


def lossCalculate(amount, lossPercent):
    return amount - (amount * (lossPercent / 100))
