
class DataSteam:

    def __init__(self, pandasDataFrame): # pandas dataframe [open,high,close,low,volume,timeFrame]
        self.openSteam = pandasDataFrame['Open'].values
        self.closeSteam = pandasDataFrame['Close'].values
        self.lowSteam = pandasDataFrame['Low'].values
        self.highStean = pandasDataFrame['High'].values
        self.volumeSteam = pandasDataFrame['Volume'].values


    def len(self):
        return len(self.openSteam)

