import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Stacked Bar Chart Dashboard", layout="wide")

st.title("📊 Stacked Bar Chart Dashboard")

# --- Upload Section ---
st.sidebar.header("📁 Upload File")
file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx", "xls"])

# Initialize placeholders
df = None

if file:
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("✅ File uploaded successfully!")
        st.write("### Preview of Data")
        st.dataframe(df.head())

        # --- UI Inputs ---
        st.sidebar.header("🛠️ Plot Options")
        title = st.sidebar.text_input("Plot Title", "Stacked Bar Chart")
        subtitle = st.sidebar.text_input("Plot Subtitle", "")
        x_var = st.sidebar.selectbox("X-Axis Variable", df.columns)
        y_var = st.sidebar.selectbox("Y-Axis Variable", df.columns)
        legend_var = st.sidebar.selectbox("Legend Variable", df.columns)
        chart_type = st.sidebar.radio("Chart Type", ["Count", "Proportion", "Scatter"])
        show_legend = st.sidebar.checkbox("Show Legend", True)

        st.sidebar.markdown("### Customize Appearance")
        alpha = st.sidebar.slider("Transparency", 0.0, 1.0, 0.8, step=0.1)
        font_size = st.sidebar.slider("Font Size", 5, 20, 10)

        # --- Plot Section ---
        st.subheader(f"{title}")
        if subtitle:
            st.caption(subtitle)

        # Count / Proportion chart
        if chart_type in ["Count", "Proportion"]:
            df_grouped = df.groupby([x_var, legend_var]).size().reset_index(name='Count')

            if chart_type == "Proportion":
                df_grouped['Proportion'] = df_grouped.groupby(x_var)['Count'].transform(lambda x: x / x.sum())

            fig = px.bar(
                df_grouped,
                x=x_var,
                y='Count' if chart_type == "Count" else 'Proportion',
                color=legend_var,
                barmode='stack',
                opacity=alpha,
                text_auto=True
            )
            fig.update_layout(font=dict(size=font_size))
            if not show_legend:
                fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Scatter Plot
        elif chart_type == "Scatter":
            fig = px.scatter(
                df,
                x=x_var,
                y=y_var,
                color=legend_var,
                opacity=alpha
            )
            fig.update_layout(font=dict(size=font_size))
            if not show_legend:
                fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # --- Download Plot ---
        st.sidebar.markdown("### 📥 Download")
        buf = BytesIO()
        fig.write_image(buf, format="png")
        st.download_button("Download Plot", data=buf.getvalue(), file_name="plot.png", mime="image/png")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("👈 Upload a file to get started.")
