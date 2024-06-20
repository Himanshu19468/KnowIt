import http.client
import mimetypes
import json

conn = http.client.HTTPSConnection(
    "apiconnect.angelbroking.com"
)
payload = """{\n\"clientcode\":\"H57730738\"
            ,\n\"password\":\"7838\"\n
		,\n\"totp\":\"378402\"\n}"""
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-PrivateKey': 'OC1fqV7N'
}
conn.request("POST", "/rest/auth/angelbroking/user/v1/loginByPassword", payload, headers)

res = conn.getresponse()
data = res.read()
parsed_message = json.loads(data)
print(parsed_message)
print(parsed_message.get('data').get("jwtToken"))

# JWT  = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Ikg1NzczMDczOCIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUp6ZFdJaU9pSklOVGMzTXpBM016Z2lMQ0psZUhBaU9qRTNNVEE1TnpJMk9Ua3NJbWxoZENJNk1UY3hNRGczTkRBMk1Td2lhblJwSWpvaU1UUTFNVFV3TTJRdFpqTmtNaTAwT0dVd0xXSTRPVFl0WWpneFlXWTJaRFkyWmpBMUlpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk1Td2ljMjkxY21ObGFXUWlPaUl6SWl3aWRYTmxjbDkwZVhCbElqb2lZMnhwWlc1MElpd2lkRzlyWlc1ZmRIbHdaU0k2SW5SeVlXUmxYMkZqWTJWemMxOTBiMnRsYmlJc0ltZHRYMmxrSWpveExDSnpiM1Z5WTJVaU9pSXpJaXdpWkdWMmFXTmxYMmxrSWpvaU0yTTJOV1kzTW1JdFlUUm1OeTB6TXpVNUxXRTBPRFF0WXpBeFl6ZzNaR016WW1Oa0lpd2lZV04wSWpwN2ZYMC5Gc2dNX2t1SDR6Rm4tTERPQlNUclFoVjNFcUU5b2FZZkg0WTBuVktOQ0lZRWtIQlpHRk5taWw1bE04TmdJOTNvRTVhVzdRbTU1RTRxQkpoWDBuVzJvUSIsIkFQSS1LRVkiOiJPQzFmcVY3TiIsImlhdCI6MTcxMDg3NDEyMSwiZXhwIjoxNzEwOTcyNjk5fQ.fT2yLHT4gQrJ7uWoc4_68WUz6FvuScOXz2S7s93QsonO6UAfihKM0ZCUBmh2X0t6g6UIG0F_rP8Ec00NYVo4uQ"
# import http.client
#
# conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
# payload = """{\r\n     \"exchange\": \"NSE\",\r\n
#  \"symboltoken\": \"3045\",\r\n     \"interval\": \"ONE_MINUTE\",\r\n
#     \"fromdate\": \"2021-02-08 09:00\",\r\n     \"todate\": \"2021-03-08 09:16\"\r\n}"""
# headers = {
#   'X-PrivateKey': 'OC1fqV7N',
#   'Accept': 'application/json',
#   'X-SourceID': 'WEB',
#   'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
#   'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
#   'X-MACAddress': 'MAC_ADDRESS',
#   'X-UserType': 'USER',
#   'Authorization': f'Bearer {JWT}',
#   'Accept': 'application/json',
#   'X-SourceID': 'WEB',
#   'Content-Type': 'application/json'
# }
# conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))
