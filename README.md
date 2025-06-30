Stacked Bar Chart Dashboard
This is a Python-based interactive dashboard built with Streamlit for visualizing data as stacked bar charts (count or proportion) or scatter plots. The application allows users to upload CSV or Excel files, customize plot aesthetics (e.g., colors, text sizes, transparency), apply faceting (facet_grid or facet_wrap), and filter data by date ranges or legend categories. It replicates the functionality of an R Shiny dashboard, using Plotly for interactive plotting and Pandas for data manipulation.
Features

File Upload: Supports CSV (.csv) and Excel (.xlsx, .xls) files.
Chart Types:
Count: Stacked bar chart showing counts by category over time.
Proportion: Stacked bar chart showing proportions (percentages) by category over time.
Scatter: Scatter plot with customizable point size and shape.


Faceting: Apply facet_grid (rows) or facet_wrap (columns) to all chart types for multi-panel visualizations.
Text Size Customization: Adjust sizes for data labels, x-axis labels, and y-axis labels.
Date Filtering: Filter data by year or month for date-based x-axis variables.
Legend Customization: Show/hide legend and adjust its position (top, bottom, left, right).
Color Picker: Customize colors for each legend category.
Scatter Plot Options: Adjust point size, shape, and y-axis numeric range (for numeric y-axis).
Plot Download: Save plots as JPEG images.
Transparency: Adjust plot opacity (alpha).

Prerequisites

Python 3.8 or higher
pip for installing dependencies
A web browser for viewing the Streamlit app

Installation

Clone the Repository:
git clone https://github.com/your-username/stacked-bar-chart-dashboard.git
cd stacked-bar-chart-dashboard


Create a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:The required packages are listed in requirements.txt. Install them using:
pip install -r requirements.txt

The requirements.txt includes:
streamlit>=1.38.0
pandas>=2.2.2
plotly>=5.24.1
openpyxl>=3.1.5
xl


