import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPORTMONKS_API_TOKEN")

season_id = 27897

url = f"https://api.sportmonks.com/v3/football/seasons/{season_id}"

response = requests.get(
    url,
    params={
        "api_token": token,
        "include": "fixtures"
    }
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    fixtures = data.get("data", {}).get("fixtures", [])

    with open("data/raw/fixtures.json", "w") as file:
        json.dump(fixtures, file, indent=4)

    print("Fixtures ingestion: SUCCESS")
    print("Season:", season_id)
    print("Fixtures saved to: data/raw/fixtures.json")
    print("Fixtures returned:", len(fixtures))

else:
    print("Fixtures ingestion: FAILED")
    print(response.text)
