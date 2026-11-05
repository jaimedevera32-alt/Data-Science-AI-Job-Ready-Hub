import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class RobustOutlierCapper(BaseEstimator, TransformerMixin):
    def __init__(self, lower_percentile: float = 1.0, upper_percentile: float = 99.0):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.lower_bound_ = None
        self.upper_bound_ = None

    def fit(self, X, y=None):
        X_arr = np.asarray(X)
        self.lower_bound_ = np.percentile(X_arr, self.lower_percentile, axis=0)
        self.upper_bound_ = np.percentile(X_arr, self.upper_percentile, axis=0)
        return self

    def transform(self, X):
        if self.lower_bound_ is None or self.upper_bound_ is None:
            raise RuntimeError("Debes llamar a fit() antes de transform().")
        X_arr = np.asarray(X)
        return np.clip(X_arr, self.lower_bound_, self.upper_bound_)

