import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample Data Generation
@st.cache_data
def load_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-10', freq='D')
    channels = ['Social Media', 'Email', 'Direct', 'Organic Search', 'Paid Ads']
    
    data = []
    for date in dates:
        for channel in channels:
            data.append({
                'date': date,
                'channel': channel,
                'revenue': np.random.uniform(1000, 10000),
                'orders': np.random.randint(10, 100),
                'customers': np.random.randint(5, 80),
                'conversion_rate': np.random.uniform(0.01, 0.15),
                'avg_order_value': np.random.uniform(50, 200)
            })
    
    return pd.DataFrame(data)

df = load_data()

# Sidebar - Filters
with st.sidebar:
    st.title("🎯 Filters")
    
    st.markdown("---")
    
    # Channel Filter
    st.subheader("📡 Channel")
    channels = st.multiselect(
        "Select Channels",
        options=df['channel'].unique(),
        default=df['channel'].unique()
    )
    
    # Date Range Filter
    st.subheader("📅 Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

# Apply Filters
filtered_df = df[
    (df['channel'].isin(channels)) &
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date)
]

# Main Title
st.title("📊 Performance Analytics Dashboard")
st.caption(f"Period: {start_date} to {end_date}")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 KPIs & Overview",
    "🔍 Performance Analysis",
    "📉 Time Trends & Efficiency",
    "💡 About & Recommendations"
])

# TAB 1: KPIs & Overview
with tab1:
    st.header("Key Performance Indicators")
    
    # Calculate KPIs
    total_revenue = filtered_df['revenue'].sum()
    total_orders = filtered_df['orders'].sum()
    total_customers = filtered_df['customers'].sum()
    avg_conversion = filtered_df['conversion_rate'].mean()
    avg_order_val = filtered_df['avg_order_value'].mean()
    
    # KPI Cards using Streamlit metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{(total_revenue/1000000):.1f}M"
        )
    
    with col2:
        st.metric(
            label="🛒 Total Orders",
            value=f"{total_orders:,}",
            delta=f"{total_orders}"
        )
    
    with col3:
        st.metric(
            label="👥 Total Customers",
            value=f"{total_customers:,}",
            delta=f"{total_customers}"
        )
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.metric(
            label="📊 Avg Conversion Rate",
            value=f"{avg_conversion*100:.2f}%",
            delta=f"{avg_conversion*100:.1f}%"
        )
    
    with col5:
        st.metric(
            label="💵 Avg Order Value",
            value=f"${avg_order_val:.2f}",
            delta=f"${avg_order_val:.0f}"
        )
    
    st.divider()
    
    # Overview Charts
    st.subheader("📊 Performance Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Channel
        channel_revenue = filtered_df.groupby('channel')['revenue'].sum().reset_index()
        fig = px.pie(
            channel_revenue, 
            values='revenue', 
            names='channel', 
            title='Revenue Distribution by Channel',
            color_discrete_sequence=px.colors.sequential.Purples,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders by Channel
        channel_orders = filtered_df.groupby('channel')['orders'].sum().reset_index()
        fig = px.bar(
            channel_orders, 
            x='channel', 
            y='orders',
            title='Total Orders by Channel',
            color='orders',
            color_continuous_scale='Purples',
            text='orders'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Performance Analysis
with tab2:
    st.header("Performance Analysis by Channel")
    
    # Performance Metrics Table
    performance_summary = filtered_df.groupby('channel').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'customers': 'sum',
        'conversion_rate': 'mean',
        'avg_order_value': 'mean'
    }).reset_index()
    
    performance_summary.columns = ['Channel', 'Total Revenue', 'Total Orders', 
                                   'Total Customers', 'Avg Conversion Rate', 'Avg Order Value']
    
    st.dataframe(
        performance_summary.style.format({
            'Total Revenue': '${:,.2f}',
            'Total Orders': '{:,.0f}',
            'Total Customers': '{:,.0f}',
            'Avg Conversion Rate': '{:.2%}',
            'Avg Order Value': '${:.2f}'
        }).background_gradient(cmap='Purples', subset=['Total Revenue']),
        use_container_width=True,
        height=250
    )
    
    st.divider()
    
    # Detailed Channel Analysis
    st.subheader("📈 Channel Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            performance_summary, 
            x='Total Orders', 
            y='Total Revenue',
            size='Total Customers', 
            color='Channel',
            title='Revenue vs Orders (sized by Customers)',
            color_discrete_sequence=px.colors.qualitative.Bold,
            size_max=50
        )
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            performance_summary, 
            x='Channel', 
            y='Avg Conversion Rate',
            title='Average Conversion Rate by Channel',
            color='Avg Conversion Rate',
            color_continuous_scale='Purples',
            text='Avg Conversion Rate'
        )
        fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Time Trends & Efficiency
with tab3:
    st.header("Time Trends Analysis")
    
    # Daily Trends
    daily_trends = filtered_df.groupby('date').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'conversion_rate': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            daily_trends, 
            x='date', 
            y='revenue',
            title='Revenue Trend Over Time',
            labels={'date': 'Date', 'revenue': 'Revenue ($)'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            daily_trends, 
            x='date', 
            y='orders',
            title='Orders Trend Over Time',
            labels={'date': 'Date', 'orders': 'Orders'},
            color_discrete_sequence=['#764ba2']
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Efficiency Metrics
    st.subheader("⚡ Efficiency Analysis")
    
    # Calculate Efficiency Metrics
    efficiency_df = filtered_df.groupby('channel').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'customers': 'sum'
    }).reset_index()
    
    efficiency_df['Revenue per Order'] = efficiency_df['revenue'] / efficiency_df['orders']
    efficiency_df['Revenue per Customer'] = efficiency_df['revenue'] / efficiency_df['customers']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            efficiency_df, 
            x='channel', 
            y='Revenue per Order',
            title='Revenue per Order by Channel',
            color='Revenue per Order',
            color_continuous_scale='Teal',
            text='Revenue per Order'
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            efficiency_df, 
            x='channel', 
            y='Revenue per Customer',
            title='Revenue per Customer by Channel',
            color='Revenue per Customer',
            color_continuous_scale='Viridis',
            text='Revenue per Customer'
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly Performance Heatmap
    st.subheader("📅 Weekly Performance Heatmap")
    
    # Create copy to avoid modifying original
    temp_df = filtered_df.copy()
    temp_df['day_of_week'] = temp_df['date'].dt.day_name()
    temp_df['week'] = temp_df['date'].dt.isocalendar().week
    
    weekly_revenue = temp_df.pivot_table(
        values='revenue', 
        index='day_of_week',
        columns='week',
        aggfunc='sum'
    )
    
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_revenue = weekly_revenue.reindex([d for d in day_order if d in weekly_revenue.index])
    
    fig = px.imshow(
        weekly_revenue,
        labels=dict(x="Week Number", y="Day of Week", color="Revenue ($)"),
        title="Revenue Heatmap by Day and Week",
        color_continuous_scale='Purples',
        aspect='auto'
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: About & Recommendations
with tab4:
    st.header("About This Dashboard")
    
    with st.expander("📊 Dashboard Overview", expanded=True):
        st.markdown("""
        This interactive dashboard provides comprehensive performance analytics across multiple dimensions:
        
        - *KPIs & Overview*: High-level metrics with key performance indicators
        - *Performance Analysis*: Channel-by-channel performance breakdown
        - *Time Trends*: Historical trends and efficiency metrics
        - *Recommendations*: Data-driven insights for optimization
        """)
    
    st.divider()
    
    st.header("💡 Key Recommendations")
    
    if len(performance_summary) > 0:
        # Generate Dynamic Recommendations based on data
        top_channel = performance_summary.loc[performance_summary['Total Revenue'].idxmax(), 'Channel']
        worst_channel = performance_summary.loc[performance_summary['Total Revenue'].idxmin(), 'Channel']
        best_conversion = performance_summary.loc[performance_summary['Avg Conversion Rate'].idxmax(), 'Channel']
        
        st.subheader("🎯 Strategic Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"*Top Performer*: {top_channel}")
            st.write("Your highest revenue generator. Consider allocating more resources here.")
            
            st.info(f"*Conversion Excellence*: {best_conversion}")
            st.write("Best conversion rate. Study and replicate its tactics across other channels.")
        
        with col2:
            st.warning(f"*Optimization Opportunity*: {worst_channel}")
            st.write("Shows lower performance. Analyze and optimize this channel's strategy.")
            
            st.info("*Time-Based Insights*")
            st.write("Review the weekly heatmap to identify peak performance days and schedule campaigns accordingly.")
        
        st.divider()
        
        st.subheader("📈 Next Steps")
        
        steps = [
            "Conduct A/B testing on underperforming channels",
            "Invest in top-performing channels during peak periods",
            "Implement cross-channel learnings from high-conversion channels",
            "Monitor trends weekly to identify early warning signs or opportunities",
            "Focus on channels with higher revenue per customer for acquisition efforts"
        ]
        
        for i, step in enumerate(steps, 1):
            st.write(f"{i}. {step}")
    
    st.divider()
    
    st.info("💡 *Tip*: Use the filters in the sidebar to drill down into specific time periods or channels for deeper insights!")

# Footer
st.divider()
st.caption("📊 Performance Analytics Dashboard | Built with Streamlit & Python")
