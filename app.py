import gradio as gr
import pandas as pd

from data_processor import (
    load_data,
    get_basic_info,
    get_preview,
    get_summary_statistics,
    get_missing_report,
    get_correlation_matrix,
    filter_dataframe,
    save_dataframe_to_temp_csv,
)
from visualizations import (
    plot_distribution,
    plot_category_bar,
    plot_correlation_heatmap,
    plot_time_series,
)
from insights import (
    get_top_n,
    get_simple_outliers,
)

def create_dashboard():
    """Create and configure the BI dashboard Gradio app.

    Sets up all tabs (Upload Data, Statistics, Filter & Explore, Visualizations,
    Insights), wires UI components to backend functions, and returns the Blocks
    object that can be launched.
    """
    with gr.Blocks() as demo:
        gr.Markdown("# Business Intelligence Dashboard")
        gr.Markdown("Upload a dataset to begin exploring.")

        df_state = gr.State(value=None)

        # -------- Data Upload Tab --------
        with gr.Tab("Data Upload"):
            file_input = gr.File(label="Upload CSV or Excel file")
            upload_button = gr.Button("Load Data")

            info_box = gr.JSON(label="Dataset Info")
            preview_rows = gr.Slider(
                minimum=1, maximum=20, value=5, step=1, label="Preview rows"
            )
            preview_table = gr.Dataframe(
                label="Data Preview", interactive=False
            )
            error_box = gr.Markdown(label="Messages")

            def handle_upload(file, n_rows):
                """Handle file upload, returning state, dataset info, preview, and a status message.
                
                Args:
                    file: Uploaded file (CSV/Excel) from Gradio.
                    n_rows: Number of rows to show in the preview.

                Returns:
                    Tuple of:
                        - DataFrame or None
                        - dataset info dict
                        - preview DataFrame
                        - status message string
                """
                if file is None:
                    return None, {}, pd.DataFrame(), "Please upload a file first."
                try:
                    df = load_data(file)
                    info = get_basic_info(df)
                    preview = get_preview(df, n_rows)
                    return df, info, preview, "✅ Data loaded successfully."
                except Exception as e:
                    return None, {}, pd.DataFrame(), f"⚠️ {str(e)}"

            upload_button.click(
                fn=handle_upload,
                inputs=[file_input, preview_rows],
                outputs=[df_state, info_box, preview_table, error_box],
            )

        # -------- Statistics Tab --------
        with gr.Tab("Statistics"):
            gr.Markdown("## Dataset Profiling")

            stats_button = gr.Button("Compute Statistics")

            numeric_stats = gr.Dataframe(label="Numeric Columns Summary")
            categorical_stats = gr.Dataframe(label="Categorical Columns Summary")
            missing_report_df = gr.Dataframe(label="Missing Values Report")
            corr_matrix_df = gr.Dataframe(label="Correlation Matrix")
            stats_msg = gr.Markdown()

            def compute_stats(df: pd.DataFrame | None):
                """Compute statistics, missing report, and correlation matrix for the dataset.
                
                Args:
                    df (pd.DataFrame | None): Current dataset from state.

                Returns:
                    Tuple of:
                        - numeric summary DataFrame
                        - categorical summary DataFrame
                        - missing values report DataFrame
                        - correlation matrix DataFrame
                        - status message string
                """
                if df is None or len(df) == 0:
                    return (
                        pd.DataFrame(),
                        pd.DataFrame(),
                        pd.DataFrame(),
                        pd.DataFrame(),
                        "⚠️ Please upload data first in the Data Upload tab.",
                    )
                stats = get_summary_statistics(df)
                missing = get_missing_report(df)
                corr = get_correlation_matrix(df)
                return (
                    stats["numeric"],
                    stats["categorical"],
                    missing,
                    corr,
                    "✅ Statistics computed.",
                )

            stats_button.click(
                fn=compute_stats,
                inputs=[df_state],
                outputs=[
                    numeric_stats,
                    categorical_stats,
                    missing_report_df,
                    corr_matrix_df,
                    stats_msg,
                ],
            )

        # -------- Filter & Explore Tab --------
        with gr.Tab("Filter & Explore"):
            gr.Markdown("## Interactive Filtering")

            with gr.Row():
                column_dropdown = gr.Dropdown(
                    choices=[],
                    label="Column to filter",
                    interactive=True,
                )
                refresh_cols_btn = gr.Button("Load Columns")

            with gr.Row():
                min_input = gr.Number(label="Min (numeric columns)")
                max_input = gr.Number(label="Max (numeric columns)")

            category_multiselect = gr.Dropdown(
                choices=[],
                multiselect=True,
                label="Categories (for text columns)",
            )

            filter_button = gr.Button("Apply Filter")

            filtered_info = gr.Markdown(label="Filter Info")
            filtered_table = gr.Dataframe(label="Filtered Data", interactive=False)

            download_btn = gr.Button("Download filtered data (CSV)")
            download_file = gr.File(label="Download file", interactive=False)

            def handle_download(df):
                """Prepare the currently displayed DataFrame for CSV download.
                
                Args:
                    df (pd.DataFrame | None): Filtered DataFrame from the UI.

                Returns:
                    str | None: Path to a temporary CSV file, or None if no data.
                """
                if df is None or len(df) == 0:
                    return None
                filepath = save_dataframe_to_temp_csv(df)
                return filepath
            
            download_btn.click(
                fn=handle_download,
                inputs=[filtered_table],
                outputs=[download_file],
            )

            def load_columns(df: pd.DataFrame | None):
                """Load column names into the filter column dropdown.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.

                Returns:
                    gr.update: Updated choices for the column dropdown.
                """
                if df is None or len(df) == 0:
                    return gr.update(choices=[])
                cols = list(df.columns.astype(str))
                return gr.update(choices=cols)

            refresh_cols_btn.click(
                fn=load_columns,
                inputs=[df_state],
                outputs=[column_dropdown],
            )

            def update_categories(df: pd.DataFrame | None, col: str):
                """Update category choices based on the selected column.
                For non-numeric columns, returns up to 100 unique values.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.
                    col (str): Selected column name.

                Returns:
                    gr.update: Updated choices for the category multiselect.
                """
                if df is None or len(df) == 0 or col is None or col == "":
                    return gr.update(choices=[])
                if col not in df.columns:
                    return gr.update(choices=[])
                series = df[col]
                if not pd.api.types.is_numeric_dtype(series):
                    # for non-numeric columns, list unique values
                    uniques = sorted(series.dropna().astype(str).unique().tolist())
                    # cap length to avoid massive dropdowns
                    uniques = uniques[:100]
                    return gr.update(choices=uniques)
                else:
                    return gr.update(choices=[])

            column_dropdown.change(
                fn=update_categories,
                inputs=[df_state, column_dropdown],
                outputs=[category_multiselect],
            )

            def apply_filter(
                df: pd.DataFrame | None,
                col: str,
                min_val,
                max_val,
                cats,
            ):
                """Apply the current filter settings to the DataFrame and return the filtered data and message.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.
                    col (str): Column to filter on.
                    min_val: Minimum value for numeric filter.
                    max_val: Maximum value for numeric filter.
                    cats: Selected categories for categorical filter.
                
                Returns:
                    Tuple[pd.DataFrame, str]: Filtered DataFrame and status message.
                """
                if df is None or len(df) == 0:
                    return pd.DataFrame(), "⚠️ Please upload data first."
                if not col:
                    return pd.DataFrame(), "⚠️ Please select a column."

                filtered = filter_dataframe(df, col, min_val, max_val, cats)
                msg = f"Filtered rows: {len(filtered)} (out of {len(df)})"
                return filtered, msg

            filter_button.click(
                fn=apply_filter,
                inputs=[df_state, column_dropdown, min_input, max_input, category_multiselect],
                outputs=[filtered_table, filtered_info],
            )

        # -------- Visualizations Tab --------
        with gr.Tab("Visualizations"):
            gr.Markdown("## Visualizations")

            # Distribution Controls
            with gr.Row():
                vis_type = gr.Radio(
                    choices=["Distribution", "Category Bar", "Correlation Heatmap", "Time Series"],
                    value="Distribution",
                    label="Visualization Type",
            )
                vis_column = gr.Dropdown(
                    choices=[],
                    label="Numeric Column (for Distribution)",
                    interactive=True,
                )
                vis_kind = gr.Radio(
                    choices=["hist", "box"],
                    value="hist",
                    label="Distribution Type",
                )

            # Category Bar Controls
            with gr.Row():
                cat_x = gr.Dropdown(choices=[], label="Category Column", interactive=True)
                cat_y = gr.Dropdown(choices=[], label="Value Column (numeric)", interactive=True)
                cat_agg = gr.Radio(
                    choices=["sum", "mean", "count", "median"],
                    value="sum",
                    label="Aggregation",
                )

            # Time Series Controls
            with gr.Row():
                ts_date = gr.Dropdown(choices=[], label="Date Column", interactive=True)
                ts_value = gr.Dropdown(choices=[], label="Value Column (numeric)", interactive=True)
                ts_agg = gr.Radio(
                    choices=["sum", "mean", "count", "median"],
                    value="sum",
                    label="Time Series Aggregation",
                )

            vis_output = gr.Plot(label="Plot")
            vis_msg = gr.Markdown()
            vis_refresh = gr.Button("Refresh Columns")

            def load_vis_columns(df: pd.DataFrame | None):
                """Load column names into the visualization dropdowns based on data types.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.

                Returns:
                    Tuple of gr.update objects for each visualization-related dropdown.
                """
                if df is None or len(df) == 0:
                    empty = gr.update(choices=[])
                    return empty, empty, empty, empty, empty
                cols = df.columns.astype(str).tolist()
                num_cols = df.select_dtypes(include="number").columns.astype(str).tolist()
                # crude date detection: columns containing 'date' or already datetime
                date_like = [
                    c for c in cols
                    if "date" in c.lower() or pd.api.types.is_datetime64_any_dtype(df[c])
                ]
                return (
                    gr.update(choices=num_cols),  # vis_column
                    gr.update(choices=cols),      # cat_x
                    gr.update(choices=num_cols),  # cat_y
                    gr.update(choices=date_like or cols),  # ts_date
                    gr.update(choices=num_cols),  # ts_value
                )

            vis_refresh.click(
                fn=load_vis_columns,
                inputs=[df_state],
                outputs=[vis_column, cat_x, cat_y, ts_date, ts_value],
            )

            def make_plot(df, vtype, col, kind, x_cat, y_val, agg, date_col, ts_val, ts_agg_sel):
                """Dispatch to the appropriate visualization strategy based on the selected type.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.
                    vtype (str): Visualization type selected by the user.
                    col (str): Column for distribution plot.
                    kind (str): Distribution kind ('hist' or 'box').
                    x_cat (str): Category column for bar chart.
                    y_val (str): Value column for bar chart and time series.
                    agg (str): Aggregation for category bar.
                    date_col (str): Date column for time series.
                    ts_val (str): Value column for time series.
                    ts_agg_sel (str): Aggregation function for time series.

                Returns:
                    Tuple[plot, str]: Plot object (image or figure) and status message.
                """
                if df is None or len(df) == 0:
                    return None, "⚠️ Please upload data first."

                if vtype == "Distribution":
                    if not col:
                        return None, "⚠️ Select a numeric column."
                    img = plot_distribution(df, col, kind=kind)
                    if img is None:
                        return None, "⚠️ Could not create plot."
                    return img, f"✅ {vtype} plot created for '{col}'."

                if vtype == "Category Bar":
                    if not x_cat or not y_val:
                        return None, "⚠️ Select category and value columns."
                    fig = plot_category_bar(df, x_cat, y_val, agg=agg)
                    if fig is None:
                        return None, "⚠️ Could not create bar plot."
                    return fig, f"✅ Bar chart created: {agg} of {y_val} by {x_cat}."

                if vtype == "Correlation Heatmap":
                    fig = plot_correlation_heatmap(df)
                    if fig is None:
                        return None, "⚠️ Need at least 2 numeric columns for a heatmap."
                    return fig, "✅ Correlation heatmap created."

                if vtype == "Time Series":
                    if not date_col or not ts_val:
                        return None, "⚠️ Select date and value columns."
                    fig = plot_time_series(df, date_col, ts_val, agg=ts_agg_sel)
                    if fig is None:
                        return None, "⚠️ Could not create time series plot. Check date column."
                    return fig, f"✅ Time series of {ts_agg_sel} {ts_val} over time."

                return None, "⚠️ Unsupported visualization type."

            plot_button = gr.Button("Generate Plot")
            plot_button.click(
                fn=make_plot,
                inputs=[df_state, vis_type, vis_column, vis_kind,
                    cat_x, cat_y, cat_agg, ts_date, ts_value, ts_agg],
                outputs=[vis_output, vis_msg],
            )


        # -------- Insights Tab --------
        with gr.Tab("Insights"):
            gr.Markdown("Automated insights will appear here.")
            with gr.Row():
                ins_group_col = gr.Dropdown(choices=[], label="Group by (category)", interactive=True)
                ins_value_col = gr.Dropdown(choices=[], label="Value column (numeric)", interactive=True)
                ins_top_n = gr.Slider(3, 20, value=5, step=1, label="Top N")

            top_table = gr.Dataframe(label="Top N Groups", interactive=False)
            outlier_table = gr.Dataframe(label="Potential Outliers", interactive=False)

            ins_msg = gr.Markdown()
            ins_btn = gr.Button("Generate Insights")

            def load_insight_columns(df: pd.DataFrame | None):
                """Generate top-N and outlier insights from the given DataFrame.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.

                Returns:
                    Tuple of gr.update objects for group and value column dropdowns.
                """
                if df is None or len(df) == 0:
                    return gr.update(choices=[]), gr.update(choices=[])
                cols = df.columns.astype(str).tolist()
                num_cols = df.select_dtypes(include="number").columns.astype(str).tolist()
                return gr.update(choices=cols), gr.update(choices=num_cols)
            ins_refresh = gr.Button("Refresh Columns")
            ins_refresh.click(
                fn=load_insight_columns,
                inputs=[df_state],
                outputs=[ins_group_col, ins_value_col],
            )    
            # On app load or data change, you can also reuse df_state to fill these.
            
            def run_insights(df: pd.DataFrame | None, group_col, value_col, n):
                """Generate top-N and outlier insights from the given DataFrame.
                
                Args:
                    df (pd.DataFrame | None): Current dataset.
                    group_col (str): Column to group by for top-N.
                    value_col (str): Numeric column used for aggregation and outliers.
                    n (int): Number of top groups to return.

                Returns:
                    Tuple[pd.DataFrame, pd.DataFrame, str]:
                        - Top-N groups DataFrame
                        - Outliers DataFrame
                        - Status message
                """
                if df is None or len(df) == 0:
                    return pd.DataFrame(), pd.DataFrame(), "⚠️ Please upload/filter data first."
                top_df = get_top_n(df, group_col, value_col, n=int(n))
                out_df = get_simple_outliers(df, value_col)
                if top_df.empty and out_df.empty:
                    return top_df, out_df, "⚠️ No insights available. Check column choices."
                return top_df, out_df, f"✅ Insights based on '{group_col}' and '{value_col}'."
            ins_btn.click(
                fn=run_insights,
                inputs=[df_state, ins_group_col, ins_value_col, ins_top_n],
                outputs=[top_table, outlier_table, ins_msg],
            )
    return demo


if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(theme=gr.themes.Soft(), share=True)