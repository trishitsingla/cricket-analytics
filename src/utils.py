import pandas as pd
import numpy as np

# =========================
# PHASE MAPPING
# =========================

def add_match_phase(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds phase column based on match_type and over
    """

    conditions = [
        # ODI / ODM
        df['match_type'].isin(['ODI', 'ODM']) & (df['over'] < 10),
        df['match_type'].isin(['ODI', 'ODM']) & (df['over'] >= 10) & (df['over'] < 40),
        df['match_type'].isin(['ODI', 'ODM']) & (df['over'] >= 40),

        # T20 formats
        df['match_type'].isin(['T20', 'IT20', 'T20I']) & (df['over'] < 6),
        df['match_type'].isin(['T20', 'IT20', 'T20I']) & (df['over'] >= 6) & (df['over'] < 15),
        df['match_type'].isin(['T20', 'IT20', 'T20I']) & (df['over'] >= 15)
    ]

    choices = [
        "powerplay", "middle", "death",
        "powerplay", "middle", "death"
    ]

    df["phase"] = np.select(conditions, choices, default="Test")

    return df


# =========================
# UTILITY: OVERS FORMAT
# =========================

def balls_to_overs(balls_series: pd.Series) -> pd.Series:
    """
    Convert balls to cricket overs format (e.g., 62 -> 10.2)
    """

    return (
        (balls_series // 6).astype(int).astype(str)
        + "."
        + (balls_series % 6).astype(int).astype(str)
    )
