import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== THEME TOGGLE ==========
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

st.sidebar.title("⚙️ Settings")
theme_mode = st.sidebar.radio(
    "🎨 Theme Mode",
    options=['🌙 Dark Mode', '☀️ Light Mode'],
    index=0 if st.session_state.theme == 'dark' else 1,
    horizontal=True
)

if '☀️' in theme_mode:
    st.session_state.theme = 'light'
else:
    st.session_state.theme = 'dark'

# ========== THEME SETTINGS ==========
if st.session_state.theme == 'light':
    # Light Mode Colors
    plot_bg = "#FFFFFF"
    paper_bg = "#FFFFFF"
    font_color = "#040D2F"
    grid_color = "#3647F5"
    marker_line_color = "#040D2F"
    
    # Custom CSS for Light Mode
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #040D2F;
        }
        .stMarkdown, .stText {
            color: #040D2F !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #040D2F !important;
        }
        .stMetric label {
            color: #040D2F !important;
        }
        .stMetric .metric-value {
            color: #FF9F0D !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Light Layout للـ Charts
    chart_layout = dict(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#040D2F",
        title_font_size=22,
        title_x=0.5,
        yaxis=dict(
            showgrid=True,
            gridcolor="#3647F5",
            zeroline=False,
            showline=False,
            tickfont=dict(color="black")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#3647F5",
            tickangle=45,
            showline=False,
            tickfont=dict(color="black")
        )
    )
else:
    # Dark Mode Colors
    plot_bg = "rgba(0,0,0,0)"
    paper_bg = "rgba(0,0,0,0)"
    font_color = "#f5f5f5"
    grid_color = "#3647F5"
    marker_line_color = "#D9D9D9"
    
    # Dark Layout للـ Charts
    chart_layout = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f5f5f5",
        title_font_size=22,
        title_x=0.5,
        yaxis=dict(
            showgrid=True,
            gridcolor="#3647F5",
            zeroline=False,
            showline=False,
            tickfont=dict(color="#D9D9D9")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#3647F5",
            tickangle=45,
            showline=False,
            tickfont=dict(color="#D9D9D9")
        )
    )

st.sidebar.markdown("---")

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_data.csv')
    df['roi'] = df['roi'].replace([np.inf, -np.inf], np.nan)
    if 'month_date' in df.columns:
        df['month_date'] = pd.to_datetime(df['month_date'])
    return df

df = load_data()

# ========== SIDEBAR FILTERS ==========
st.sidebar.header("🔍 Filters")

# Marketing Channel Filter
if 'marketing_channel' in df.columns:
    channels = ['All Channels'] + list(df['marketing_channel'].unique())
    selected_channel = st.sidebar.selectbox('Marketing Channel', channels)
else:
    selected_channel = 'All Channels'

# Date Range Filter
if 'month_date' in df.columns:
    min_date = df['month_date'].min()
    max_date = df['month_date'].max()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = []

# Apply filters
filtered_df = df.copy()
if selected_channel != 'All Channels' and 'marketing_channel' in df.columns:
    filtered_df = filtered_df[filtered_df['marketing_channel'] == selected_channel]
if len(date_range) == 2 and 'month_date' in df.columns:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['month_date'] >= pd.to_datetime(start_date)) &
        (filtered_df['month_date'] <= pd.to_datetime(end_date))
    ]

st.sidebar.success(f"📊 Showing {len(filtered_df):,} / {len(df):,} records")

# ========== MAIN DASHBOARD ==========
st.title("📊 E-Commerce Analytics Dashboard")
st.markdown("---")

# ========== KPIs ==========
st.header("📈 Key Performance Indicators")

kpi_tabs = st.tabs([
    "📊 Overall", 
    "📦 By Category", 
    "📢 By Campaign", 
    "📡 By Channel", 
    "👥 By Segment", 
    "🗺️ By Region", 
    "📅 By Time"
])

# ========== TAB 1: OVERALL KPIs ==========
with kpi_tabs[0]:
    col1, col2, col3 = st.columns(3)
    
    total_revenue = filtered_df['net_revenue'].sum() if 'net_revenue' in filtered_df.columns else 0
    total_customers = filtered_df['customer_id'].nunique() if 'customer_id' in filtered_df.columns else 0
    total_orders = len(filtered_df)
    avg_order_value = filtered_df['final_amount'].mean() if 'final_amount' in filtered_df.columns else 0
    
    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
        st.metric("📦 Total Orders", f"{total_orders:,}")
    
    with col2:
        st.metric("👥 Total Customers", f"{total_customers:,}")
        st.metric("🛍️ Avg Order Value", f"${avg_order_value:,.2f}")
    
    with col3:
        conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
        return_rate = (filtered_df['returned'].sum() / total_orders * 100) if total_orders > 0 and 'returned' in filtered_df.columns else 0
        avg_satisfaction = filtered_df['satisfaction_rating'].mean() if 'satisfaction_rating' in filtered_df.columns else 0
        
        st.metric("📊 Conversion Rate", f"{conversion_rate:.2f}%")
        st.metric("↩️ Return Rate", f"{return_rate:.2f}%")
        st.metric("⭐ Satisfaction", f"{avg_satisfaction:.2f}/5")

# ========== TAB 2: BY CATEGORY ==========
with kpi_tabs[1]:
    if 'category' in filtered_df.columns:
        kpi_category = filtered_df.groupby('category').agg({
            'gross_revenue': 'sum',
            'net_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        kpi_category['avg_order_value'] = (kpi_category['net_revenue'] / kpi_category['quantity']).round(2)
        kpi_category['roi'] = ((kpi_category['net_revenue'] - kpi_category['discount_amount']) / kpi_category['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_category.style.format({
                'gross_revenue': '${:,.2f}',
                'net_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

# ========== TAB 3: BY CAMPAIGN ==========
with kpi_tabs[2]:
    if 'marketing_campaign' in filtered_df.columns:
        kpi_campaign = filtered_df.groupby('marketing_campaign').agg({
            'net_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        kpi_campaign['revenue_per_customer'] = (kpi_campaign['net_revenue'] / kpi_campaign['customer_id']).round(2)
        kpi_campaign['roi'] = ((kpi_campaign['net_revenue'] - kpi_campaign['discount_amount']) / kpi_campaign['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_campaign.style.format({
                'net_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'customer_id': '{:,.0f}',
                'revenue_per_customer': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

# ========== TAB 4: BY CHANNEL ==========
with kpi_tabs[3]:
    if 'marketing_channel' in filtered_df.columns:
        kpi_channel = filtered_df.groupby('marketing_channel').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        kpi_channel['avg_order_value'] = (kpi_channel['net_revenue'] / kpi_channel['quantity']).round(2)
        kpi_channel['revenue_per_customer'] = (kpi_channel['net_revenue'] / kpi_channel['customer_id']).round(2)
        kpi_channel['roi'] = ((kpi_channel['net_revenue'] - kpi_channel['discount_amount']) / kpi_channel['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_channel.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'customer_id': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'revenue_per_customer': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

# ========== TAB 5: BY SEGMENT ==========
with kpi_tabs[4]:
    if 'customer_segment' in filtered_df.columns:
        kpi_segment = filtered_df.groupby('customer_segment').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
            'customer_lifetime_value': 'mean',
            'retention_score': 'mean'
        }).reset_index()
        
        kpi_segment['avg_order_value'] = (kpi_segment['net_revenue'] / kpi_segment['quantity']).round(2)
        kpi_segment['revenue_per_customer'] = (kpi_segment['net_revenue'] / kpi_segment['customer_id']).round(2)
        kpi_segment['roi'] = ((kpi_segment['net_revenue'] - kpi_segment['discount_amount']) / kpi_segment['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_segment.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'customer_id': '{:,.0f}',
                'customer_lifetime_value': '${:,.2f}',
                'retention_score': '{:.2f}',
                'avg_order_value': '${:,.2f}',
                'revenue_per_customer': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

# ========== TAB 6: BY REGION ==========
with kpi_tabs[5]:
    if 'region' in filtered_df.columns:
        kpi_region = filtered_df.groupby('region').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        kpi_region['avg_order_value'] = (kpi_region['net_revenue'] / kpi_region['quantity']).round(2)
        kpi_region['revenue_per_customer'] = (kpi_region['net_revenue'] / kpi_region['customer_id']).round(2)
        kpi_region['roi'] = ((kpi_region['net_revenue'] - kpi_region['discount_amount']) / kpi_region['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_region.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'customer_id': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'revenue_per_customer': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

# ========== TAB 7: BY TIME ==========
with kpi_tabs[6]:
    time_view = st.radio("Select Time Period", ["Month", "Quarter", "Season"], horizontal=True)
    
    if time_view == "Month" and 'month' in filtered_df.columns:
        kpi_time = filtered_df.groupby('month').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        kpi_time['avg_order_value'] = (kpi_time['net_revenue'] / kpi_time['quantity']).round(2)
        kpi_time['roi'] = ((kpi_time['net_revenue'] - kpi_time['discount_amount']) / kpi_time['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_time.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )
    
    elif time_view == "Quarter" and 'quarter' in filtered_df.columns:
        kpi_time = filtered_df.groupby('quarter').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        kpi_time['avg_order_value'] = (kpi_time['net_revenue'] / kpi_time['quantity']).round(2)
        kpi_time['roi'] = ((kpi_time['net_revenue'] - kpi_time['discount_amount']) / kpi_time['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_time.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )
    
    elif time_view == "Season" and 'season' in filtered_df.columns:
        kpi_time = filtered_df.groupby('season').agg({
            'net_revenue': 'sum',
            'gross_revenue': 'sum',
            'discount_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        kpi_time['avg_order_value'] = (kpi_time['net_revenue'] / kpi_time['quantity']).round(2)
        kpi_time['roi'] = ((kpi_time['net_revenue'] - kpi_time['discount_amount']) / kpi_time['discount_amount'] * 100).round(2)
        
        st.dataframe(
            kpi_time.style.format({
                'net_revenue': '${:,.2f}',
                'gross_revenue': '${:,.2f}',
                'discount_amount': '${:,.2f}',
                'quantity': '{:,.0f}',
                'avg_order_value': '${:,.2f}',
                'roi': '{:.2f}%'
            }),
            use_container_width=True
        )

st.markdown("---")

# ========== CHARTS ==========
st.header("📊 Data Visualizations")
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🎯 Marketing", "📊 Performance", "👥 Customers"])

# ========== TAB 1: TRENDS ==========
with tab1:
    if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
        st.subheader("Monthly Revenue Trends by Marketing Channel")
        
        monthly_channel = filtered_df.groupby(['month_date', 'marketing_channel']).agg({
            'net_revenue': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        fig_rev = px.line(
            monthly_channel,
            x='month_date',
            y='net_revenue',
            color='marketing_channel',
            markers=True,
            title='Monthly Revenue by Channel'
        )
        fig_rev.update_layout(**chart_layout, height=450)
        st.plotly_chart(fig_rev, use_container_width=True)
        
        # Overall Revenue Trend
        st.subheader("Overall Monthly Revenue")
        monthly_total = filtered_df.groupby('month_date').agg({
            'net_revenue': 'sum'
        }).reset_index()
        
        fig_total_rev = px.line(
            monthly_total,
            x='month_date',
            y='net_revenue',
            markers=True,
            title='Overall Monthly Revenue'
        )
        fig_total_rev.update_traces(
            line=dict(color="#3647F5", width=3),
            marker=dict(size=8, color="#FF9F0D")
        )
        fig_total_rev.update_layout(**chart_layout, height=400)
        st.plotly_chart(fig_total_rev, use_container_width=True)

# ========== TAB 2: MARKETING ==========
with tab2:
    if 'marketing_channel' in filtered_df.columns:
        st.subheader("Marketing Channel Performance")
        
        channel_perf = filtered_df.groupby('marketing_channel').agg({
            'net_revenue': 'sum',
            'customer_id': 'nunique',
            'discount_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        channel_perf.columns = ['Channel', 'total_revenue', 'total_conversions', 'total_spend', 'total_quantity']
        channel_perf['avg_roi'] = ((channel_perf['total_revenue'] - channel_perf['total_spend']) / channel_perf['total_spend'] * 100).round(2)
        channel_perf = channel_perf.sort_values(by='avg_roi', ascending=True)
        
        # Total Revenue - Vertical Bar with Bubbles
        st.subheader("💰 Total Revenue per Marketing Channel")
        bar_width = 25
        
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=channel_perf['Channel'],
            y=channel_perf['total_revenue'],
            mode='markers+text',
            marker=dict(color="#3647F5", size=bar_width),
            text=channel_perf['total_revenue'],
            textposition='top center',
            texttemplate='%{text:.2s}'
        ))
        
        for x_val, y_val in zip(channel_perf['Channel'], channel_perf['total_revenue']):
            fig_rev.add_shape(
                type="line",
                x0=x_val, y0=0,
                x1=x_val, y1=y_val,
                line=dict(color="#3647F5", width=bar_width),
                layer="below"
            )
        
        fig_rev.update_layout(
            **chart_layout,
            title="Total Revenue per Marketing Channel",
            height=450,
            margin=dict(t=60)
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        
        # Total Conversions - Bubble Chart
        st.subheader("📈 Total Conversions per Channel")
        fig_conv = px.scatter(
            channel_perf,
            x='Channel',
            y='total_conversions',
            size='total_conversions',
            color='total_conversions',
            color_continuous_scale=["#FF9F0D", "#D9D9D9"],
            text='total_conversions',
            title="Total Conversions per Channel"
        )
        fig_conv.update_traces(
            marker=dict(line=dict(width=2, color=marker_line_color)),
            textposition='top center'
        )
        fig_conv.update_layout(**chart_layout, height=450, yaxis_title="Total Conversions", xaxis_title="Marketing Channel")
        st.plotly_chart(fig_conv, use_container_width=True)
        
        # Average ROI - Horizontal Bar
        st.subheader("💹 Average ROI per Channel")
        fig_roi = px.bar(
            channel_perf,
            x='avg_roi',
            y='Channel',
            orientation='h',
            color='avg_roi',
            color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D'],
            title="Average ROI per Channel"
        )
        fig_roi.update_layout(**chart_layout, height=450, xaxis_title="Average ROI", yaxis_title="Marketing Channel")
        st.plotly_chart(fig_roi, use_container_width=True)

# ========== TAB 3: PERFORMANCE ==========
with tab3:
    st.subheader("📊 Marketing Channel Performance Analysis")
    
    if 'marketing_channel' in filtered_df.columns:
        performance_by_channel = filtered_df.groupby('marketing_channel').agg({
            'final_amount': ['sum', 'mean'],
            'order_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        performance_by_channel.columns = ['Channel', 'Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Unique_Customers']
        performance_by_channel['Revenue_Per_Order'] = (performance_by_channel['Total_Revenue'] / performance_by_channel['Total_Orders']).round(2)
        
        # Chart 1: Revenue Per Order
        st.subheader("💵 Revenue Per Order by Channel")
        performance_sorted = performance_by_channel.sort_values('Revenue_Per_Order')
        
        fig_revenue_order = px.bar(
            performance_sorted,
            x='Revenue_Per_Order',
            y='Channel',
            orientation='h',
            title='Revenue Per Order by Channel',
            color='Revenue_Per_Order',
            color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
        )
        fig_revenue_order.update_traces(marker=dict(line=dict(width=1.5, color=marker_line_color)))
        fig_revenue_order.update_layout(**chart_layout, height=450, xaxis_title="Revenue Per Order ($)", yaxis_title="Marketing Channel")
        st.plotly_chart(fig_revenue_order, use_container_width=True)
        
        # Chart 2: Customer Acquisition Rate
        st.subheader("📈 Customer Acquisition Rate by Channel")
        conversion_by_channel = filtered_df.groupby('marketing_channel').agg({
            'customer_id': 'nunique',
            'order_id': 'count'
        }).reset_index()
        conversion_by_channel.columns = ['Channel', 'Unique_Customers', 'Total_Orders']
        conversion_by_channel['Customer_Acquisition_Rate_%'] = ((conversion_by_channel['Unique_Customers'] / conversion_by_channel['Total_Orders']) * 100).round(2)
        conversion_by_channel = conversion_by_channel.sort_values('Customer_Acquisition_Rate_%', ascending=False)
        
        fig_acquisition = px.bar(
            conversion_by_channel,
            x='Channel',
            y='Customer_Acquisition_Rate_%',
            title='Customer Acquisition Rate by Channel',
            color='Customer_Acquisition_Rate_%',
            color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
        )
        fig_acquisition.update_traces(marker=dict(line=dict(width=1.5, color=marker_line_color)))
        fig_acquisition.update_layout(**chart_layout, height=450, xaxis_title="Marketing Channel", yaxis_title="Customer Acquisition Rate (%)")
        st.plotly_chart(fig_acquisition, use_container_width=True)
        
        # Chart 3: Channel Efficiency Ranking
        st.subheader("🏆 Channel Efficiency Ranking")
        efficiency = filtered_df.groupby('marketing_channel').agg({
            'final_amount': ['sum', 'mean'],
            'order_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        efficiency.columns = ['Channel', 'Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Unique_Customers']
        efficiency['Revenue_Per_Order'] = (efficiency['Total_Revenue'] / efficiency['Total_Orders']).round(2)
        efficiency['Customer_Acq_Rate_%'] = ((efficiency['Unique_Customers'] / efficiency['Total_Orders']) * 100).round(2)
        
        max_rev = efficiency['Revenue_Per_Order'].max()
        max_cust = efficiency['Customer_Acq_Rate_%'].max()
        max_order = efficiency['Avg_Order_Value'].max()
        
        efficiency['Efficiency_Score'] = (
            (efficiency['Revenue_Per_Order'] / max_rev) * 40 +
            (efficiency['Customer_Acq_Rate_%'] / max_cust) * 30 +
            (efficiency['Avg_Order_Value'] / max_order) * 30
        ).round(2)
        efficiency = efficiency.sort_values('Efficiency_Score')
        
        fig_efficiency = px.bar(
            efficiency,
            x='Efficiency_Score',
            y='Channel',
            orientation='h',
            title='Channel Efficiency Ranking',
            color='Efficiency_Score',
            color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
        )
        fig_efficiency.update_traces(marker=dict(line=dict(width=1.5, color=marker_line_color)))
        fig_efficiency.update_layout(**chart_layout, height=450, xaxis_title="Efficiency Score", yaxis_title="Marketing Channel")
        st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # Chart 4: Revenue vs Customer Acquisition
        st.subheader("🎯 Revenue vs Customer Acquisition")
        revenue_analysis = filtered_df.groupby('marketing_channel').agg({
            'final_amount': 'sum',
            'customer_id': 'nunique',
            'order_id': 'count'
        }).reset_index()
        revenue_analysis.columns = ['Channel', 'Total_Revenue', 'Unique_Customers', 'Total_Orders']
        revenue_analysis['Revenue_Per_Customer'] = (revenue_analysis['Total_Revenue'] / revenue_analysis['Unique_Customers']).round(2)
        
        fig_revenue_customers = px.scatter(
            revenue_analysis,
            x='Unique_Customers',
            y='Total_Revenue',
            size='Revenue_Per_Customer',
            color='Revenue_Per_Customer',
            hover_name='Channel',
            text='Channel',
            title='Revenue vs Customer Acquisition',
            size_max=60,
            color_continuous_scale=['#FF9F0D', '#3647F5', '#D9D9D9']
        )
        fig_revenue_customers.update_traces(
            textposition='top center',
            textfont=dict(size=12, color=font_color),
            marker=dict(line=dict(width=2, color=marker_line_color), opacity=0.85)
        )
        fig_revenue_customers.update_layout(**chart_layout, height=500, showlegend=False, xaxis_title="Unique Customers Acquired", yaxis_title="Total Revenue ($)")
        st.plotly_chart(fig_revenue_customers, use_container_width=True)
        
        # Chart 5: Revenue Per Customer
        st.subheader("💰 Revenue Per Customer by Channel")
        customer_value = filtered_df.groupby('marketing_channel').agg({
            'final_amount': 'sum',
            'customer_id': 'nunique',
            'order_id': 'count'
        }).reset_index()
        customer_value.columns = ['Channel', 'Total_Revenue', 'Total_Customers', 'Total_Orders']
        customer_value['Revenue_Per_Customer'] = (customer_value['Total_Revenue'] / customer_value['Total_Customers']).round(2)
        customer_value = customer_value.sort_values('Revenue_Per_Customer')
        
        fig_revenue_customer = px.bar(
            customer_value,
            x='Channel',
            y='Revenue_Per_Customer',
            title='Revenue Per Customer by Channel',
            color='Revenue_Per_Customer',
            color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
        )
        fig_revenue_customer.update_traces(marker=dict(line=dict(width=1.5, color=marker_line_color)))
        fig_revenue_customer.update_layout(**chart_layout, height=450, xaxis_title="Marketing Channel", yaxis_title="Revenue Per Customer ($)")
        st.plotly_chart(fig_revenue_customer, use_container_width=True)
        
        # Chart 6: Performance Quadrant Analysis
        st.subheader("🏆 Performance Quadrant Analysis")
        
        quadrant_analysis = filtered_df.groupby('marketing_channel').agg({
            'customer_id': 'nunique',
            'final_amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        quadrant_analysis.columns = ['Channel', 'Unique_Customers', 'Total_Revenue', 'Total_Orders']
        quadrant_analysis['Revenue_Per_Customer'] = (quadrant_analysis['Total_Revenue'] / quadrant_analysis['Unique_Customers']).round(2)
        
        avg_customers = quadrant_analysis['Unique_Customers'].mean()
        avg_revenue = quadrant_analysis['Total_Revenue'].mean()
        
        fig_quadrant = px.scatter(
            quadrant_analysis,
            x='Unique_Customers',
            y='Total_Revenue',
            size='Revenue_Per_Customer',
            color='Revenue_Per_Customer',
            hover_name='Channel',
            hover_data=['Revenue_Per_Customer', 'Total_Orders'],
            title='Performance Quadrant Analysis: High Revenue/High Reach = Top Right 🏆',
            size_max=50,
            color_continuous_scale=['#FF9F0D', '#3647F5']
        )
        
        fig_quadrant.update_traces(marker=dict(line=dict(width=2, color=marker_line_color), opacity=0.9))
        fig_quadrant.update_layout(**chart_layout, height=500, xaxis_title="Unique Customers Acquired", yaxis_title="Total Revenue ($)", showlegend=False)
        
        fig_quadrant.add_hline(y=avg_revenue, line_dash="dash", line_color="#FF9F0D", annotation_text=f"Avg Revenue: ${avg_revenue:,.0f}", annotation_position="right")
        fig_quadrant.add_vline(x=avg_customers, line_dash="dash", line_color="#FF9F0D", annotation_text=f"Avg Customers: {avg_customers:,.0f}", annotation_position="top")
        
        st.plotly_chart(fig_quadrant, use_container_width=True)
        
        best_channel = quadrant_analysis.loc[quadrant_analysis['Revenue_Per_Customer'].idxmax()]
        st.success(f"🌟 **Best Performer:** {best_channel['Channel']} - Revenue/Customer: ${best_channel['Revenue_Per_Customer']:,.2f}")

# ========== TAB 4: CUSTOMERS ==========
with tab4:
    if 'customer_segment' in filtered_df.columns:
        st.subheader("Customer Segmentation Analysis")
        
        segment_analysis = filtered_df.groupby('customer_segment').agg({
            'customer_id': 'nunique',
            'final_amount': 'sum'
        }).reset_index()
        segment_analysis.columns = ['Segment', 'Total_Customers', 'Total_Revenue']
        
        fig_segment = px.pie(
            segment_analysis,
            values='Total_Customers',
            names='Segment',
            title='Customer Distribution by Segment',
            color_discrete_sequence=['#3647F5', '#FF9F0D', '#D9D9D9']
        )
        fig_segment.update_layout(**chart_layout, height=450)
        st.plotly_chart(fig_segment, use_container_width=True)

st.markdown("---")
st.markdown("### 📌 Dashboard created with Streamlit")
