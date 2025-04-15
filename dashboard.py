
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_q1 = pd.read_csv("cleaned_q1.csv")
df_q2 = pd.read_csv("cleaned_q2.csv")
df_q3 = pd.read_csv("cleaned_q3.csv")
df_pivot = pd.read_csv("cleaned_pivot.csv")

st.set_page_config(page_title="Excel Insights Dashboard", layout="wide")
st.title("📊 Excel-Based Business Insights Dashboard")

# Sidebar Navigation
menu = st.sidebar.radio("Navigate", ["Q1 - City & Population", "Q2 - Sales Zones", "Q3 - Manager Map", "Pivot Summary"])

if menu == "Q1 - City & Population":
    st.header("Q1: City Population Insights")
    st.subheader("Total Population by State")
    pop_by_state = df_q1.groupby("State")["Population"].sum().reset_index()
    fig1 = px.bar(pop_by_state.sort_values("Population", ascending=False), x="State", y="Population", title="Population by State")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Cities with Population > 1 Million")
    big_cities = df_q1[df_q1["Population"] > 1_000_000]
    st.dataframe(big_cities.sort_values("Population", ascending=False))

elif menu == "Q2 - Sales Zones":
    st.header("Q2: Sales by Zone & Manager")
    zone_sales = df_q2.groupby(["Zone", "Manager"])["Sales"].sum().reset_index()
    fig2 = px.bar(zone_sales, x="Zone", y="Sales", color="Manager", barmode="group", title="Sales by Manager per Zone")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_q2)

elif menu == "Q3 - Manager Map":
    st.header("Q3: Customer Regions and Managers")
    st.dataframe(df_q3)
    st.subheader("Number of Customers per Manager")
    customer_count = df_q3["Manager"].value_counts().reset_index()
    customer_count.columns = ["Manager", "Number of Customers"]
    st.bar_chart(customer_count.set_index("Manager"))

elif menu == "Pivot Summary":
    st.header("Pivot Campaign Summary")
    st.dataframe(df_pivot)
    top_campaigns = df_pivot.sort_values("Clicks", ascending=False).head(10)
    st.subheader("Top 10 Campaigns by Clicks")
    fig5 = px.bar(top_campaigns, x="Campaign", y="Clicks", title="Top Campaigns")
    st.plotly_chart(fig5, use_container_width=True)
