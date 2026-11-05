import numpy as np
try:
    import pytest
except ImportError:
    pytest = None
from sklearn.pipeline import Pipeline
from challenge import RobustOutlierCapper

def test_capper_logic():
    X_train = np.array([
        [1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0], [9.0], [10.0]
    ])
    capper = RobustOutlierCapper(lower_percentile=10.0, upper_percentile=90.0)
    capper.fit(X_train)

    assert capper.lower_bound_ is not None
    assert capper.upper_bound_ is not None

    # Test con valores extremos fuera del rango aprendido
    X_test = np.array([[-100.0], [500.0]])
    X_trans = capper.transform(X_test)

    assert X_trans[0, 0] >= capper.lower_bound_[0]
    assert X_trans[1, 0] <= capper.upper_bound_[0]

def test_pipeline_integration():
    pipe = Pipeline([
        ("capper", RobustOutlierCapper(lower_percentile=5.0, upper_percentile=95.0))
    ])
    X = np.random.normal(0, 1, size=(100, 2))
    transformed = pipe.fit_transform(X)
    assert transformed.shape == (100, 2)
