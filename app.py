# app.py - Part 1: Imports and Setup
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="NexaVerse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Styling
st.markdown("""
    <style>
    .main {background-color: #f3f4f6;}
    section[data-testid="stSidebar"] {background-color: #e5e7eb; padding-top: 1.5rem;}
    .sidebar-logo {font-weight: 800; font-size: 22px; color: #111827; margin-bottom: 2rem; 
                    display: flex; align-items: center; gap: 0.5rem; padding: 0 1rem;}
    .sidebar-logo-circle {width: 32px; height: 32px; border-radius: 999px; background-color: #111827;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .kpi-card {border-radius: 16px; padding: 20px; color: #f9fafb; margin-bottom: 10px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
    .kpi-label {font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; 
                 color: #e5e7eb; margin-bottom: 8px;}
    .kpi-value {font-size: 28px; font-weight: 700; margin: 8px 0;}
    .kpi-sub {font-size: 12px; color: #e5e7eb;}
    .kpi-navy {background-color: #111827;}
    .kpi-orange {background-color: #f59e0b;}
    .kpi-blue {background-color: #2563eb;}
    .kpi-indigo {background-color: #4f46e5;}
    
    .stTabs [data-baseweb="tab-list"] {gap: 8px; background-color: white; border-radius: 12px; padding: 8px;}
    .stTabs [data-baseweb="tab"] {height: 50px; background-color: transparent; border-radius: 8px; 
                                    color: #111827; font-weight: 600; font-size: 14px;}
    .stTabs [aria-selected="true"] {background-color: #111827; color: white;}
    
    .content-card {background-color: white; border-radius: 16px; padding: 20px; 
                   margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .card-title {font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px;}
    
    .dash-header {background-color: white; border-radius: 12px; padding: 20px 24px; 
                  margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .dash-title {font-size: 28px; font-weight: 700; color: #111827; margin: 0;}
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        df['date'] = pd.to_datetime(df['date'])
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        
        # Add calculated columns
        if 'marketing_spend' not in df.columns:
            df['marketing_spend'] = df['price'] * df['quantity'] * 0.2
        if 'clicks' not in df.columns:
            df['clicks'] = df['quantity'] * 50
        if 'cpc' not in df.columns:
            df['cpc'] = df['marketing_spend'] / df['clicks']
        if 'visits' not in df.columns:
            df['visits'] = df['quantity'] * 100
            
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

df = load_data()
if df is None:
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div class="sidebar-logo-circle"></div><span>NexaVerse</span></div>', 
                unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎯 Filters")
    
    all_channels = ['All Channels'] + sorted(df['marketing_channel'].unique().tolist())
    selected_channel = st.selectbox("Marketing Channel", options=all_channels, index=0)
    
    st.markdown("#### 📅 Month Range")
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = st.date_input("Select Date Range", value=(min_date, max_date), 
                                min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Info")
    st.info(f"""
    **Total Records:** {len(df):,}  
    **Date Range:** {min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}  
    **Channels:** {df['marketing_channel'].nunique()}
    """)
    st.markdown("---")
    st.markdown("**© 2024 NexaVerse Analytics**")

# Apply Filters
filtered_df = df.copy()
if selected_channel != 'All Channels':
    filtered_df = filtered_df[filtered_df['marketing_channel'] == selected_channel]
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['date'].dt.date >= start_date) & 
                              (filtered_df['date'].dt.date <= end_date)]

# Header
st.markdown('<div class="dash-header"><h1 class="dash-title">📊 E-Commerce Analytics Dashboard</h1></div>', 
            unsafe_allow_html=True)

# Calculate KPIs
total_revenue = filtered_df['net_revenue'].sum()
total_customers = filtered_df['customer_id'].nunique()
total_orders = len(filtered_df)
discount_sum = filtered_df['discount_amount'].sum()
total_roi = ((total_revenue - discount_sum) / discount_sum * 100) if discount_sum > 0 else 0

# Create Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 KPIs & Overview", "🎯 Channel Performance", "📅 Time Trends", 
    "⚡ Efficiency Analysis", "💡 About & Recommendations"
])

# ========== TAB 1: KPIs & Overview ==========
with tab1:
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="kpi-card kpi-navy"><div class="kpi-label">Total Revenue</div>'
                   f'<div class="kpi-value">${total_revenue:,.0f}</div>'
                   f'<div class="kpi-sub">Net revenue from all sales</div></div>', 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="kpi-card kpi-orange"><div class="kpi-label">Total Customers</div>'
                   f'<div class="kpi-value">{total_customers:,}</div>'
                   f'<div class="kpi-sub">Unique customers</div></div>', 
                   unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-label">Total Orders</div>'
                   f'<div class="kpi-value">{total_orders:,}</div>'
                   f'<div class="kpi-sub">Total transactions</div></div>', 
                   unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="kpi-card kpi-indigo"><div class="kpi-label">Average ROI</div>'
                   f'<div class="kpi-value">{total_roi:.1f}%</div>'
                   f'<div class="kpi-sub">Return on investment</div></div>', 
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📊 Revenue by Category")
        category_revenue = filtered_df.groupby('category')['net_revenue'].sum().sort_values(ascending=False)
        
        fig_category = px.bar(
            x=category_revenue.values, y=category_revenue.index, orientation='h',
            labels={'x': 'Revenue ($)', 'y': 'Category'},
            color=category_revenue.values,
            color_continuous_scale=['#3647F5', '#FF9F0D']
        )
        fig_category.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=400, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False), coloraxis_showscale=False
        )
        fig_category.update_traces(marker_line_width=0)
        st.plotly_chart(fig_category, use_container_width=True, key="cat_revenue")
    
    with col_right:
        st.markdown("### 🎯 Sales by Region")
        region_sales = filtered_df.groupby('region')['net_revenue'].sum()
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=region_sales.index, values=region_sales.values, hole=0.6,
            marker=dict(colors=['#111827', '#f59e0b', '#2563eb', '#4f46e5', '#10b981', '#ef4444'])
        )])
        fig_donut.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827', size=12),
            height=400, showlegend=True, margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig_donut, use_container_width=True, key="region_donut")
    
    # Summary Tables
    st.markdown("### 📋 KPIs Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        kpi_segment = filtered_df.groupby('customer_segment').agg({
            'net_revenue': 'sum', 'customer_id': 'nunique', 
            'quantity': 'sum', 'Average Order Value': 'mean'
        }).round(2)
        kpi_segment.columns = ['Revenue ($)', 'Customers', 'Orders', 'Avg Order Value ($)']
        st.markdown("**By Customer Segment**")
        st.dataframe(kpi_segment.sort_values('Revenue ($)', ascending=False), use_container_width=True)
    
    with col2:
        kpi_payment = filtered_df.groupby('payment_method').agg({
            'net_revenue': 'sum', 'customer_id': 'nunique', 'quantity': 'sum'
        }).round(2)
        kpi_payment.columns = ['Revenue ($)', 'Customers', 'Orders']
        st.markdown("**By Payment Method**")
        st.dataframe(kpi_payment.sort_values('Revenue ($)', ascending=False), use_container_width=True)

# ========== TAB 2: Channel Performance ==========
with tab2:
    st.markdown("### 🎯 Total Performance per Channel")
    
    channel_performance = filtered_df.groupby('marketing_channel').agg({
        'marketing_spend': 'sum', 'net_revenue': 'sum', 
        'customer_id': 'nunique', 'discount_amount': 'sum'
    }).round(2)
    channel_performance.columns = ['Total Spend', 'Total Revenue', 'Total Conversions', 'Total Discount']
    channel_performance['Average ROI'] = 0.0
    
    for idx in channel_performance.index:
        discount = channel_performance.loc[idx, 'Total Discount']
        revenue = channel_performance.loc[idx, 'Total Revenue']
        if discount > 0:
            channel_performance.loc[idx, 'Average ROI'] = ((revenue - discount) / discount * 100)
    
    channel_performance = channel_performance.sort_values('Total Revenue', ascending=False)
    st.dataframe(channel_performance, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Total Revenue by Channel")
        fig_revenue = px.bar(
            channel_performance.reset_index().sort_values('Total Revenue', ascending=True),
            x='Total Revenue', y='marketing_channel', orientation='h',
            color='Total Revenue', color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'marketing_channel': 'Channel', 'Total Revenue': 'Revenue ($)'}
        )
        fig_revenue.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=500, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False), coloraxis_showscale=False
        )
        fig_revenue.update_traces(marker_line_width=0)
        st.plotly_chart(fig_revenue, use_container_width=True, key="channel_rev")
    
    with col2:
        st.markdown("### 👥 Total Conversions by Channel")
        fig_conversions = px.bar(
            channel_performance.reset_index().sort_values('Total Conversions', ascending=True),
            x='Total Conversions', y='marketing_channel', orientation='h',
            color='Total Conversions', color_continuous_scale=['#10b981', '#f59e0b'],
            labels={'marketing_channel': 'Channel', 'Total Conversions': 'Conversions'}
        )
        fig_conversions.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=500, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False), coloraxis_showscale=False
        )
        fig_conversions.update_traces(marker_line_width=0)
        st.plotly_chart(fig_conversions, use_container_width=True, key="channel_conv")
    
    # ROI Chart
    st.markdown("### 📈 ROI Comparison")
    fig_roi = px.bar(
        channel_performance.reset_index().sort_values('Average ROI', ascending=False),
        x='marketing_channel', y='Average ROI',
        color='Average ROI', color_continuous_scale=['#ef4444', '#10b981'],
        labels={'marketing_channel': 'Channel', 'Average ROI': 'ROI (%)'}
    )
    fig_roi.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
        showlegend=False, height=400, margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb'), coloraxis_showscale=False
    )
    fig_roi.update_traces(marker_line_width=0)
    st.plotly_chart(fig_roi, use_container_width=True, key="roi_chart")

# ========== TAB 3: Time Trends ==========
with tab3:
    monthly_data = filtered_df.groupby(['month_year', 'marketing_channel']).agg({
        'net_revenue': 'sum', 'customer_id': 'nunique'
    }).reset_index()
    monthly_data.columns = ['month', 'channel', 'revenue', 'conversions']
    
    monthly_total = filtered_df.groupby('month_year').agg({
        'net_revenue': 'sum', 'customer_id': 'nunique'
    }).reset_index()
    monthly_total.columns = ['month', 'total_revenue', 'total_conversions']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💵 Monthly Revenue Trend")
        fig_revenue_trend = px.line(
            monthly_total, x='month', y='total_revenue', markers=True,
            labels={'month': 'Month', 'total_revenue': 'Revenue ($)'}
        )
        fig_revenue_trend.update_traces(
            line=dict(color='#3647F5', width=3),
            marker=dict(size=8, color='#FF9F0D')
        )
        fig_revenue_trend.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=350, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig_revenue_trend, use_container_width=True, key="monthly_rev")
    
    with col2:
        st.markdown("### 👥 Monthly Conversions Trend")
        fig_conv_trend = px.line(
            monthly_total, x='month', y='total_conversions', markers=True,
            labels={'month': 'Month', 'total_conversions': 'Conversions'}
        )
        fig_conv_trend.update_traces(
            line=dict(color='#FF9F0D', width=3),
            marker=dict(size=8, color='#3647F5')
        )
        fig_conv_trend.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=350, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig_conv_trend, use_container_width=True, key="monthly_conv")
    
    st.markdown("### 📊 Monthly Revenue by Channel")
    fig_channel_time = px.line(
        monthly_data, x='month', y='revenue', color='channel', markers=True,
        labels={'month': 'Month', 'revenue': 'Revenue ($)', 'channel': 'Channel'}
    )
    fig_channel_time.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
        height=450, margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_channel_time, use_container_width=True, key="channel_time_rev")
    
    if len(monthly_total) > 0:
        peak_month = monthly_total.loc[monthly_total['total_revenue'].idxmax(), 'month']
        peak_value = monthly_total['total_revenue'].max()
        low_month = monthly_total.loc[monthly_total['total_revenue'].idxmin(), 'month']
        low_value = monthly_total['total_revenue'].min()
        growth = ((peak_value - low_value) / low_value * 100) if low_value > 0 else 0
        
        st.success(f"""
        **Peak:** ${peak_value:,.0f} in {peak_month} | **Low:** ${low_value:,.0f} in {low_month} | **Growth:** {growth:,.1f}%
        """)

# ========== TAB 4: Efficiency ==========
with tab4:
    cpc_by_channel = filtered_df.groupby('marketing_channel').agg({
        'cpc': 'mean', 'marketing_spend': 'sum', 'clicks': 'sum'
    }).reset_index()
    cpc_by_channel.columns = ['Channel', 'Avg_CPC', 'Total_Spend', 'Total_Clicks']
    cpc_by_channel = cpc_by_channel.sort_values('Avg_CPC')
    
    conversion_by_channel = filtered_df.groupby('marketing_channel').agg({
        'customer_id': 'nunique', 'visits': 'sum'
    }).reset_index()
    conversion_by_channel['conversion_rate'] = (
        conversion_by_channel['customer_id'] / conversion_by_channel['visits'] * 100
    ).round(3)
    conversion_by_channel.columns = ['Channel', 'Conversions', 'Total_Visits', 'Conversion_Rate']
    conversion_by_channel = conversion_by_channel.sort_values('Conversion_Rate', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💲 CPC by Channel")
        fig_cpc = px.bar(
            cpc_by_channel.sort_values('Avg_CPC'), x='Avg_CPC', y='Channel', orientation='h',
            color='Avg_CPC', color_continuous_scale=['#10b981', '#3647F5', '#FF9F0D'],
            labels={'Avg_CPC': 'Average CPC ($)', 'Channel': 'Marketing Channel'}
        )
        fig_cpc.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=450, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False), coloraxis_showscale=False
        )
        fig_cpc.update_traces(marker_line_width=0)
        st.plotly_chart(fig_cpc, use_container_width=True, key="cpc_chart")
    
    with col2:
        st.markdown("### 📊 Conversion Rate by Channel")
        fig_conv_rate = px.bar(
            conversion_by_channel.sort_values('Conversion_Rate', ascending=False),
            x='Channel', y='Conversion_Rate',
            color='Conversion_Rate', color_continuous_scale=['#3647F5', '#10b981'],
            labels={'Conversion_Rate': 'Conversion Rate (%)', 'Channel': 'Marketing Channel'}
        )
        fig_conv_rate.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#111827'),
            showlegend=False, height=450, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb'), coloraxis_showscale=False
        )
        fig_conv_rate.update_traces(marker_line_width=0)
        st.plotly_chart(fig_conv_rate, use_container_width=True, key="conv_rate_chart")

# ========== TAB 5: About ==========
with tab5:
    st.markdown("### 📊 About This Dashboard")
    st.markdown("""
    Dashboard تحليل شامل للأداء التسويقي والمبيعات، يوفر رؤى احترافية حول:
    - 📈 المؤشرات الرئيسية (KPIs)
    - 🎯 أداء القنوات التسويقية
    - 📅 الاتجاهات الزمنية
    - ⚡ تحليل الكفاءة والتكلفة
    
    **Team:** Zaid Tarek, Mayar, Ahmed, Toqa | **© 2024 NexaVerse Analytics**
    """)
    
    if len(channel_performance) > 0:
        best_roi_channel = channel_performance['Average ROI'].idxmax()
        best_roi_value = channel_performance['Average ROI'].max()
        st.success(f"🏆 **Best ROI:** {best_roi_channel} - {best_roi_value:.2f}%")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #6b7280; font-size: 14px; padding: 20px;">'
           '<strong>NexaVerse Analytics Dashboard</strong> | Built with ❤️ using Streamlit & Plotly | © 2024</div>', 
           unsafe_allow_html=True)
