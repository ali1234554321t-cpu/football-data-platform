import os
import json
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
    data = response.json()

    with open("data/raw/leagues.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Leagues ingestion: SUCCESS")
    print("Leagues saved to: data/raw/leagues.json")

else:
    print("Leagues ingestion: FAILED")
    print(response.text)
