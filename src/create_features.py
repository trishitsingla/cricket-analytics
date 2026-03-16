import pandas as pd

df = pd.read_csv("data/processed/deliveries.csv")

# phase classification
def get_phase(over):
    if over < 6:
        return "powerplay"
    elif over < 15:
        return "middle"
    else:
        return "death"

df["phase"] = df["over"].apply(get_phase)

# ball number in innings
df["ball_in_innings"] = df["over"] * 6 + df["ball"]

# cumulative runs
df["cum_runs"] = df.groupby(["match_id","inning"])["runs_total"].cumsum()

# cumulative wickets
df["cum_wickets"] = df.groupby(["match_id","inning"])["wicket"].cumsum()

# balls remaining in innings
df["balls_remaining"] = 120 - df["ball_in_innings"]

# wickets remaining
df["wickets_remaining"] = 10 - df["cum_wickets"]

# run rate
df["run_rate"] = df["cum_runs"] / (df["ball_in_innings"] / 6)

df.to_csv("data/processed/ball_features.csv", index=False)

print("Feature dataset created")
print("Rows:", len(df))