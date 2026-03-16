import pandas as pd

df = pd.read_csv("data/processed/deliveries.csv")

df["is_boundary"] = df["runs"].apply(lambda x: 1 if x >= 4 else 0)

df["dot_ball"] = df["runs"].apply(lambda x: 1 if x == 0 else 0)

df["phase"] = df["over"].apply(
    lambda x: "powerplay" if x < 6 else "middle" if x < 15 else "death"
)

df.to_csv("data/processed/ball_features.csv", index=False)

print("Feature file created")
