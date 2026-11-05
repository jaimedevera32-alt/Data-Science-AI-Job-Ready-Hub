import numpy as np
import pandas as pd

def slow_adjusted_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Implementación de referencia ingenua y lenta O(N) en Python puro."""
    adjusted = []
    for _, row in df.iterrows():
        if row["category"] == "LUXURY":
            adjusted.append(row["amount"] * 1.15)
        elif row["category"] == "ESSENTIAL":
            adjusted.append(row["amount"] * 0.95)
        else:
            adjusted.append(row["amount"])
    df["adjusted_amount"] = adjusted
    return df

def vectorized_adjusted_amount(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Tu solución vectorizada usando np.select o np.where.
    No debe usar bucles for, iterrows(), ni .apply().
    """
    conditions = [
        df["category"] == "LUXURY",
        df["category"] == "ESSENTIAL",
    ]
    choices = [
        df["amount"] * 1.15,
        df["amount"] * 0.95,
    ]
    df["adjusted_amount"] = np.select(conditions, choices, default=df["amount"])
    return df

