# Interactive BI Dashboard (Python + Gradio)

# 

# Overview
This project is an interactive Business Intelligence (BI) dashboard built with Python and Gradio. It allows users to upload tabular data (CSV/Excel), explore it through summary statistics and filters, generate multiple visualizations, export filtered subsets, and view automated insights such as top-performing groups and potential outliers. The dashboard is designed for non-technical business users and data analysts who want to quickly understand their data and answer key business questions.

# 

# Features

## \*   Data upload:

# &nbsp;   
\*   Upload CSV or Excel files.     
\*   View dataset info (rows, columns, data types) and a preview of the data.     
\*   Clear error messages for invalid or empty files.
     

## \*   Data exploration:

# &nbsp;   
\*   Summary statistics for numeric columns.      
\*   Missing values report by column.
\*   Correlation matrix for numeric features.
\*   Interactive filtering:
\*   Filter by numeric ranges (min/max).
\*   Filter by categorical selections.
\*   View the filtered subset in a table with row counts.      

## \*   Visualizations:

# &nbsp;   
\*   Distribution plots (histogram / boxplot) for numeric columns.
\*   Category bar chart with aggregation (sum, mean, count, etc.).
\*   Correlation heatmap of numeric features.
\*   Time series plot (aggregated metric over time).     

## \*   Export:

# &nbsp;   
\*   Download the filtered dataset as a CSV file.
\*   Automated insights:
\*   Top N groups by a selected numeric metric.
\*   Simple outlier detection for numeric columns (high/low values vs. average).      

# 

## Tech Stack
\*   Python   
\*   pandas 
\*   numpy   
\*   Plotly
\*   Gradio

# &nbsp;   

# 

# Project Structure
\*   app.py - Main Gradio app: UI layout, tabs, and event wiring.
\*   data\\\_processor.py - Data loading, cleaning, summary statistics, missing values, correlation matrix, filtering, export helpers, etc.
\*   visualizations.py - Functions to create distribution plots, category bar charts, correlation heatmaps, and time series plots.
\*   insights.py - Automated insight generation (top N groups, outliers).
\*   utils.py - Small shared (unused) helper functions.  
\*   requirements.txt - Python dependencies.
\*   README.md - Project overview and instructions.
\*   data folder - Sample datasets to test.   

# 

# Setup (for local run)

# 1\. Clone this repository and move it into the project folder.

# 2\. (Recommended) Create and activate a virtual environment.

# 3\. Install dependencies using pip install -r requirements.txt in the terminal.

# 

# How to Run the Dashboard

# 

# \#### Option 1 – Hosted (recommended)

# 

# 1\. Simply open the deployed Gradio app in your browser using the link https://huggingface.co/spaces/aryanb2305/BI\_Dashboard.

# 

# \#### Option 2 – Run locally

# 

# 1\. After installing dependencies, run python app.py in the terminal.

# 2\. Open the URL shown in the terminal.

# &nbsp;   

# 

# How to Use the Dashboard

# 

# 1\.  Upload Data

# &nbsp;   

# &nbsp;   \*   Go to the “Upload Data” tab.

# &nbsp;       

# &nbsp;   \*   Upload a CSV or Excel file.

# &nbsp;       

# &nbsp;   \*   Check dataset info and the preview to confirm the data loaded correctly.

# &nbsp;       

# 2\.  Explore Statistics

# &nbsp;   

# &nbsp;   \*   Open the “Statistics” tab.

# &nbsp;       

# &nbsp;   \*   View summary statistics, missing values, and the correlation matrix to understand data quality and relationships.

# &nbsp;       

# 3\.  Filter \& Explore

# &nbsp;   

# &nbsp;   \*   Use the “Filter \& Explore” tab to:

# &nbsp;       

# &nbsp;       \*   Load available columns.

# &nbsp;           

# &nbsp;       \*   Apply numeric and categorical filters.

# &nbsp;           

# &nbsp;       \*   Inspect the filtered subset and row count.

# &nbsp;           

# &nbsp;       \*   Download the filtered subset as a CSV file.

# &nbsp;           

# 4\.  Visualizations

# &nbsp;   

# &nbsp;   \*   In the “Visualizations” tab:

# &nbsp;       

# &nbsp;       \*   Choose a visualization type (Distribution, Category Bar, Correlation Heatmap, Time Series).

# &nbsp;           

# &nbsp;       \*   Select appropriate columns (numeric/date/category).

# &nbsp;           

# &nbsp;       \*   Generate the plot and interpret the results.

# &nbsp;           

# 5\.  Insights

# &nbsp;   

# &nbsp;   \*   In the “Insights” tab:

# &nbsp;       

# &nbsp;       \*   Refresh columns.

# &nbsp;           

# &nbsp;       \*   Select a grouping column (category) and a numeric value column.

# &nbsp;           

# &nbsp;       \*   Choose Top N.

# &nbsp;           

# &nbsp;       \*   Generate insights to see top groups and potential outliers.

# &nbsp;           

# 

# Business Questions (Examples)

# 

# This dashboard can help answer questions such as:

# 

# \*   Which categories, products, or regions generate the highest sales or revenue?

# &nbsp;   

# \*   How are key metrics distributed (e.g., order values, prices, ratings)?

# &nbsp;   

# \*   Are there strong correlations between numeric variables?

# &nbsp;   

# \*   How do key metrics change over time?

# &nbsp;   

# \*   Are there any unusually high or low values that may indicate anomalies?

# &nbsp;   

# 

# Limitations and Future Improvements

# 

# \*   Data types rely on basic pandas inference; further cleaning may be needed for very messy datasets.

# &nbsp;   

# \*   Time series assumes a parseable date column.

# &nbsp;   

# \*   Outlier detection uses a simple z-score approach and may need adjustment for heavily skewed data.

# &nbsp;   

# 

# Possible future enhancements:

# 

# \*   More advanced statistical tests or segmentation.

# &nbsp;   

# \*   Additional visualization types (e.g., scatter plots, maps).

# &nbsp;   

# \*   User-defined insight rules or thresholds.

# &nbsp;   

# \*   Authentication / saving dashboards per user.




