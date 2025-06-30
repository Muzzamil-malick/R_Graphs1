import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
from PIL import Image

# Streamlit page configuration
st.set_page_config(page_title="Stacked Bar Chart Dashboard", layout="wide")

# Title
st.title("Stacked Bar Chart Dashboard")

# Sidebar
with st.sidebar:
    st.header("Data Upload")
    uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx", "xls"])

    if uploaded_file:
        # Read file based on extension
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Date parsing
            date_cols = ["date", "onsetdate", "specdate", "DateEnter", "Year"]
            for col in date_cols:
                if col in df.columns:
                    if df[col].dtype in ["object", "string"]:
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                    elif df[col].dtype in ["int64", "float64"] and col == "Year":
                        df[col] = pd.to_datetime(df[col].astype(str) + "-01-01", format="%Y-%m-%d")

            # Store data in session state
            st.session_state["df"] = df

            # Column selection
            all_cols = df.columns.tolist()
            st.header("Graph Options")
            title = st.text_input("Plot Title", value="Stacked Bar Chart")
            subtitle = st.text_input("Plot Subtitle", value="")
            x_var = st.selectbox("X-Axis Variable", all_cols, index=0)
            y_var = st.selectbox("Y-Axis Variable", all_cols, index=1 if len(all_cols) > 1 else 0)
            legend_var = st.selectbox("Legend Color Variable", all_cols, index=2 if len(all_cols) > 2 else 0)
            time_filter = st.selectbox("Time Filter Granularity", ["Year", "Month"], index=0)
            chart_type = st.selectbox("Chart Type", ["Count", "Proportion", "Scatter"], index=0)
            
            # Date range filter for date x-axis
            if pd.api.types.is_datetime64_any_dtype(df[x_var]):
                date_range = st.date_input("Select Date Range", 
                                          [df[x_var].min(), df[x_var].max()],
                                          min_value=df[x_var].min(),
                                          max_value=df[x_var].max())
            else:
                date_range = None

            # Legend filter
            legend_choices = df[legend_var].unique().tolist()
            legend_filter = st.multiselect("Filter Legend Categories", legend_choices, default=legend_choices)

            # Transparency
            alpha = st.slider("Transparency", min_value=0.0, max_value=1.0, value=0.8, step=0.1)

            # Text size options
            st.header("Text Size Options")
            data_label_size = st.slider("Data Label Text Size", min_value=1, max_value=10, value=3, step=0.5)
            x_label_size = st.slider("X-Axis Label Text Size", min_value=5, max_value=20, value=10, step=1)
            y_label_size = st.slider("Y-Axis Label Text Size", min_value=5, max_value=20, value=10, step=1)

            # Facet options
            st.header("Facet Options")
            facet_var = st.selectbox("Facet Variable", ["None"] + all_cols, index=0)
            facet_type = st.radio("Facet Type", ["Grid", "Wrap"], index=1, horizontal=True)

            # Legend options
            st.header("Legend Options")
            show_legend = st.checkbox("Show Legend", value=True)
            if show_legend:
                legend_position = st.selectbox("Legend Position", ["top", "bottom", "left", "right"], index=0)
            else:
                legend_position = None

            # Scatter plot options
            if chart_type == "Scatter":
                st.header("Scatter Plot Options")
                point_size = st.slider("Point Size", min_value=1, max_value=10, value=3, step=0.5)
                point_shape = st.selectbox("Point Shape", ["circle", "triangle-up", "square", "diamond"], index=0)
                if pd.api.types.is_numeric_dtype(df[y_var]):
                    y_range = st.slider("Y-Axis Numeric Range", 
                                        min_value=float(df[y_var].min()), 
                                        max_value=float(df[y_var].max()), 
                                        value=(float(df[y_var].min()), float(df[y_var].max())))
                else:
                    y_range = None
            else:
                point_size = None
                point_shape = None
                y_range = None

            # Color picker
            st.header("Color Picker")
            if legend_filter:
                colors = {cat: st.color_picker(f"Color for {cat}", value="#FF0000") for cat in legend_filter}
            else:
                colors = {}

            # Store inputs in session state
            st.session_state["title"] = title
            st.session_state["subtitle"] = subtitle
            st.session_state["x_var"] = x_var
            st.session_state["y_var"] = y_var
            st.session_state["legend_var"] = legend_var
            st.session_state["time_filter"] = time_filter
            st.session_state["chart_type"] = chart_type
            st.session_state["date_range"] = date_range
            st.session_state["legend_filter"] = legend_filter
            st.session_state["alpha"] = alpha
            st.session_state["data_label_size"] = data_label_size
            st.session_state["x_label_size"] = x_label_size
            st.session_state["y_label_size"] = y_label_size
            st.session_state["facet_var"] = facet_var
            st.session_state["facet_type"] = facet_type
            st.session_state["show_legend"] = show_legend
            st.session_state["legend_position"] = legend_position
            st.session_state["colors"] = colors
            st.session_state["point_size"] = point_size
            st.session_state["point_shape"] = point_shape
            st.session_state["y_range"] = y_range

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Main panel
required_keys = ["df", "x_var", "y_var", "legend_var", "time_filter", "chart_type", 
                 "legend_filter", "alpha", "data_label_size", "x_label_size", 
                 "y_label_size", "facet_var", "facet_type", "show_legend", "colors"]
if all(key in st.session_state for key in required_keys):
    df = st.session_state["df"]
    x_var = st.session_state["x_var"]
    y_var = st.session_state["y_var"]
    legend_var = st.session_state["legend_var"]
    time_filter = st.session_state["time_filter"]
    chart_type = st.session_state["chart_type"]
    date_range = st.session_state["date_range"]
    legend_filter = st.session_state["legend_filter"]
    alpha = st.session_state["alpha"]
    data_label_size = st.session_state["data_label_size"]
    x_label_size = st.session_state["x_label_size"]
    y_label_size = st.session_state["y_label_size"]
    facet_var = st.session_state["facet_var"]
    facet_type = st.session_state["facet_type"]
    show_legend = st.session_state["show_legend"]
    legend_position = st.session_state["legend_position"]
    colors = st.session_state["colors"]
    point_size = st.session_state.get("point_size")
    point_shape = st.session_state.get("point_shape")
    y_range = st.session_state.get("y_range")

    # Data processing
    plot_df = df.copy()
    
    # Apply date range filter
    if pd.api.types.is_datetime64_any_dtype(plot_df[x_var]) and date_range:
        if time_filter == "Year":
            plot_df["Year"] = plot_df[x_var].dt.year
            plot_df = plot_df[(plot_df["Year"] >= date_range[0].year) & (plot_df["Year"] <= date_range[1].year)]
        else:
            plot_df["Month"] = plot_df[x_var].dt.strftime("%Y-%m")
            plot_df = plot_df[(plot_df[x_var] >= pd.to_datetime(date_range[0])) & 
                              (plot_df[x_var] <= pd.to_datetime(date_range[1]))]

    # Apply legend filter
    if legend_filter:
        plot_df = plot_df[plot_df[legend_var].isin(legend_filter)]

    # Apply y-axis filter for scatter
    if chart_type == "Scatter" and pd.api.types.is_numeric_dtype(plot_df[y_var]) and y_range:
        plot_df = plot_df[(plot_df[y_var] >= y_range[0]) & (plot_df[y_var] <= y_range[1])]

    # Prepare data for count/proportion
    if chart_type in ["Count", "Proportion"]:
        if time_filter == "Year":
            plot_df["TimeUnit"] = plot_df[x_var].dt.year
        else:
            plot_df["TimeUnit"] = plot_df[x_var].dt.strftime("%Y-%m")

        if chart_type == "Count":
            plot_df = plot_df.groupby(["TimeUnit", legend_var]).size().reset_index(name="Count")
        else:
            plot_df = plot_df.groupby(["TimeUnit", legend_var]).size().reset_index(name="Count")
            plot_df["Proportion"] = plot_df.groupby("TimeUnit")["Count"].transform(lambda x: x / x.sum())

    # Plotting
    if len(plot_df) == 0:
        st.warning("No data available for the selected filters.")
    else:
        # Define color map
        color_map = {cat: colors.get(cat, "#FF0000") for cat in legend_filter}

        # Create plot
        if chart_type == "Count":
            fig = px.bar(
                plot_df, x="TimeUnit", y="Count", color=legend_var,
                barmode="stack", opacity=alpha,
                title=st.session_state["title"],
                labels={"TimeUnit": "Year" if time_filter == "Year" else "Month-Year", "Count": "Count"}
            )
            # Add data labels
            for cat in legend_filter:
                cat_df = plot_df[plot_df[legend_var] == cat]
                fig.add_trace(
                    go.Scatter(
                        x=cat_df["TimeUnit"],
                        y=cat_df["Count"],
                        text=[str(int(c)) if c > 0 else "" for c in cat_df["Count"]],
                        mode="text",
                        textposition="middle center",
                        textfont=dict(size=data_label_size * 4),
                        showlegend=False
                    )
                )
        elif chart_type == "Proportion":
            fig = px.bar(
                plot_df, x="TimeUnit", y="Proportion", color=legend_var,
                barmode="stack", opacity=alpha,
                title=st.session_state["title"],
                labels={"TimeUnit": "Year" if time_filter == "Year" else "Month-Year", "Proportion": "Proportion"}
            )
            fig.update_yaxes(tickformat=".0%")
            # Add data labels
            for cat in legend_filter:
                cat_df = plot_df[plot_df[legend_var] == cat]
                fig.add_trace(
                    go.Scatter(
                        x=cat_df["TimeUnit"],
                        y=cat_df["Proportion"],
                        text=[f"{int(p * 100)}%" if p > 0 else "" for p in cat_df["Proportion"]],
                        mode="text",
                        textposition="middle center",
                        textfont=dict(size=data_label_size * 4),
                        showlegend=False
                    )
                )
        else:  # Scatter
            fig = px.scatter(
                plot_df, x=x_var, y=y_var, color=legend_var,
                opacity=alpha,
                title=st.session_state["title"],
                size=[point_size] * len(plot_df) if point_size else None,
                symbol=legend_var,
                symbol_map={cat: point_shape for cat in legend_filter} if point_shape else None,
                labels={x_var: x_var, y_var: y_var}
            )

        # Apply colors
        for trace in fig.data:
            if trace.name in color_map:
                trace.marker.color = color_map[trace.name]
                if chart_type == "Scatter":
                    trace.marker.line.color = color_map[trace.name]

        # Faceting
        if facet_var != "None" and facet_var in plot_df.columns:
            if facet_type == "Grid":
                fig = px.bar(plot_df, x="TimeUnit" if chart_type in ["Count", "Proportion"] else x_var,
                             y="Count" if chart_type == "Count" else "Proportion" if chart_type == "Proportion" else y_var,
                             color=legend_var, barmode="stack" if chart_type in ["Count", "Proportion"] else None,
                             facet_row=facet_var, opacity=alpha)
                if chart_type == "Scatter":
                    fig = px.scatter(plot_df, x=x_var, y=y_var, color=legend_var, facet_row=facet_var,
                                     opacity=alpha, size=[point_size] * len(plot_df) if point_size else None,
                                     symbol=legend_var, symbol_map={cat: point_shape for cat in legend_filter} if point_shape else None)
            else:  # Wrap
                fig = px.bar(plot_df, x="TimeUnit" if chart_type in ["Count", "Proportion"] else x_var,
                             y="Count" if chart_type == "Count" else "Proportion" if chart_type == "Proportion" else y_var,
                             color=legend_var, barmode="stack" if chart_type in ["Count", "Proportion"] else None,
                             facet_col=facet_var, facet_col_wrap=3, opacity=alpha)
                if chart_type == "Scatter":
                    fig = px.scatter(plot_df, x=x_var, y=y_var, color=legend_var, facet_col=facet_var, facet_col_wrap=3,
                                     opacity=alpha, size=[point_size] * len(plot_df) if point_size else None,
                                     symbol=legend_var, symbol_map={cat: point_shape for cat in legend_filter} if point_shape else None)

            # Reapply colors for faceted plots
            for trace in fig.data:
                if trace.name in color_map:
                    trace.marker.color = color_map[trace.name]
                    if chart_type == "Scatter":
                        trace.marker.line.color = color_map[trace.name]

        # Update layout
        fig.update_layout(
            showlegend=show_legend,
            legend=dict(orientation="h" if legend_position in ["top", "bottom"] else "v",
                        y=1.1 if legend_position == "top" else -0.1 if legend_position == "bottom" else 0.5,
                        x=0.5 if legend_position in ["top", "bottom"] else 1.02 if legend_position == "right" else -0.02,
                        xanchor="center" if legend_position in ["top", "bottom"] else "left" if legend_position == "left" else "right",
                        yanchor="top"),
            xaxis_title_font=dict(size=x_label_size),
            yaxis_title_font=dict(size=y_label_size),
            xaxis_tickfont=dict(size=x_label_size),
            yaxis_tickfont=dict(size=y_label_size),
            title=dict(text=f"{st.session_state['title']}<br><sub>{st.session_state['subtitle']}</sub>", x=0.5, xanchor="center"),
            height=600
        )

        if chart_type == "Proportion":
            fig.update_yaxes(tickformat=".0%")

        # Display plot
        st.plotly_chart(fig, use_container_width=True)

        # Download button
        buffer = io.BytesIO()
        fig.write_image(buffer, format="jpeg", width=1000, height=600)
        st.download_button(
            label="Download Plot",
            data=buffer,
            file_name=f"plot-{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )
else:
    st.info("Please upload a CSV or Excel file to begin.")
