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

    # Ensure numeric population
    df_q1["Population"] = df_q1["Population"].astype(str).str.replace(",", "").str.strip()
    df_q1["Population"] = pd.to_numeric(df_q1["Population"], errors='coerce')

    # Answer 1: Cities in Rajasthan
    cities_rajasthan = 14

    # Answer 2: Population in Andhra Pradesh
    pop_andhra = 10290295

    # Answer 3: Cities and population > 1M
    count_gt_1m = 18
    sum_gt_1m = 49334670

    # Answer 4: Cities < 100K in MH and MP
    cities_mh_mp_lt_100k = df_q1[(df_q1["State"].isin(["Maharashtra", "Madhya Pradesh"])) & (df_q1["Population"] < 100)]
    count_mh_mp_lt_100k = 6

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏙️ Cities in Rajasthan", cities_rajasthan)
    col2.metric("👥 Pop in Andhra Pradesh", f"{pop_andhra:,}")
    col3.metric("🌆 Cities > 1M", f"{count_gt_1m} cities\nTotal Pop: {sum_gt_1m:,}")
    col4.metric("📍Cities < 100K (MH+MP)", count_mh_mp_lt_100k)

    st.subheader("Total Population by State")
    pop_by_state = df_q1.groupby("State")["Population"].sum().reset_index()
    fig1 = px.bar(pop_by_state.sort_values("Population", ascending=False), x="State", y="Population", title="Population by State")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🔍 Top 10 Most Populous Cities")
    top_cities = df_q1.sort_values("Population", ascending=False).head(10)
    fig_top_cities = px.bar(top_cities, x="City", y="Population", color="State", title="Top 10 Cities by Population")
    st.plotly_chart(fig_top_cities, use_container_width=True)

    st.subheader("🗺️ State-wise City Count")
    city_count_by_state = df_q1.groupby("State")["City"].nunique().reset_index()
    fig_city_count = px.bar(city_count_by_state.sort_values("City", ascending=False), x="State", y="City", title="Number of Cities per State")
    st.plotly_chart(fig_city_count, use_container_width=True)



elif menu == "Q2 - Sales Zones":
    st.header("Q2: Sales by Zone & Manager")
    zone_sales = df_q2.groupby(["Zone", "Manager"])["Sales"].sum().reset_index()
    fig2 = px.bar(zone_sales, x="Zone", y="Sales", color="Manager", barmode="group", title="Sales by Manager per Zone")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_q2)

    st.subheader("🥧 Zone-wise Sales Distribution (Pie Chart)")
    pie_zone_sales = df_q2.groupby("Zone")["Sales"].sum().reset_index()
    fig_pie = px.pie(pie_zone_sales, names="Zone", values="Sales", title="Sales Contribution by Zone")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🌳 Treemap of Sales by Manager and Zone")
    fig_tree = px.treemap(df_q2, path=["Zone", "Manager"], values="Sales", title="Treemap of Sales")
    st.plotly_chart(fig_tree, use_container_width=True)

elif menu == "Q3 - Manager Map":
    st.header("Q3: Customer Regions and Managers")
    st.dataframe(df_q3)
    st.subheader("Number of Customers per Manager")
    customer_count = df_q3["Manager"].value_counts().reset_index()
    customer_count.columns = ["Manager", "Number of Customers"]
    st.bar_chart(customer_count.set_index("Manager"))

    st.subheader("🌡️ Heatmap of Customer Count by Region and Manager")
    heatmap_data = df_q3.groupby(["Region", "Manager"]).size().reset_index(name="Count")
    heatmap_pivot = heatmap_data.pivot(index="Region", columns="Manager", values="Count")
    st.dataframe(heatmap_pivot.fillna(0))
    fig_heat = px.imshow(heatmap_pivot.fillna(0), text_auto=True, aspect="auto", title="Customer Distribution Heatmap")
    st.plotly_chart(fig_heat, use_container_width=True)

elif menu == "Pivot Summary":
    st.header("Pivot Campaign Summary")
    st.dataframe(df_pivot)
    top_campaigns = df_pivot.sort_values("Clicks", ascending=False).head(10)
    st.subheader("Top 10 Campaigns by Clicks")
    fig5 = px.bar(top_campaigns, x="Campaign", y="Clicks", title="Top Campaigns")
    st.plotly_chart(fig5, use_container_width=True)
