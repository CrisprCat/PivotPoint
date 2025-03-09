import streamlit as st

# Define mde functions
from scipy.stats import norm
import numpy as np
def mde_cr(sample_size, baseline, alpha = 0.05, power = 0.8, test_type = 'Two-sided'):
    """
    Calculate the Minimum Detectable Effect (MDE) for a two-sample z-test.
    
    Parameters:
    sample_size (int): Sample size per group
    baseline (float): Conversion rate
    alpha (float): Significance level (default: 0.05)
    power (float): Statistical power (default: 0.8)
    test_type (str): 'Two-sided' or 'One-sided' (default: 'Two-sided')
    
    Returns:
    float: Minimum Detectable Effect (MDE)
    """
    z_beta = norm.ppf(power)
    if test_type == 'Two-sided':
        z_alpha = norm.ppf(1 - alpha / 2)
    elif test_type == 'One-sided':
        z_alpha = norm.ppf(1 - alpha)
    else:
        raise ValueError("test_type must be 'Two-sided' or 'One-sided'.")

    se_baseline = np.sqrt(2 * baseline * (1 - baseline) / sample_size)

    mde = (z_alpha + z_beta) * se_baseline

    return mde

def mde_cont(sample_size, std_dev, alpha=0.05, power=0.8, test_type='Two-sided'):
    """
    Calculate the Minimum Detectable Effect (MDE) for a two-sample t-test with a continuous metric.
    
    Parameters:
    sample_size (int): Sample size per group
    std_dev (float): Standard deviation of the metric
    alpha (float): Significance level (default: 0.05)
    power (float): Statistical power (default: 0.8)
    test_type (str): 'Two-sided' or 'One-sided' (default: 'Two-sided')
    
    Returns:
    float: Minimum Detectable Effect (MDE)
    """
    z_beta = norm.ppf(power)
    if test_type == 'Two-sided':
        z_alpha = norm.ppf(1 - alpha / 2)
    elif test_type == 'One-sided':
        z_alpha = norm.ppf(1 - alpha)
    else:
        raise ValueError("test_type must be 'Two-sided' or 'One-sided'.")
    
    se = std_dev / np.sqrt(sample_size)
    
    mde = (z_alpha + z_beta) * se
    
    return mde


## Sanity checks for csv file uploads
### check if revenue file data only contains numeric values
import pandas as pd
def check_numeric_columns (df, col_indices):
    is_numeric = []
    for col_idx in col_indices:
        col = df.iloc[:, col_idx]
        is_numeric.append(pd.to_numeric(col, errors = 'coerce').notnull().all())

    return all(is_numeric)

### check if revenue file contains orders with revenue <=0
def check_value_size(df, col_indices):
    is_greater_zero = df.iloc[:, col_indices].gt(0).all().all()

    return is_greater_zero


