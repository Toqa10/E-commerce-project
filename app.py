import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# COLORS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

COLORS = {
    'primary': '#3647F5',
    'dark': '#1B2346',
    'accent': '#FF9F0D',
    'bg_dark': '#040D2F',
    'light': '#D9D9D9'
}

# Custom CSS for styling
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['light']};
    }}
    .stMetric {{
        background-color: {COLORS['dark']};
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid {COLORS['accent']};
    }}
    h1, h2, h3 {{
        color: {COLORS['accent']};
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ═══════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════

st.title("📊 E-Commerce Analytics Dashboard")
st.markdown(f"**Data Range:** {df['date'].min().date()} to {df['date'].max().date()}")
st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - FILTERS
# ═══════════════════════════════════════════════════════════════════════════

st.sidebar.title("🎛️ FILTERS")
st.sidebar.markdown("---")

# Date Range Filter
date_range = st.sidebar.date_input(
    "📅 Select Date Range:",
    value=(df['date'].min().date(), df['date'].max().date())
)

# Channels Filter
channels = st.sidebar.multiselect(
    "📢 Marketing Channels:",
    options=df['marketing_channel'].unique(),
    default=df['marketing_channel'].unique()
)

# Campaigns Filter
campaigns = st.sidebar.multiselect(
    "🎪 Marketing Campaigns:",
    options=df['marketing_campaign'].unique(),
    default=df['marketing_campaign'].unique()
)

# Segments Filter
segments = st.sidebar.multiselect(
    "👥 Customer Segments:",
    options=df['customer_segment'].unique(),
    default=df['customer_segment'].unique()
)

# Regions Filter
regions = st.sidebar.multiselect(
    "🗺️ Regions:",
    options=df['region'].unique(),
    default=df['region'].unique()
)

st.sidebar.markdown("---")

# Apply Filters
filtered_df = df[
    (df['date'].dt.date >= date_range[0]) &
    (df['date'].dt.date <= date_range[1]) &
    (df['marketing_channel'].isin(channels)) &
    (df['marketing_campaign'].isin(campaigns)) &
    (df['customer_segment'].isin(segments)) &
    (df['region'].isin(regions))
]

# ═══════════════════════════════════════════════════════════════════════════
# 1. KPI OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("🎯 Key Performance Indicators (KPIs)")

col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['net_revenue'].sum()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = filtered_df['final_amount'].mean()
avg_satisfaction = filtered_df['satisfaction_rating'].mean()

with col1:
    st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.0f}")

with col2:
    st.metric(label="👥 Total Customers", value=f"{total_customers:,}")

with col3:
    st.metric(label="📦 Avg Order Value", value=f"${avg_order_value:,.2f}")

with col4:
    st.metric(label="⭐ Satisfaction", value=f"{avg_satisfaction:.2f}/5")

col5, col6, col7, col8 = st.columns(4)

total_orders = len(filtered_df)
conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
return_rate = (filtered_df['returned'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
avg_roi = filtered_df['roi'].replace([np.inf, -np.inf], np.nan).mean()

with col5:
    st.metric(label="📋 Total Orders", value=f"{total_orders:,}")

with col6:
    st.metric(label="📊 Conversion Rate", value=f"{conversion_rate:.2f}%")

with col7:
    st.metric(label="🔄 Return Rate", value=f"{return_rate:.2f}%")

with col8:
    st.metric(label="📈 Avg ROI", value=f"{avg_roi:.2f}x")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 2. CHANNEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("📢 Marketing Channel Performance")

col1, col2 = st.columns(2)

channel_stats = filtered_df.groupby('marketing_channel').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False)

with col1:
    fig_channel = px.bar(
        x=channel_stats.index,
        y=channel_stats['net_revenue'],
        title='Revenue by Channel',
        color=channel_stats['net_revenue'],
        color_continuous_scale=['#FF9F0D', '#3647F5']
    )
    fig_channel.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with col2:
    fig_channel_pie = px.pie(
        values=channel_stats['customer_id'],
        names=channel_stats.index,
        title='Customer Distribution by Channel'
    )
    fig_channel_pie.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_channel_pie, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 3. CAMPAIGN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("🎪 Marketing Campaign Performance")

col1, col2 = st.columns(2)

campaign_stats = filtered_df.groupby('marketing_campaign').agg({
    'net_revenue': 'sum'
}).sort_values('net_revenue', ascending=False)

with col1:
    fig_campaign = px.bar(
        x=campaign_stats.index,
        y=campaign_stats['net_revenue'],
        title='Revenue by Campaign',
        color=campaign_stats['net_revenue'],
        color_continuous_scale=['#FF9F0D', '#3647F5']
    )
    fig_campaign.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_campaign, use_container_width=True)

with col2:
    fig_campaign_pie = px.pie(
        values=campaign_stats['net_revenue'],
        names=campaign_stats.index,
        title='Revenue Distribution by Campaign'
    )
    fig_campaign_pie.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_campaign_pie, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 4. REGIONAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("🗺️ Regional Performance")

col1, col2 = st.columns(2)

region_stats = filtered_df.groupby('region').agg({
    'net_revenue': 'sum'
}).sort_values('net_revenue', ascending=False)

with col1:
    fig_region = px.bar(
        x=region_stats.index,
        y=region_stats['net_revenue'],
        title='Revenue by Region',
        color=region_stats['net_revenue'],
        color_continuous_scale=['#3647F5', '#FF9F0D']
    )
    fig_region.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    fig_region_pie = px.pie(
        values=region_stats['net_revenue'],
        names=region_stats.index,
        title='Revenue Distribution by Region'
    )
    fig_region_pie.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_region_pie, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 5. CUSTOMER SEGMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("👥 Customer Segment Analysis")

col1, col2 = st.columns(2)

segment_stats = filtered_df.groupby('customer_segment').agg({
    'net_revenue': 'sum',
    'customer_lifetime_value': 'mean'
}).sort_values('net_revenue', ascending=False)

with col1:
    fig_segment = px.bar(
        x=segment_stats.index,
        y=segment_stats['net_revenue'],
        title='Revenue by Customer Segment',
        color=segment_stats['net_revenue'],
        color_continuous_scale=['#FF9F0D', '#3647F5']
    )
    fig_segment.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_segment, use_container_width=True)

with col2:
    fig_segment_clv = px.bar(
        x=segment_stats.index,
        y=segment_stats['customer_lifetime_value'],
        title='Customer Lifetime Value by Segment',
        color=segment_stats['customer_lifetime_value'],
        color_continuous_scale=['#3647F5', '#FF9F0D']
    )
    fig_segment_clv.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400
    )
    st.plotly_chart(fig_segment_clv, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 6. MONTHLY TRENDS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("📅 Monthly Trends")

col1, col2 = st.columns(2)

monthly_data = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).reset_index()
monthly_data['date'] = monthly_data['date'].astype(str)

with col1:
    fig_monthly_rev = px.line(
        monthly_data,
        x='date',
        y='net_revenue',
        markers=True,
        title='Monthly Revenue Trend'
    )
    fig_monthly_rev.update_traces(
        line=dict(color='#FF9F0D', width=3),
        marker=dict(size=8, color='#3647F5')
    )
    fig_monthly_rev.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_monthly_rev, use_container_width=True)

with col2:
    fig_monthly_cust = px.line(
        monthly_data,
        x='date',
        y='customer_id',
        markers=True,
        title='Monthly Customer Growth'
    )
    fig_monthly_cust.update_traces(
        line=dict(color='#3647F5', width=3),
        marker=dict(size=8, color='#FF9F0D')
    )
    fig_monthly_cust.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font_color='#D9D9D9',
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_monthly_cust, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 7. CATEGORY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("📦 Product Category Performance")

category_stats = filtered_df.groupby('category').agg({
    'net_revenue': 'sum'
}).sort_values('net_revenue', ascending=False).head(10)

fig_category = px.bar(
    x=category_stats['net_revenue'],
    y=category_stats.index,
    orientation='h',
    title='Top 10 Categories by Revenue',
    color=category_stats['net_revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig_category.update_layout(
    plot_bgcolor='#040D2F',
    paper_bgcolor='#040D2F',
    font_color='#D9D9D9',
    height=500
)
st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 8. SEASONAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("🌡️ Seasonal Performance")

season_stats = filtered_df.groupby('season').agg({
    'net_revenue': 'sum'
}).sort_values('net_revenue', ascending=False)

fig_season = px.bar(
    x=season_stats.index,
    y=season_stats['net_revenue'],
    title='Revenue by Season',
    color=season_stats['net_revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig_season.update_layout(
    plot_bgcolor='#040D2F',
    paper_bgcolor='#040D2F',
    font_color='#D9D9D9',
    height=400
)
st.plotly_chart(fig_season, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# 9. KEY INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("💡 Key Insights & Recommendations")

col1, col2, col3 = st.columns(3)

best_channel = channel_stats['net_revenue'].idxmax() if len(channel_stats) > 0 else "N/A"
best_campaign = campaign_stats['net_revenue'].idxmax() if len(campaign_stats) > 0 else "N/A"
best_segment = segment_stats['net_revenue'].idxmax() if len(segment_stats) > 0 else "N/A"

with col1:
    if best_channel != "N/A":
        st.info(f"🥇 Best Channel: {best_channel}\n\n💰 Revenue: ${channel_stats.loc[best_channel, 'net_revenue']:,.0f}")
    else:
        st.info("🥇 Best Channel: N/A")

with col2:
    if best_campaign != "N/A":
        st.success(f"🎯 Best Campaign: {best_campaign}\n\n💰 Revenue: ${campaign_stats.loc[best_campaign, 'net_revenue']:,.0f}")
    else:
        st.success("🎯 Best Campaign: N/A")

with col3:
    if best_segment != "N/A":
        st.warning(f"👑 Best Segment: {best_segment}\n\n💰 Revenue: ${segment_stats.loc[best_segment, 'net_revenue']:,.0f}")
    else:
        st.warning("👑 Best Segment: N/A")

st.markdown("""
### 📌 Recommendations:

1. **Focus on Top Performers:** Allocate more budget to best channels
2. **Segment Strategy:** Develop loyalty programs for high-value segments
3. **Seasonal Planning:** Plan inventory around seasonal peaks
4. **Regional Expansion:** Strengthen high-revenue regions
5. **Quality Improvement:** Monitor customer satisfaction metrics
""")

st.markdown("---")
st.markdown("✨ **Dashboard Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
