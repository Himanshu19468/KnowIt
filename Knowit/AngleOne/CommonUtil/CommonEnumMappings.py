privateKey = "OC1fqV7N"
time_mapping = {
    '1m': "ONE_MINUTE",
    '3m': "THREE_MINUTE",
    '5m': "FIVE_MINUTE",
    '10m': "TEN_MINUTE",
    "15m": "FIFTEEN_MINUTE",
    "30m" : "THIRTY_MINUTE",
    "1h" : "ONE_HOUR",
    "1d" : "ONE_DAY"
}

time_reverse_mapping = {
    'ONE_MINUTE': '1m',
    'THREE_MINUTE': '3m',
    'FIVE_MINUTE': '5m',
    'TEN_MINUTE': '10m',
    'FIFTEEN_MINUTE': '15m',
    'THIRTY_MINUTE': '30m',
    'ONE_HOUR': '1h',
    'ONE_DAY': '1d'
}


max_interval = {
    "ONE_MINUTE": 30,
    "THREE_MINUTE": 60,
    "FIVE_MINUTE": 100,
    "TEN_MINUTE": 100,
    "FIFTEEN_MINUTE": 200,
    "THIRTY_MINUTE": 200,
    "ONE_HOUR": 400,
    "ONE_DAY": 2000
}


def getMaxInterval(interval): # should be like 1m
    return max_interval[time_mapping[interval]];
