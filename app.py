import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="NexaVerse Dashboard",
    page_icon="💎",
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

# Plotly Theme Colors
DARK_BG = '#1a1d24'
CHART_BG = '#1a1d24'
GRID_COLOR = '#2d3139'
TEXT_COLOR = '#ffffff'
SECONDARY_TEXT = '#a0aec0'

# Color Palette
COLORS = {
    'blue': '#4338ca',
    'purple': '#6366f1',
    'orange': '#f59e0b',
    'green': '#10b981',
    'red': '#ef4444',
    'violet': '#8b5cf6'
}

# Sidebar - Filters
with st.sidebar:
    st.markdown("## 💎 NexaVerse")
    st.divider()
    
    # Navigation
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "",
        ["📈 Overview", "👥 Customers", "📊 Reports", "⚙ Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Channel Filter
    st.markdown("### 📡 Channel Filter")
    channels = st.multiselect(
        "Select Channels",
        options=df['channel'].unique(),
        default=df['channel'].unique()
    )
    
    # Date Range Filter
    st.markdown("### 📅 Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.date_input(
        "Select Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    st.divider()
    
    if st.button("🚪 Log out", use_container_width=True):
        st.success("Logged out successfully!")

# Apply Filters
filtered_df = df[
    (df['channel'].isin(channels)) &
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date)
]

# Main Title
st.title("📊 Dashboard")
st.caption(f"Data period: {start_date} to {end_date}")
st.markdown("")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 KPIs & Overview",
    "🔍 Performance Analysis",
    "📉 Time Trends & Efficiency",
    "💡 Insights & Recommendations"
])

# TAB 1: KPIs & Overview
with tab1:
    # Calculate KPIs
    total_revenue = filtered_df['revenue'].sum()
    total_orders = filtered_df['orders'].sum()
    total_customers = filtered_df['customers'].sum()
    avg_conversion = filtered_df['conversion_rate'].mean()
    
    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Current MRR",
            value=f"${total_revenue/1000:.1f}k",
            delta=f"+{np.random.randint(5, 15)}% from last month"
        )
    
    with col2:
        st.metric(
            label="👥 Current Customers",
            value=f"{total_orders:,}",
            delta=f"+{np.random.randint(100, 500)} new"
        )
    
    with col3:
        st.metric(
            label="📊 Active Customers",
            value=f"{int(avg_conversion*100)}%",
            delta=f"{avg_conversion*100:.1f}% active rate"
        )
    
    with col4:
        st.metric(
            label="📉 Churn Rate",
            value=f"{np.random.randint(1, 5)}%",
            delta=f"-{np.random.uniform(0.5, 2):.1f}%",
            delta_color="inverse"
        )
    
    st.markdown("")
    
    # Charts Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Trend")
        
        # Revenue Trend Chart
        daily_trends = filtered_df.groupby('date').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily_trends['date'],
            y=daily_trends['revenue'],
            name='Revenue',
            marker_color=COLORS['blue'],
            opacity=0.8
        ))
        
        fig.add_trace(go.Bar(
            x=daily_trends['date'],
            y=daily_trends['orders']*50,
            name='Orders x50',
            marker_color=COLORS['purple'],
            opacity=0.9
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Sales")
        
        # Sales Donut Chart
        channel_revenue = filtered_df.groupby('channel')['revenue'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=channel_revenue['channel'],
            values=channel_revenue['revenue'],
            hole=.65,
            marker=dict(colors=[COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['red'], COLORS['violet']]),
            textposition='outside',
            textinfo='percent'
        )])
        
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR, size=10),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=-0.2, font=dict(size=9))
        )
        
        fig.add_annotation(
            text=f"${total_revenue/1000:.0f}k",
            x=0.5, y=0.5,
            font_size=24,
            font_color=TEXT_COLOR,
            font_weight='bold',
            showarrow=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("")
    
    # Transactions Section
    st.markdown("### 💳 Recent Transactions")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        transactions = pd.DataFrame({
            'Type': ['Dribbble', 'Behance', 'Upwork', 'Freelancer', 'Toptal'],
            'Amount': [np.random.randint(1000, 5000) for _ in range(5)],
            'Status': ['Completed'] * 5
        })
        
        for idx, row in transactions.iterrows():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"{row['Type']}")
            with col_b:
                st.write(f"${row['Amount']}")
        
        st.button("View All Transactions →", use_container_width=True)
    
    with col2:
        # Customer Demographics Map
        st.markdown("### 🗺 Customer Demographics")
        
        fig = go.Figure(data=go.Scattergeo(
            lon=[-100, 10, 50, 120, -50],
            lat=[40, 50, 30, 35, -20],
            mode='markers',
            marker=dict(
                size=[35, 45, 30, 40, 25],
                color=[COLORS['blue'], COLORS['purple'], COLORS['violet'], COLORS['orange'], COLORS['green']],
                line_width=0,
                opacity=0.8
            )
        ))
        
        fig.update_layout(
            geo=dict(
                bgcolor=CHART_BG,
                lakecolor=CHART_BG,
                landcolor='#2d3139',
                coastlinecolor='#3d4149',
                showland=True,
                showcountries=True,
                countrycolor='#3d4149',
                projection_type='natural earth'
            ),
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Performance Analysis
with tab2:
    st.markdown("## 🔍 Performance Analysis by Channel")
    
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
        }).background_gradient(cmap='Blues', subset=['Total Revenue']),
        use_container_width=True,
        height=250
    )
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue vs Orders")
        
        fig = px.scatter(
            performance_summary, 
            x='Total Orders', 
            y='Total Revenue',
            size='Total Customers', 
            color='Channel',
            color_discrete_sequence=[COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['red'], COLORS['violet']],
            size_max=50,
            text='Channel'
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Conversion Rate by Channel")
        
        fig = px.bar(
            performance_summary, 
            x='Channel', 
            y='Avg Conversion Rate',
            color='Channel',
            color_discrete_sequence=[COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['red'], COLORS['violet']],
            text='Avg Conversion Rate'
        )
        
        fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Channel Performance Details
    st.markdown("### 📊 Detailed Channel Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            performance_summary,
            x='Channel',
            y='Avg Order Value',
            color='Avg Order Value',
            color_continuous_scale='Purples',
            text='Avg Order Value'
        )
        
        fig.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        performance_summary['Revenue per Customer'] = performance_summary['Total Revenue'] / performance_summary['Total Customers']
        
        fig = px.bar(
            performance_summary,
            x='Channel',
            y='Revenue per Customer',
            color='Revenue per Customer',
            color_continuous_scale='Viridis',
            text='Revenue per Customer'
        )
        
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Time Trends & Efficiency
with tab3:
    st.markdown("## 📉 Time Trends Analysis")
    
    daily_trends = filtered_df.groupby('date').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'conversion_rate': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_trends['date'],
            y=daily_trends['revenue'],
            mode='lines',
            fill='tozeroy',
            line=dict(color=COLORS['blue'], width=2),
            fillcolor='rgba(67, 56, 202, 0.3)'
        ))
        
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=350,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Orders Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_trends['date'],
            y=daily_trends['orders'],
            mode='lines',
            fill='tozeroy',
            line=dict(color=COLORS['purple'], width=2),
            fillcolor='rgba(99, 102, 241, 0.3)'
        ))
        
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=350,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Efficiency Metrics
    st.markdown("## ⚡ Efficiency Analysis")
    
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
            color='channel',
            color_discrete_sequence=[COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['red'], COLORS['violet']],
            text='Revenue per Order'
        )
        
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(title='Channel', showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(title='Revenue per Order ($)', showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            efficiency_df,
            x='channel',
            y='Revenue per Customer',
            color='channel',
            color_discrete_sequence=[COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['red'], COLORS['violet']],
            text='Revenue per Customer'
        )
        
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(title='Channel', showgrid=False, color=SECONDARY_TEXT),
            yaxis=dict(title='Revenue per Customer ($)', showgrid=True, gridcolor=GRID_COLOR, color=SECONDARY_TEXT),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Weekly Heatmap
    st.markdown("### 📅 Weekly Performance Heatmap")
    
    temp_df = filtered_df.copy()
    temp_df['day_of_week'] = temp_df['date'].dt.day_name()
    temp_df['week'] = temp_df['date'].dt.isocalendar().week
    
    weekly_revenue = temp_df.pivot_table(
        values='revenue',
        index='day_of_week',
        columns='week',
        aggfunc='sum'
    )
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_revenue = weekly_revenue.reindex([d for d in day_order if d in weekly_revenue.index])
    
    fig = px.imshow(
        weekly_revenue,
        labels=dict(x="Week Number", y="Day of Week", color="Revenue ($)"),
        color_continuous_scale='Purples',
        aspect='auto'
    )
    
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_BG,
        font=dict(color=TEXT_COLOR),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: Insights & Recommendations
with tab4:
    st.markdown("## 💡 Insights & Recommendations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.expander("📊 Dashboard Information", expanded=True):
            st.markdown("""
            *Dashboard Overview*
            
            This analytics dashboard provides comprehensive insights into:
            - Real-time KPI monitoring
            - Channel performance analysis
            - Time-based trend analysis
            - Efficiency metrics and optimization opportunities
            
            *Data Sources*
            - Revenue data from all channels
            - Customer engagement metrics
            - Order and transaction history
            - Conversion rate tracking
            """)
    
    with col2:
        with st.expander("🎯 Key Features", expanded=True):
            st.markdown("""
            *Interactive Features*
            - Dynamic filtering by channel and date range
            - Multi-tab navigation for different views
            - Real-time data visualization
            - Comparative analysis tools
            
            *Export Options*
            - Download reports as CSV
            - Export charts as images
            - Share insights with team members
            """)
    
    st.divider()
    
    if len(performance_summary) > 0:
        st.markdown("## 🎯 Strategic Recommendations")
        
        top_channel = performance_summary.loc[performance_summary['Total Revenue'].idxmax(), 'Channel']
        worst_channel = performance_summary.loc[performance_summary['Total Revenue'].idxmin(), 'Channel']
        best_conversion = performance_summary.loc[performance_summary['Avg Conversion Rate'].idxmax(), 'Channel']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"🏆 Top Performer**")
            st.write(f"{top_channel}** is your highest revenue generator")
            st.caption("Consider allocating more marketing budget here")
        
        with col2:
            st.info(f"⭐ Best Conversion**")
            st.write(f"{best_conversion}** has the highest conversion rate")
            st.caption("Study and replicate winning strategies")
        
        with col3:
            st.warning(f"📈 Growth Opportunity**")
            st.write(f"{worst_channel}** needs optimization")
            st.caption("Analyze and improve this channel")
        
        st.divider()
        
        st.markdown("### 📋 Action Items")
        
        action_items = [
            "Conduct A/B testing on underperforming channels",
            "Increase investment in top-performing channels during peak periods",
            "Implement cross-channel learning from high-conversion channels",
            "Set up weekly monitoring for trend identification",
            "Focus acquisition efforts on channels with highest revenue per customer"
        ]
        
        for i, item in enumerate(action_items, 1):
            st.checkbox(f"{i}. {item}", key=f"action_{i}")
        
        st.divider()
        
        st.info("💡 *Pro Tip*: Use the sidebar filters to explore specific time periods and channels for deeper insights!")

# Footer
st.divider()
st.caption("📊 NexaVerse Analytics Dashboard | Built with Streamlit & Python")
