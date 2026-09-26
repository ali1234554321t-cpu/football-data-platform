import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPORTMONKS_API_TOKEN")

url = "https://api.sportmonks.com/v3/football/teams"

response = requests.get(
    url,
    params={"api_token": token}
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    with open("data/raw/teams.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Teams ingestion: SUCCESS")
    print("Teams saved to: data/raw/teams.json")
    print("Teams returned:", len(data.get("data", [])))

else:
    print("Teams ingestion: FAILED")
    print(response.text)
