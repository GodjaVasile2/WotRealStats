import requests
import config

params = {
    "type": "exact",
    "search": "Call_me_Vosi"
}

response = requests.get(config.id_url, params=params)
result = response.json()["data"][0]["account_id"]

# print(result)

params = {
    "account_id": result
}

stats = requests.get(config.stats_url, params=params)

print(stats.text)
