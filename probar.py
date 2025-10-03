import requests

url = "https://fastapiopensearch-production.up.railway.app/sync_firebase"
resp = requests.post(url)

print(resp.status_code)
print(resp.json())
