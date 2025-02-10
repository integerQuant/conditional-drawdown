from textwrap import fill
from typing import Union
import numpy as np
from numba import njit
import pandas as pd

@njit
def max_drawdown(returns: np.ndarray) -> float:
    """Computes the maximum drawdown of an array of returns.

    ## Parameters:
    returns (numpy.ndarray): 1D array of return values over time.

    ## Returns:
    float: Maximum drawdown of given returns array.
    """
    n = returns.size
    if n == 0: return np.nan

    acc_returns = np.empty(n + 1)
    acc_returns[0] = 1.0
    acc_returns[1:] = np.cumprod(1 + returns)

    cur_max = acc_returns[0]
    max_drawdown = 0.0

    for i in range(1, n + 1):
        if acc_returns[i] > cur_max:
            cur_max = acc_returns[i]
        else:
            drawdown = (acc_returns[i] - cur_max) / cur_max
            if drawdown < max_drawdown:
                max_drawdown = drawdown

    return -max_drawdown

@njit
def rolling_max_drawdown(
    returns: np.ndarray,
    window: int = 21,
    min_window: int = 21,
    step: int = 1
) -> np.ndarray:
    """Computes the rolling maximum drawdown over an array of returns.

    ## Parameters:
    returns (numpy.ndarray): 1D array of returns over time.
    window (int): The size of the rolling window.
    min_window (int): The minimum window size to start computing MDD.
    step(int): The step size for the rolling window.

    ## Returns:
    numpy.ndarray: Array of rolling maximum drawdown values.
    """
    n = returns.size
    max_window_i = n-min_window+1
    mdd_results = []

    for i in range(0, max_window_i, step):
        
        if i<(window-min_window):
            i_window = min_window+i
            start_i = 0

        else:
            i_window = window
            start_i = i - (window-min_window)

        end_i = start_i+i_window
        
        if end_i>n: break 
        
        i_array = returns[start_i:end_i]
        mdd = max_drawdown(i_array)
        mdd_results.append(mdd)

    return np.array(mdd_results)

@njit
def CED(
    returns: np.ndarray,
    t: int = 21,
    alpha: float = 0.9
) -> float:
    """Computes the Conditional Expected Drawdown (CED) of an array of returns.""" 
    if returns.size == 0: 
        return np.nan
    r_mdd = rolling_max_drawdown(returns, t)    
    quantile = np.quantile(r_mdd, alpha)
    return np.mean( r_mdd[r_mdd >= quantile])

@njit
def expanding_CED(returns: np.ndarray, t=21, alpha=0.9):
    """Computes the Conditional Expected Drawdown (CED) over an expanding array of returns.""" 
    if returns.size < t:
        return np.full(returns.shape, np.nan)  # Return a NumPy array instead of a scalar

    ced_series = np.full(returns.size, np.nan)  # Initialize with NaNs

    for a in range(t-1, returns.size):  # Ensure at least t observations
        _ret = returns[:a+1]  # Expanding window
        ced_series[a] = CED(_ret, t, alpha)

    return ced_series  # Always return an array

def series_CED(return_series: pd.Series, t=21, alpha=0.9):
    """Computes the Conditional Expected Drawdown (CED) of a Series of returns."""
    _idx = return_series.index
    _arr = return_series.values    
    return pd.Series(expanding_CED(_arr, t, alpha), index=_idx)