import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------
# STREAMLIT CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="Marketing Dashboard",
    layout="wide",
    page_icon="📊"
)

# ---------------------------------------------
# COLORS (THEME)
# ---------------------------------------------
PRIMARY = "#3647F5"
DARK = "#1B2346"
ACCENT = "#FF9F0D"
BG = "#040D2F"
LIGHT = "#D9D9D9"

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")

    # Fix dates
    if "date" in df:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "month" not in df:
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    df["month"] = pd.to_datetime(df["month"], errors="coerce")

    return df

df = load_data()

# ---------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------
st.sidebar.header("🔎 Filters")

# Channel Filter
channels = df["marketing_channel"].dropna().unique()
channel_filter = st.sidebar.multiselect(
    "Marketing Channel",
    options=list(channels),
    default=list(channels)
)

# Month Range
valid_months = df["month"].dropna().sort_values()
min_m = valid_months.min().to_pydatetime()
max_m = valid_months.max().to_pydatetime()

month_range = st.sidebar.slider(
    "Month Range",
    min_value=min_m,
    max_value=max_m,
    value=(min_m, max_m),
    format="MMM YYYY"
)

# Filter Data
df_filtered = df[
    (df["marketing_channel"].isin(channel_filter)) &
    (df["month"] >= month_range[0]) &
    (df["month"] <= month_range[1])
]

# ---------------------------------------------
# TABS
# ---------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 KPIs & Overview",
    "📈 Channel Performance",
    "📆 Time Trends",
    "⚙ Efficiency",
    "ℹ About & Recommendations"
])

# ---------------------------------------------
# TAB 1 — KPIs & OVERVIEW
# ---------------------------------------------
with tab1:
    st.title("📊 Overview & KPIs")

    col1, col2, col3, col4 = st.columns(4)

    total_revenue = df_filtered["net_revenue"].sum()
    avg_order = df_filtered["Average Order Value"].mean()
    retention = df_filtered["retention_score"].mean()
    conversion = df_filtered["conversion_rate"].mean()

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Avg Order Value", f"${avg_order:,.2f}")
    col3.metric("Retention Score", f"{retention:.2f}")
    col4.metric("Conversion Rate", f"{conversion:.2f}%")

    st.subheader("Revenue by Category")

    fig, ax = plt.subplots(figsize=(8, 4))
    df_filtered.groupby("category")["net_revenue"].sum().plot(kind="bar", ax=ax, color=PRIMARY)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------------------------
# TAB 2 — CHANNEL PERFORMANCE
# ---------------------------------------------
with tab2:
    st.title("📈 Analyze Total Performance per Channel")

    perf = df_filtered.groupby("marketing_channel").agg({
        "spend": "sum" if "spend" in df_filtered else "mean",
        "net_revenue": "sum",
        "conversion_rate": "mean",
        "roi": "mean"
    })

    st.write("### Channel Performance Table")
    st.dataframe(perf)

    st.subheader("Revenue per Channel")
    fig, ax = plt.subplots(figsize=(8, 4))
    perf["net_revenue"].plot(kind="bar", ax=ax, color=ACCENT)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------------------------
# TAB 3 — TIME TRENDS
# ---------------------------------------------
with tab3:
    st.title("📆 Time Trends Analysis")

    monthly_rev = df_filtered.groupby("month")["net_revenue"].sum()

    st.subheader("Monthly Revenue Trend")
    fig, ax = plt.subplots(figsize=(8, 4))
    monthly_rev.plot(ax=ax, marker="o", color=PRIMARY)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    monthly_conv = df_filtered.groupby("month")["conversion_rate"].mean()

    st.subheader("Monthly Conversion Trend")
    fig, ax = plt.subplots(figsize=(8, 4))
    monthly_conv.plot(ax=ax, marker="o", color=ACCENT)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------------------------
# TAB 4 — EFFICIENCY
# ---------------------------------------------
with tab4:
    st.title("⚙ Cost Efficiency & Spend Impact")

    st.subheader("Avg CPC per Channel")
    if "cpc" in df_filtered:
        cpc = df_filtered.groupby("marketing_channel")["cpc"].mean()

        fig, ax = plt.subplots(figsize=(8, 4))
        cpc.plot(kind="bar", ax=ax, color=PRIMARY)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.subheader("ROI per Channel")
    roi = df_filtered.groupby("marketing_channel")["roi"].mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    roi.plot(kind="bar", ax=ax, color=ACCENT)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------------------------
# TAB 5 — ABOUT & RECOMMENDATIONS
# ---------------------------------------------
with tab5:
    st.title("ℹ About the Dashboard")
    st.write("""
    This dashboard is built to analyze marketing channel performance,
    time trends, efficiency, and provide clear recommendations.
    """)

    st.header("💡 Recommendations")
    st.write("""
    - Allocate more budget to channels with higher ROI.  
    - Improve targeting in channels with low conversion rates.  
    - Track monthly performance to identify seasonal peaks.  
    - Maintain spending efficiency by monitoring CPC.  
    """)

