import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("Data Explorer and Visualization Dashboard")

uploaded_file = st.file_uploader("Upload csv/excel file",type=["csv","xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Show Preview
    st.subheader(" Data Preview")
    st.dataframe(df.head())

    # Show basic info
    st.subheader(" Dataset Info")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    try:
        desc = st.write(df.describe(include="all")).transpose()
        st.dataframe(desc)
    except Exception as e:
        st.warning(f"Could not generate dataset description: {e}")

    # Missing values
    st.subheader(" Missing Info")
    st.write(df.isnull().sum())

    # Visualization
    st.subheader("📊 Create a Chart")
    chart_type = st.selectbox("Select Chart Type", ["Bar", "Line", "Scatter", "Histogram"])
    x_axis = st.selectbox("Select X-axis", df.columns)
    y_axis = st.selectbox("Select Y-axis", df.columns)

    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x_axis)

    st.plotly_chart(fig, use_container_width=True)

    # Export cleaned dataset
    st.download_button(
        label="Download Cleaned CSV",
        data=df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )