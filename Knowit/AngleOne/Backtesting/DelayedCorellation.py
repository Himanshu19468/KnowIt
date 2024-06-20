
from AngleOne.HistoricalData.HistoricalData2 import *
from tqdm import tqdm
import copy
from DataGetter import getNifty500StocksMetaData


def calculate(df1, df2, delayDays):
    # Shift one DataFrame by delay time
    # df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    # df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    df2_shifted = df2.copy()
    df2_shifted['timestamp'] += pd.DateOffset(days=delayDays)

    # Merge the shifted DataFrame with the original DataFrame
    merged_df = pd.merge(df1, df2_shifted, on='timestamp', how='inner')
    correlation = merged_df['Close_x'].corr(merged_df['Close_y'])
    return correlation





def allStockMetaDataWithData(nifty500StocksMetaData, timeFrameTickSize, start_date, end_date):
    nifty500StocksMetaDataWithData = []
    for row in tqdm(nifty500StocksMetaData):
        messages = getData(start_date, end_date, timeFrameTickSize, row[0], row[7])
        df = zipAll(messages)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        deep_copy_row = copy.deepcopy(row)
        deep_copy_row.append(df)
        nifty500StocksMetaDataWithData.append(deep_copy_row)
    return nifty500StocksMetaDataWithData


def calculateCorelationBetweenTwo(df1, df2, delay):
    correlation = calculate(df1, df2, delay)
    return correlation


def analyzeCorelation(correlations):
    correlation_df = pd.DataFrame(correlations, columns=['StockA', 'StockB', 'Correlation'])
    correlation_df['Abs_Correlation'] = correlation_df['Correlation'].abs()
    sorted_correlations = correlation_df.sort_values(by='Abs_Correlation', ascending=False)

    sorted_correlations.to_excel("correlations.xlsx", index=False, engine='openpyxl')


def main(nifty500StocksMetaDataWithData, delay):
    n = len(nifty500StocksMetaDataWithData)
    correlations = []
    for i in tqdm(range(0, n)):
        for j in range(i, n):
            row1 = nifty500StocksMetaDataWithData[i]
            row2 = nifty500StocksMetaDataWithData[j]
            correlation = calculateCorelationBetweenTwo(row1[-1], row2[-1], delay)
            correlations.append((row1[2], row2[2], correlation))
    analyzeCorelation(correlations)


if __name__ == "__main__":
    nifty500StocksMetaData = getNifty500StocksMetaData()

    start_date = '2023-12-08 09:16'
    end_date = '2024-05-8 09:16'
    timeFrameTickSize = "1d"  # 1m , 5m , 15m, 30m, 1d
    nifty500StocksMetaDataWithData = allStockMetaDataWithData(nifty500StocksMetaData, timeFrameTickSize, start_date,
                                                              end_date)

    delay = 10  # days to delay
    main(nifty500StocksMetaDataWithData, delay)
