import json
import os
import pandas as pd

data_dir = "data/raw/cricsheet_json"
rows = []

for file in os.listdir(data_dir):
    if not file.endswith(".json"):
        continue

    path = os.path.join(data_dir, file)

    with open(path) as f:
        match = json.load(f)

    match_id = file.replace(".json", "")

    innings = match.get("innings", [])

    for inning in innings:
        inning_data = list(inning.values())[0]

        team = inning_data.get("team")

        for over in inning_data.get("overs", []):
            over_number = over["over"]

            for ball in over["deliveries"]:
                batter = ball["batter"]
                bowler = ball["bowler"]

                runs = ball["runs"]["total"]

                rows.append([
                    match_id,
                    team,
                    over_number,
                    batter,
                    bowler,
                    runs
                ])

df = pd.DataFrame(rows, columns=[
    "match_id",
    "batting_team",
    "over",
    "batter",
    "bowler",
    "runs"
])

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/deliveries.csv", index=False)

print("Rows created:", len(df))
