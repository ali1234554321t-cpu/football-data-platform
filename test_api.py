import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPORTMONKS_API_TOKEN")

url = "https://api.sportmonks.com/v3/football/leagues"

response = requests.get(
    url,
    params={"api_token": token}
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("API Connection: SUCCESS")
    data = response.json()
    print("Leagues returned:", len(data.get("data", [])))
else:
    print("API Connection: FAILED")
    print(response.text)
