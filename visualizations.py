import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import plotly.express as px


def plot_distribution(df: pd.DataFrame, column: str, kind: str = "hist"):
    """Create a distribution plot (histogram or boxplot) for a numeric column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Numeric column to plot.
        kind (str): 'hist' for histogram or 'box' for boxplot.

    Returns:
        plotly.graph_objs._figure.Figure | None
    """
    if df is None or len(df) == 0:
        return None
    if column not in df.columns:
        return None

    series = df[column]
    if not pd.api.types.is_numeric_dtype(series):
        return None

    if kind == "box":
        fig = px.box(df, x=column, title=f"Box Plot of {column}")
    else:
        fig = px.histogram(
            df,
            x=column,
            nbins=30,
            marginal="box",
            title=f"Distribution of {column}",
        )

    return fig

def plot_category_bar(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    agg: str = "sum",
):
    """Create a bar chart showing aggregated values by category.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        category_col (str): Categorical column for the x-axis.
        value_col (str): Numeric column to aggregate on the y-axis.
        agg (str): Aggregation function (e.g., 'sum', 'mean', 'count').

    Returns:
        plotly.graph_objs._figure.Figure or None: Plotly Figure or None if invalid
    """
    if df is None or len(df) == 0:
        return None
    if category_col not in df.columns or value_col not in df.columns:
        return None

    grouped = df.groupby(category_col)[value_col].agg(agg).reset_index()
    fig = px.bar(grouped, x=category_col, y=value_col, title=f"{agg} of {value_col} by {category_col}")
    return fig

def plot_correlation_heatmap(df: pd.DataFrame):
    """
    Create a correlation heatmap for numeric columns using Plotly.
    
    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        plotly.graph_objs._figure.Figure | None: Plotly heatmap, or None if fewer than two numeric columns are available.
    """
    if df is None or len(df) == 0:
        return None

    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        origin="lower",
        title="Correlation Heatmap (numeric features)",
    )
    return fig

def plot_time_series(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    agg: str = "sum",
):
    """Create a time series plot for an aggregated numeric metric over time.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        date_col (str): Column containing date or datetime information.
        value_col (str): Numeric column to aggregate.
        agg (str): Aggregation function (e.g., 'sum', 'mean', 'count').

    Returns:
        plotly.graph_objs._figure.Figure | None: Plotly line chart, or None if the date column cannot be parsed or no data remains.
    """
    if df is None or len(df) == 0:
        return None
    if date_col not in df.columns or value_col not in df.columns:
        return None

    ts_df = df.copy()
    ts_df[date_col] = pd.to_datetime(ts_df[date_col], errors="coerce")
    ts_df = ts_df.dropna(subset=[date_col])

    grouped = (
        ts_df
        .groupby(ts_df[date_col].dt.date)[value_col]
        .agg(agg)
        .reset_index()
        .rename(columns={date_col: "date"})
    )

    if grouped.empty:
        return None

    fig = px.line(grouped, x="date", y=value_col,
                  title=f"{agg} of {value_col} over time")
    return fig