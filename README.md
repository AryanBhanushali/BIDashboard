#  Interactive BI Dashboard (Python + Gradio)

##  Overview

This project is an **interactive Business Intelligence (BI) dashboard** built with **Python** and **Gradio**. It enables users to upload tabular data (CSV or Excel), explore it through summary statistics and interactive filters, generate multiple visualizations, export filtered subsets, and view automated insights such as top-performing groups and potential outliers.

The dashboard is designed for **non-technical business users** and **data analysts** who want to quickly understand their data and answer key business questions without writing code.

---

##  Features

###  Data Upload

* Upload CSV or Excel files
* View dataset info (rows, columns, data types)
* Preview uploaded data
* Clear error handling for invalid or empty files

###  Data Exploration

* Summary statistics for numeric columns
* Missing values report by column
* Correlation matrix for numeric features

###  Interactive Filtering

* Numeric range filters (min/max)
* Categorical filters
* View filtered subset with row counts

###  Visualizations

* Distribution plots (histogram, boxplot)
* Category bar charts with aggregation (sum, mean, count, etc.)
* Correlation heatmap
* Time series plots (aggregated metrics over time)

###  Export

* Download filtered datasets as CSV files

###  Automated Insights

* Top **N** groups by selected numeric metric
* Simple outlier detection (high/low values vs. average)

---

##  Tech Stack

* **Python**
* **pandas**
* **numpy**
* **Plotly**
* **Gradio**

---

##  Project Structure

```text
.
├── app.py               # Main Gradio app (UI, tabs, event wiring)
├── data_processor.py    # Data loading, cleaning, stats, filtering, export
├── visualizations.py    # Plot generation functions
├── insights.py          # Automated insight logic (top N, outliers)
├── utils.py             # Shared helper utilities (currently minimal)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── data/                # Sample datasets
```

---

##  Setup (Local Run)

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. *(Recommended)* Create and activate a virtual environment

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

##  How to Run the Dashboard

### Option 1 – Hosted (Recommended)

Open the deployed Gradio app directly in your browser:
 [https://huggingface.co/spaces/aryanb2305/BI_Dashboard](https://huggingface.co/spaces/aryanb2305/BI_Dashboard)

### Option 2 – Run Locally

```bash
python app.py
```

Open the URL shown in the terminal.

---

##  How to Use the Dashboard

###  Upload Data

* Navigate to the **Upload Data** tab
* Upload a CSV or Excel file
* Verify dataset info and preview

###  Explore Statistics

* Open the **Statistics** tab
* Review summary statistics, missing values, and correlations

###  Filter & Explore

* Use the **Filter & Explore** tab to:

  * Load available columns
  * Apply numeric and categorical filters
  * Inspect filtered results
  * Download filtered data as CSV

###  Visualizations

* Go to the **Visualizations** tab
* Select a visualization type
* Choose relevant columns
* Generate and interpret plots

###  Insights

* Open the **Insights** tab
* Refresh available columns
* Select grouping and numeric metrics
* Choose **Top N**
* Generate insights and outlier summaries

---

##  Example Business Questions

This dashboard can help answer:

* Which products, categories, or regions generate the highest revenue?
* How are key metrics distributed (prices, ratings, order values)?
* Are there strong correlations between numeric variables?
* How do metrics evolve over time?
* Are there unusually high or low values indicating anomalies?

---

##  Limitations

* Data types rely on basic pandas inference
* Time series assumes a parseable date column
* Outlier detection uses a simple z-score approach

---

##  Future Improvements

* Advanced statistical tests and segmentation
* Additional visualizations (scatter plots, maps)
* User-defined insight rules or thresholds
* Authentication and saved dashboards per user

---

##  Acknowledgements

If you find this project useful, feel free to  the repository and share feedback!

---

Happy exploring your data!
