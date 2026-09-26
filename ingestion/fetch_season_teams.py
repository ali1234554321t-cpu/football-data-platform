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
        "include": "fixtures.participants"
    }
)

print("Status Code:", response.status_code)

if response.status_code == 200:

    data = response.json()

    fixtures = data.get("data", {}).get("fixtures", [])

    teams = {}

    for fixture in fixtures:

        participants = fixture.get("participants", [])

        for participant in participants:

            team_id = participant.get("id")

            if team_id:
                teams[team_id] = participant

    teams_list = list(teams.values())

    with open("data/raw/season_teams.json", "w") as file:
        json.dump(teams_list, file, indent=4)

    print("Season teams ingestion: SUCCESS")
    print("Unique teams:", len(teams_list))
    print("Saved to: data/raw/season_teams.json")

else:

    print("Season teams ingestion: FAILED")
    print(response.text)