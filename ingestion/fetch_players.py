import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPORTMONKS_API_TOKEN")

url = "https://api.sportmonks.com/v3/football/players"

response = requests.get(
    url,
    params={"api_token": token}
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    with open("data/raw/players.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Players ingestion: SUCCESS")
    print("Players saved to: data/raw/players.json")
    print("Players returned:", len(data.get("data", [])))

else:
    print("Players ingestion: FAILED")
    print(response.text)
