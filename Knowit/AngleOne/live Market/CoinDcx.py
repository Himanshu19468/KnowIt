apikey = "20128446895570498b729be12a50fcc8325794f79825dc3c"
secretKey = "d103831a78f70aabdfd2162d111bbfd5b64da65c11565458e0630f356f15fa35"









import requests

url = "https://public.coindcx.com/market_data/candles?pair=B-BTC_USDT&interval=5m"

response = requests.get(url)
data = response.json()
print(data)


