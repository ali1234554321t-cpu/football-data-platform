import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPORTMONKS_API_TOKEN")

with open("data/raw/fixtures.json", "r") as file:
    fixtures = json.load(file)

all_events = []

for fixture in fixtures:
    fixture_id = fixture["id"]

    url = f"https://api.sportmonks.com/v3/football/fixtures/{fixture_id}"

    max_retries = 3

    for attempt in range(max_retries):

        response = requests.get(
            url,
            params={
                "api_token": token,
                "include": "events"
            }
        )

        print(
            f"Fixture {fixture_id} - Status Code: {response.status_code}"
        )

        if response.status_code == 200:

            data = response.json().get("data", {})

            events = data.get("events", [])

            for event in events:
                event["fixture_id"] = fixture_id
                all_events.append(event)

            break

        elif response.status_code == 429:

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                wait_time = int(retry_after)
            else:
                wait_time = 10

            print(
                f"Rate limit reached. Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)

        else:

            print(f"Failed to fetch fixture {fixture_id}")
            print(response.text)
            break

    time.sleep(2)

with open("data/raw/fixture_events.json", "w") as file:
    json.dump(all_events, file, indent=4)

print("\nFixture events ingestion finished")
print("Events saved to: data/raw/fixture_events.json")
print("Total events:", len(all_events))