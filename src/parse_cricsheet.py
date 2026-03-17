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

    match_info = match.get("info", {})
    match_type = match_info.get("match_type", "")
    gender =  match_info.get("gender", "")
    city = match_info.get("city", "")
    event = match_info.get("event", {})
    event_name = event.get("name", "")
    dates = match_info.get("dates", [])
    start_date = dates[0] if dates else ""
    end_date = dates[-1] if dates else ""
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
                    
                    # Extract the extras dictionary
                    extras_dict = delivery.get("extras", {})
                    wides = extras_dict.get("wides", 0)
                    noballs = extras_dict.get("noballs", 0)
                    byes = extras_dict.get("byes", 0)
                    legbyes = extras_dict.get("legbyes", 0)
                    penalty = extras_dict.get("penalty", 0)

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
                        "runs_extras": runs.get("extras", 0),
                        "runs_total": runs.get("total", 0),
                        "wides": wides,
                        "noballs": noballs,
                        "byes": byes,
                        "legbyes": legbyes,
                        "penalty": penalty,
                        # Wides = 0 balls faced. Everything else = 1 ball faced.
                        "is_ball_faced": 0 if wides > 0 else 1,
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
                
                # Extract the extras dictionary
                extras_dict = info.get("extras", {})
                wides = extras_dict.get("wides", 0)
                noballs = extras_dict.get("noballs", 0)
                byes = extras_dict.get("byes", 0)
                legbyes = extras_dict.get("legbyes", 0)
                penalty = extras_dict.get("penalty", 0)

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
                    "runs_extras": runs.get("extras", 0),
                    "runs_total": runs.get("total", 0),
                    "wides": wides,
                    "noballs": noballs,
                    "byes": byes,
                    "legbyes": legbyes,
                    "penalty": penalty,
                    # Wides = 0 balls faced. Everything else = 1 ball faced.
                    "is_ball_faced": 0 if wides > 0 else 1,
                    "wicket": 1 if "wicket" in info else 0
                })

df = pd.DataFrame(rows)

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/deliveries.csv", index=False)

print("Rows created:", len(df))