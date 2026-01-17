import pandas as pd

def get_top_n(df: pd.DataFrame, group_col: str, value_col: str, n: int = 5, agg: str = "sum"):
    """Return the top N groups by an aggregated numeric column.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        group_col (str): Categorical column to group by.
        value_col (str): Numeric column to aggregate.
        n (int): Number of top groups to return.
        agg (str): Aggregation function name (e.g., 'sum', 'mean').

    Returns:
        pd.DataFrame: DataFrame with top N groups and their aggregated values.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    if group_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()
    grouped = df.groupby(group_col)[value_col].agg(agg).reset_index()
    return grouped.sort_values(by=value_col, ascending=False).head(n)

def get_simple_outliers(df: pd.DataFrame, col: str, z_thresh: float = 2.5):
    """Return rows where the specified column has z-score beyond the threshold.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        col (str): Numeric column to analyze.
        z_thresh (float): Z-score threshold for flagging outliers.

    Returns:
        pd.DataFrame: Subset of df containing potential outliers.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    if col not in df.columns:
        return pd.DataFrame()
    s = df[col]
    if not pd.api.types.is_numeric_dtype(s):
        return pd.DataFrame()
    z = (s - s.mean()) / s.std(ddof=0)
    return df[(z > z_thresh) | (z < -z_thresh)]