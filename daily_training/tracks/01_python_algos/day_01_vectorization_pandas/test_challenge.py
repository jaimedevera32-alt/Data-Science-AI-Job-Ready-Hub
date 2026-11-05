import time
import numpy as np
import pandas as pd
try:
    import pytest
except ImportError:
    pytest = None
from challenge import vectorized_adjusted_amount, slow_adjusted_amount

def generate_sample_data(n=1000):
    categories = ["LUXURY", "ESSENTIAL", "REGULAR", "OTHER"]
    np.random.seed(42)
    return pd.DataFrame({
        "amount": np.random.uniform(10.0, 500.0, size=n),
        "category": np.random.choice(categories, size=n)
    })

def test_vectorized_matches_slow():
    df_raw = generate_sample_data(500)
    df_slow = slow_adjusted_amount(df_raw.copy())
    df_vec = vectorized_adjusted_amount(df_raw.copy())
    
    np.testing.assert_allclose(
        df_vec["adjusted_amount"].values,
        df_slow["adjusted_amount"].values,
        rtol=1e-5
    )

def test_speedup():
    df_large = generate_sample_data(50_000)
    
    t0 = time.perf_counter()
    _ = vectorized_adjusted_amount(df_large.copy())
    t_vec = time.perf_counter() - t0
    
    # Vectorized execution on 50k items should take less than 0.15 seconds
    assert t_vec < 0.20, f"Vectorized solution took too long: {t_vec:.4f}s"
