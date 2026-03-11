import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Falcon5 O&M Dashboard", layout="wide")

# --- LOAD EXCEL DATA ---
@st.cache_data
def load_data():
    # This reads the 'KPI Register' sheet from your Excel file
    return pd.read_excel('Falcon5_KPI_Register.xlsx', sheet_name='KPI Register')

try:
    df = load_data()
    st.title("📊 Falcon5 O&M Project Dashboard")

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Global Filters")
    selected_domain = st.sidebar.multiselect("Select Domain", df['Domain'].unique(), default=df['Domain'].unique())
    
    filtered_df = df[df['Domain'].isin(selected_domain)]

    # --- METRIC CARDS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total KPIs", len(filtered_df))
    col2.metric("Domains Active", filtered_df['Domain'].nunique())
    col3.metric("Owners", filtered_df['Owner'].nunique())

    # --- CHARTS ---
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.pie(filtered_df, names='Domain', title="KPI Distribution by Domain")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.bar(filtered_df, x='Subdomain', color='Domain', title="KPIs by Subdomain")
        st.plotly_chart(fig2, use_container_width=True)

    # --- DATA TABLE ---
    st.subheader("Current KPI Status")
    st.dataframe(filtered_df[['KPI ID', 'KPI Name', 'Target', 'Owner', 'Frequency']], use_container_width=True)

except Exception as e:
    st.error(f"Error: Please ensure your file is named 'Falcon5_KPI_Register.xlsx' and has a sheet named 'KPI Register'.")
    st.info(f"Technical details: {e}")
