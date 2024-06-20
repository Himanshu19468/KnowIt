import csv
from niftystocks import ns
from AngleOne.HistoricalData.HistoricalData2 import *
from tqdm import tqdm
import copy


def allStocksMetaData():  # ye angleOne ke latest file se h
    output_file_path = '/Users/mmt11312/Desktop/Knowit/AngleOne/CommonUtil/equity.csv'
    with open(output_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)
        # Iterate over each row in the CSV
        nseRawMetaData = []
        for row in reader:
            nseRawMetaData.append(row)

    return nseRawMetaData


def getNifty500StocksMetaData():
    allNseRawMetaData = allStocksMetaData()

    latestNifty500Stocks = ns.get_nifty500()  # give a list of symbols

    nifty500StocksmetaData = []
    u = 0
    for row in allNseRawMetaData:
        nseName = row[2]
        if nseName in latestNifty500Stocks:
            nifty500StocksmetaData.append(row)
            u += 1
    return nifty500StocksmetaData


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
