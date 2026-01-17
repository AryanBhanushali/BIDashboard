import pandas as pd
from typing import Tuple, Dict, Any
import tempfile
import os


def load_data(file) -> pd.DataFrame:
    """
    Load a CSV or Excel file from a Gradio UploadedFile into a DataFrame.
    Args:
        file: Gradio UploadedFile object uploaded by the user.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        ValueError: If no file is provided, format is unsupported, or loading fails.
    """
    if file is None:
        raise ValueError("No file uploaded.")

    try:
        name = file.name
        if name.endswith(".csv"):
            df = pd.read_csv(file.name)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file.name)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")
        return df
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")


def get_basic_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Return basic dataset information: shape, columns, dtypes.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        Dict[str, Any]: Basic information about the DataFrame.
    """
    info = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns.astype(str)),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
    return info


def get_preview(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Return first n rows as a preview.
    """
    return df.head(n)


def get_summary_statistics(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Return summary stats for numeric and categorical columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        n (int): Number of rows to return.

    Returns:
        Dict[str, pd.DataFrame]: Summary statistics for numeric and categorical columns.
    """
    numeric_desc = df.select_dtypes(include="number").describe().T
    categorical_desc = df.select_dtypes(exclude="number").describe().T
    return {
        "numeric": numeric_desc,
        "categorical": categorical_desc,
    }


def get_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return missing values per column.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with missing value counts and percentages.
    """
    missing = df.isna().sum()
    percent = (missing / len(df)) * 100
    report = pd.DataFrame(
        {
            "missing_count": missing,
            "missing_percent": percent.round(2),
        }
    )
    return report


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return correlation matrix for numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] == 0:
        return pd.DataFrame()
    return numeric_df.corr()

def filter_dataframe(
    df: pd.DataFrame,
    column: str,
    min_val: float | int | None = None,
    max_val: float | int | None = None,
    categories: list[str] | None = None,
):
    """
    Filter a DataFrame by a single column using numeric or categorical criteria.
    If the column is numeric, apply optional min/max filters.
    If the column is non-numeric, filter by a list of categories.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to filter on.
        min_val (float | int | None): Minimum value for numeric columns.
        max_val (float | int | None): Maximum value for numeric columns.
        categories (list[str] | None): Allowed values for non-numeric columns.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if df is None or len(df) == 0:
        return df

    if column not in df.columns:
        return df

    series = df[column]

    if pd.api.types.is_numeric_dtype(series):
        if min_val is not None:
            df = df[series >= min_val]
        if max_val is not None:
            df = df[series <= max_val]
    else:
        if categories:
            df = df[series.isin(categories)]

    return df

def save_dataframe_to_temp_csv(df: pd.DataFrame) -> str | None:
    """Save df to a temp CSV file and return its filepath.
    
    Args:
        df (pd.DataFrame): DataFrame to save.

    Returns:
        str | None: Filepath of the saved CSV, or None if df is empty.
    """
    if df is None or df.empty:
        return None
    fd, path = tempfile.mkstemp(suffix=".csv", prefix="filtered_")
    os.close(fd)
    df.to_csv(path, index=False)
    return path