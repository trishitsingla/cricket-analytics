import json
import os
import pandas as pd

DATA_PATH = "data/raw/cricsheet_json"

rows = []

for file in os.listdir(DATA_PATH):

    if not file.endswith(".json"):
        continue

    with open(f"{DATA_PATH}/{file}") as f:
        match = json.load(f)

    match_id = file.replace(".json", "")

    match_info = match.get("info", dict())
    match_type = match_info.get("match_type", "")
    gender =  match_info.get("gender", "")
    city = match_info.get("city", "")
    event = match_info.get("event", dict())
    event_name = event.get("name", "")
    dates = match_info.get("dates", [])
    start_date = dates[0]
    end_date = dates[-1]
    innings = match.get("innings", [])

    for inning_index, inning in enumerate(innings, start=1):

        # ----------------
        # NEW FORMAT
        # ----------------
        if isinstance(inning, dict) and "overs" in inning:

            team = inning.get("team")

            for over in inning["overs"]:

                over_num = over.get("over")

                for ball_num, delivery in enumerate(over.get("deliveries", []), start=1):

                    runs = delivery.get("runs", {})

                    rows.append({
                        "match_id": match_id,
			"match_type": match_type,
			"city": city,
			"event": event_name,
			"start_date": start_date,
			"end_date": end_date,
			"gender": gender,
                        "inning": inning_index,
                        "batting_team": team,
                        "over": over_num,
                        "ball": ball_num,
                        "batter": delivery.get("batter"),
                        "bowler": delivery.get("bowler"),
                        "runs_batter": runs.get("batter", 0),
                        "runs_total": runs.get("total", 0),
                        "wicket": 1 if "wickets" in delivery else 0
                    })

        # ----------------
        # OLD FORMAT
        # ----------------
        elif isinstance(inning, dict):

            inning_name = list(inning.keys())[0]
            inning_data = inning.get(inning_name)

            if not isinstance(inning_data, dict):
                continue

            team = inning_data.get("team")

            deliveries = inning_data.get("deliveries", [])

            for delivery in deliveries:

                ball_key = list(delivery.keys())[0]
                info = delivery.get(ball_key)

                if not isinstance(info, dict):
                    continue

                runs = info.get("runs", {})

                over = int(float(ball_key))
                ball = int((float(ball_key) - over) * 10)

                rows.append({
                    "match_id": match_id,
		    "match_type": match_type,
		    "city": city,
	    	    "event": event_name,
		    "start_date": start_date,
		    "end_date": end_date,
		    "gender": gender,
                    "inning": inning_index,
                    "batting_team": team,
                    "over": over,
                    "ball": ball,
                    "batter": info.get("batsman"),
                    "bowler": info.get("bowler"),
                    "runs_batter": runs.get("batsman", 0),
                    "runs_total": runs.get("total", 0),
                    "wicket": 1 if "wicket" in info else 0
                })

df = pd.DataFrame(rows)

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/deliveries.csv", index=False)

print("Rows created:", len(df))