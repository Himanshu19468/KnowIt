import http.client
import time
import pandas as pd
import json
from tqdm import tqdm

from AngleOne.CommonUtil import CommonEnumMappings
from AngleOne.CommonUtil import CommonUtil

JWT = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Ikg1NzczMDczOCIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUp6ZFdJaU9pSklOVGMzTXpBM016Z2lMQ0psZUhBaU9qRTNNVFkyTnpnMU5UY3NJbWxoZENJNk1UY3hOalU0TkRnME1pd2lhblJwSWpvaU1UUXpObU00TWpjdE5tRXdOUzAwTWpsakxXSm1aRE10WlRFME5EUXpZVGt3WkdNeUlpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk1Td2ljMjkxY21ObGFXUWlPaUl6SWl3aWRYTmxjbDkwZVhCbElqb2lZMnhwWlc1MElpd2lkRzlyWlc1ZmRIbHdaU0k2SW5SeVlXUmxYMkZqWTJWemMxOTBiMnRsYmlJc0ltZHRYMmxrSWpveExDSnpiM1Z5WTJVaU9pSXpJaXdpWkdWMmFXTmxYMmxrSWpvaU0yTTJOV1kzTW1JdFlUUm1OeTB6TXpVNUxXRTBPRFF0WXpBeFl6ZzNaR016WW1Oa0lpd2lZV04wSWpwN2ZYMC5BY2R4QkkyZWNncWRYV004VjhKMjlTQkh0VXF0N3Rfd2VTd2g3QnFrTDdYbGhyci1vcl9JSmxzRnNzZGFPOVBLa2poakh0clIya1BYWnBhZkNKLTRKUSIsIkFQSS1LRVkiOiJPQzFmcVY3TiIsImlhdCI6MTcxNjU4NDkwMiwiZXhwIjoxNzE2Njc4NTU3fQ.1yh_fFJ8XAH6R8B0fwNmemtfcy7hW2CAsKhSqaTd7T2pGlRXu0QgiZD7Dw6r7QOZOWWKaP3yGZ6qgJX3Dx8MtA"

def getDataDateSpecific(startDate, endDate, interval, symbolToken, exchange):
    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
    payload = """
            {{
                "exchange": "{exchange}",
                "symboltoken": "{symbolToken}",
                "interval": "{interval}",
                "fromdate": "{startDate}",
                "todate": "{endDate}"
            }}"""
    payload = payload.format(exchange=exchange, symbolToken=symbolToken, interval=interval, startDate=startDate,
                             endDate=endDate)

    headers = {
        'X-PrivateKey': CommonEnumMappings.privateKey,
        'Accept': 'application/json',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
        'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
        'X-MACAddress': 'MAC_ADDRESS',
        'X-UserType': 'USER',
        'Authorization': f'Bearer {JWT}',
        'Accept': 'application/json',
        'X-SourceID': 'WEB',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def getData(startDate, endDate, interval, symbolToken, exchange):
    DateList = CommonUtil.break_dates(startDate, endDate, CommonEnumMappings.getMaxInterval(interval))
    # DateList = CommonUtil.break_dates(startDate, endDate, 1)
    messages = []
    for dates in DateList:
        messages.append(getDataDateSpecific(dates[0], dates[1], CommonEnumMappings.time_mapping[interval] , symbolToken, exchange))
        time.sleep(0.5)
    return messages

def zipAll(messages):
    all_data = []
    # Process each message
    for message in messages:
        # Parse the JSON message
        parsed_message = json.loads(message)

        # Extract the 'data' field
        status = parsed_message.get("status")
        data = parsed_message.get("data", [])

        # Extend the all_data list with the contents of data

        if status:
            all_data.extend(data)
        if not status:
            print(parsed_message)

        # Create a pandas DataFrame with the specified columns
    df = pd.DataFrame(all_data, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
    return df

# test
# messages = getData("2021-03-08 09:16", "2022-03-13 09:16", "5m", "3045", "NSE")
# df = zipAll(messages)



