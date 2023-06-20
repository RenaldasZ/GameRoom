import http.client
import json

conn = http.client.HTTPConnection("127.0.0.1", 8000)

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": "Token 2e8a9cbd2976a0846d1cb0304f583aaeb39d287d",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "user": 1,
  "score": 3
})

conn.request("POST", "/player/", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))