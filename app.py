import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.io as pio

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
# COLORS CONFIGURATION - احترافي
# ═══════════════════════════════════════════════════════════════════════════

COLORS = {
    'primary': '#3647F5',      # أزرق
    'dark': '#1B2346',         # أسود مائل
    'accent': '#FF9F0D',       # برتقالي
    'bg_dark': '#040D2F',      # خلفية مظلمة
    'light': '#D9D9D9',        # رمادي فاتح
    'success': '#00C851',      # أخضر
    'warning': '#ffbb33',      # أصفر
    'danger': '#ff4444'        # أحمر
}

# Custom CSS Styling
st.markdown(f"""
<style>
    /* Main Background */
    .main {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['light']};
    }}
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {{
        background-color: {COLORS['dark']};
    }}
    
    /* Metrics Cards */
    .stMetric {{
        background-color: {COLORS['dark']};
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {COLORS['accent']};
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['accent']};
        font-weight: 600;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {{
        background-color: {COLORS['dark']};
        color: {COLORS['light']};
        border-radius: 8px;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['accent']};
    }}
    
    /* Selectbox and Multiselect */
    .stSelectbox, .stMultiSelect {{
        color: {COLORS['light']};
    }}
    
    /* Info/Success/Warning boxes */
    .stInfo {{
        background-color: rgba(54, 71, 245, 0.1);
        border: 1px solid {COLORS['primary']};
    }}
    
    .stSuccess {{
        background-color: rgba(255, 159, 13, 0.1);
        border: 1px solid {COLORS['accent']};
    }}
    
    /* Dataframes */
    .dataframe {{
        background-color: {COLORS['dark']} !important;
        color: {COLORS['light']} !important;
    }}
    
    /* Plotly chart styling */
    .js-plotly-plot .plotly {{
        background-color: {COLORS['bg_dark']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LOAD & PROCESS DATA
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_and_process_data():
    df = pd.read_csv('cleaned_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    df['month_name'] = df['date'].dt.month_name()
    
    # Calculate all KPIs from notebook
    df['Average Order Value'] = df['final_amount'] / df['quantity']
    df['revenue_per_customer'] = df['final_amount'] / df['customer_id'].nunique()
    df['discount_amount'] = df['price'] * df['discount_percent'] / 100
    df['gross_revenue'] = df['price'] * df['quantity']
    df['net_revenue'] = df['final_amount']
    df['roi'] = (df['net_revenue'] - df['discount_amount']) / df['discount_amount']
    
    # Conversion rate per customer
    orders_per_customer = df.groupby('customer_id').size()
    df['conversion_rate'] = df['customer_id'].map(orders_per_customer)
    
    return df

df = load_and_process_data()

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS FOR KPI CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════

def calculate_all_kpis(filtered_df):
    """Calculate all KPIs from the notebook"""
    
    # KPIs by category
    kpi_category = filtered_df.groupby('category').agg({
        'gross_revenue': 'sum',
        'net_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    })
    kpi_category['avg_order_value'] = kpi_category['net_revenue'] / kpi_category['quantity']
    kpi_category['roi'] = (kpi_category['net_revenue'] - kpi_category['discount_amount']) / kpi_category['discount_amount']
    
    # KPIs by marketing campaign
    kpi_campaign = filtered_df.groupby('marketing_campaign').agg({
        'net_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    })
    kpi_campaign['revenue_per_customer'] = kpi_campaign['net_revenue'] / kpi_campaign['customer_id']
    kpi_campaign['roi'] = (kpi_campaign['net_revenue'] - kpi_campaign['discount_amount']) / kpi_campaign['discount_amount']
    
    # KPIs by marketing channel
    kpi_channel = filtered_df.groupby('marketing_channel').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    })
    kpi_channel['avg_order_value'] = kpi_channel['net_revenue'] / kpi_channel['quantity']
    kpi_channel['revenue_per_customer'] = kpi_channel['net_revenue'] / kpi_channel['customer_id']
    kpi_channel['roi'] = (kpi_channel['net_revenue'] - kpi_channel['discount_amount']) / kpi_channel['discount_amount']
    
    # KPIs by customer segment
    kpi_segment = filtered_df.groupby('customer_segment').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique',
        'customer_lifetime_value': 'mean',
        'retention_score': 'mean'
    })
    kpi_segment['avg_order_value'] = kpi_segment['net_revenue'] / kpi_segment['quantity']
    kpi_segment['revenue_per_customer'] = kpi_segment['net_revenue'] / kpi_segment['customer_id']
    kpi_segment['roi'] = (kpi_segment['net_revenue'] - kpi_segment['discount_amount']) / kpi_segment['discount_amount']
    
    # KPIs by region
    kpi_region = filtered_df.groupby('region').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    })
    kpi_region['avg_order_value'] = kpi_region['net_revenue'] / kpi_region['quantity']
    kpi_region['revenue_per_customer'] = kpi_region['net_revenue'] / kpi_region['customer_id']
    kpi_region['roi'] = (kpi_region['net_revenue'] - kpi_region['discount_amount']) / kpi_region['discount_amount']
    
    # KPIs by month
    kpi_month = filtered_df.groupby('month').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    })
    kpi_month['avg_order_value'] = kpi_month['net_revenue'] / kpi_month['quantity']
    kpi_month['roi'] = (kpi_month['net_revenue'] - kpi_month['discount_amount']) / kpi_month['discount_amount']
    
    # KPIs by quarter
    kpi_quarter = filtered_df.groupby('quarter').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    })
    kpi_quarter['avg_order_value'] = kpi_quarter['net_revenue'] / kpi_quarter['quantity']
    kpi_quarter['roi'] = (kpi_quarter['net_revenue'] - kpi_quarter['discount_amount']) / kpi_quarter['discount_amount']
    
    # KPIs by season
    kpi_season = filtered_df.groupby('season').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    })
    kpi_season['avg_order_value'] = kpi_season['net_revenue'] / kpi_season['quantity']
    kpi_season['roi'] = (kpi_season['net_revenue'] - kpi_season['discount_amount']) / kpi_season['discount_amount']
    
    # Channel performance analysis
    channel_perf = filtered_df.groupby('marketing_channel').agg({
        'discount_percent': 'sum',
        'final_amount': 'sum',
        'customer_id': 'nunique',
    })
    channel_perf['total_spend'] = channel_perf['discount_percent']
    channel_perf['total_revenue'] = channel_perf['final_amount']
    channel_perf['total_conversions'] = channel_perf['customer_id']
    channel_perf['avg_roi'] = (
        (channel_perf['total_revenue'] - channel_perf['total_spend'])
        / channel_perf['total_spend']
    )
    
    return {
        'kpi_category': kpi_category,
        'kpi_campaign': kpi_campaign,
        'kpi_channel': kpi_channel,
        'kpi_segment': kpi_segment,
        'kpi_region': kpi_region,
        'kpi_month': kpi_month,
        'kpi_quarter': kpi_quarter,
        'kpi_season': kpi_season,
        'channel_perf': channel_perf
    }

# ═══════════════════════════════════════════════════════════════════════════
# LOGO & HEADER
# ═══════════════════════════════════════════════════════════════════════════

col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown(f'<h1 style="color: {COLORS["accent"]};font-size: 2em;">📊</h1>', unsafe_allow_html=True)
with col_title:
    st.title("E-Commerce Analytics Dashboard", anchor="main")
    st.markdown(f"<p style='color: {COLORS['light']}; margin-top: -20px;'>Data-Driven Business Intelligence | All Charts from Notebook</p>", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - ADVANCED FILTERS
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">🎛️ FILTERS</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Date Range Filter
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        start_date = st.date_input(
            "📅 Start Date",
            value=df['date'].min().date(),
            min_value=df['date'].min().date(),
            max_value=df['date'].max().date()
        )
    
    with col_date2:
        end_date = st.date_input(
            "📅 End Date",
            value=df['date'].max().date(),
            min_value=df['date'].min().date(),
            max_value=df['date'].max().date()
        )
    
    st.markdown("---")
    
    # Channel Filter
    selected_channels = st.multiselect(
        "📢 Marketing Channels",
        options=sorted(df['marketing_channel'].unique()),
        default=sorted(df['marketing_channel'].unique()),
        help="Select one or more channels"
    )
    
    # Campaign Filter
    selected_campaigns = st.multiselect(
        "🎪 Marketing Campaigns",
        options=sorted(df['marketing_campaign'].unique()),
        default=sorted(df['marketing_campaign'].unique()),
        help="Select one or more campaigns"
    )
    
    # Segment Filter
    selected_segments = st.multiselect(
        "👥 Customer Segments",
        options=sorted(df['customer_segment'].unique()),
        default=sorted(df['customer_segment'].unique()),
        help="Select one or more segments"
    )
    
    # Region Filter
    selected_regions = st.multiselect(
        "🗺️ Regions",
        options=sorted(df['region'].unique()),
        default=sorted(df['region'].unique()),
        help="Select one or more regions"
    )
    
    # Category Filter
    selected_categories = st.multiselect(
        "📦 Product Categories",
        options=sorted(df['category'].unique()),
        default=sorted(df['category'].unique()),
        help="Select one or more categories"
    )
    
    st.markdown("---")
    
    # View Options
    st.markdown(f'<h4 style="color: {COLORS["accent"]};">📊 View Options</h4>', unsafe_allow_html=True)
    show_tables = st.checkbox("Show Data Tables", value=False)
    show_details = st.checkbox("Show Detailed Calculations", value=False)
    
    # Apply Filters Button
    if st.button("🔄 Apply Filters", use_container_width=True):
        st.session_state.filters_applied = True
        st.rerun()

# Apply Filters
filtered_df = df[
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date) &
    (df['marketing_channel'].isin(selected_channels)) &
    (df['marketing_campaign'].isin(selected_campaigns)) &
    (df['customer_segment'].isin(selected_segments)) &
    (df['region'].isin(selected_regions)) &
    (df['category'].isin(selected_categories))
].reset_index(drop=True)

# Calculate all KPIs
kpis = calculate_all_kpis(filtered_df)

# Display filter info
st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='color: {COLORS['light']}; font-size: 12px;'>📊 Records: <strong>{len(filtered_df):,}</strong></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: {COLORS['light']}; font-size: 12px;'>✨ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# TABS NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🎯 Campaign Analysis",
    "👥 Customer Insights",
    "📈 Trends & Seasonality",
    "💰 Financial Metrics",
    "📋 All Tables"
])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # KPI ROW 1
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = filtered_df['net_revenue'].sum()
    total_customers = filtered_df['customer_id'].nunique()
    total_orders = len(filtered_df)
    avg_order_value = filtered_df['final_amount'].mean()
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"+${total_revenue * 0.12:,.0f}" if total_revenue > 0 else None
        )
    
    with col2:
        st.metric(
            label="👥 Total Customers",
            value=f"{total_customers:,}",
            delta=f"+{int(total_customers * 0.08)}" if total_customers > 0 else None
        )
    
    with col3:
        st.metric(
            label="📦 Total Orders",
            value=f"{total_orders:,}"
        )
    
    with col4:
        st.metric(
            label="📊 Avg Order Value",
            value=f"${avg_order_value:,.2f}"
        )
    
    # KPI ROW 2
    col5, col6, col7, col8 = st.columns(4)
    
    conversion_rate = (filtered_df['customer_id'].nunique() / total_orders * 100) if total_orders > 0 else 0
    return_rate = (filtered_df['returned'].sum() / total_orders * 100) if total_orders > 0 else 0
    avg_satisfaction = filtered_df['satisfaction_rating'].mean()
    avg_roi = filtered_df['roi'].replace([np.inf, -np.inf], np.nan).mean()
    
    with col5:
        st.metric(label="📊 Conversion Rate", value=f"{conversion_rate:.2f}%")
    
    with col6:
        st.metric(label="🔄 Return Rate", value=f"{return_rate:.2f}%")
    
    with col7:
        st.metric(label="⭐ Avg Satisfaction", value=f"{avg_satisfaction:.2f}/5")
    
    with col8:
        st.metric(label="📈 Avg ROI", value=f"{avg_roi:.2f}x")
    
    st.markdown("---")
    
    # Revenue Overview Charts
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">💰 Revenue Overview</h3>', unsafe_allow_html=True)
    
    col_rev1, col_rev2 = st.columns(2)
    
    with col_rev1:
        # Channel Performance Chart from notebook
        fig_channel = px.bar(
            kpis['channel_perf'].reset_index(),
            x='marketing_channel',
            y='total_revenue',
            title='💰 Revenue by Marketing Channel',
            color='total_revenue',
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'marketing_channel': 'Channel', 'total_revenue': 'Revenue ($)'},
            text_auto='$.0f'
        )
        fig_channel.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col_rev2:
        # Customer Distribution by Channel from notebook
        fig_channel_pie = px.pie(
            values=kpis['channel_perf']['total_conversions'],
            names=kpis['channel_perf'].index,
            title='👥 Customer Distribution by Channel',
            color_discrete_sequence=['#3647F5', '#FF9F0D', '#1B2346', '#D9D9D9']
        )
        fig_channel_pie.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400
        )
        st.plotly_chart(fig_channel_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Campaign & Category Performance
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">🎪 Campaign & Category Performance</h3>', unsafe_allow_html=True)
    
    col_camp, col_cat = st.columns(2)
    
    with col_camp:
        # Revenue by Campaign from notebook
        campaign_stats = kpis['kpi_campaign']['net_revenue'].sort_values(ascending=False)
        fig_campaign = px.bar(
            x=campaign_stats.index,
            y=campaign_stats.values,
            title='🎯 Revenue by Marketing Campaign',
            color=campaign_stats.values,
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'x': 'Campaign', 'y': 'Revenue ($)'},
            text_auto='$.0f'
        )
        fig_campaign.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_campaign, use_container_width=True)
    
    with col_cat:
        # Top Categories from notebook
        category_stats = kpis['kpi_category']['net_revenue'].sort_values(ascending=False).head(10)
        fig_category = px.bar(
            x=category_stats.values,
            y=category_stats.index,
            orientation='h',
            title='📦 Top 10 Product Categories by Revenue',
            color=category_stats.values,
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'x': 'Revenue ($)', 'y': 'Category'}
        )
        fig_category.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_category, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: CAMPAIGN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">🎯 Marketing Campaign Analysis</h2>', unsafe_allow_html=True)
    
    # Campaign Effectiveness Comparison
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📊 Campaign Effectiveness</h3>', unsafe_allow_html=True)
    
    fig_campaign_effect = go.Figure(data=[
        go.Bar(name='💰 Revenue', 
               x=kpis['kpi_campaign'].index, 
               y=kpis['kpi_campaign']['net_revenue'],
               marker_color=COLORS['primary']),
        go.Bar(name='👥 Customers', 
               x=kpis['kpi_campaign'].index, 
               y=kpis['kpi_campaign']['customer_id'],
               marker_color=COLORS['accent'])
    ])
    
    fig_campaign_effect.update_layout(
        title='Campaign Effectiveness: Revenue vs Customers Acquired',
        xaxis_title='Marketing Campaign',
        yaxis_title='Value',
        barmode='group',
        plot_bgcolor=COLORS['bg_dark'],
        paper_bgcolor=COLORS['bg_dark'],
        font=dict(color=COLORS['light']),
        height=500,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_campaign_effect, use_container_width=True)
    
    st.markdown("---")
    
    # Campaign ROI Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📈 Campaign ROI Analysis</h3>', unsafe_allow_html=True)
    
    col_roi1, col_roi2 = st.columns(2)
    
    with col_roi1:
        # Campaign ROI Bar Chart
        fig_campaign_roi = px.bar(
            kpis['kpi_campaign'].reset_index(),
            x='marketing_campaign',
            y='roi',
            title='📈 ROI by Campaign',
            color='roi',
            color_continuous_scale=['#FF4444', '#FF9F0D', '#00C851'],
            labels={'marketing_campaign': 'Campaign', 'roi': 'ROI'},
            text_auto='.2f'
        )
        fig_campaign_roi.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_campaign_roi, use_container_width=True)
    
    with col_roi2:
        # Revenue per Customer by Campaign
        fig_rev_per_cust = px.bar(
            kpis['kpi_campaign'].reset_index(),
            x='marketing_campaign',
            y='revenue_per_customer',
            title='💰 Revenue per Customer by Campaign',
            color='revenue_per_customer',
            color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'marketing_campaign': 'Campaign', 'revenue_per_customer': 'Revenue per Customer ($)'},
            text_auto='$.0f'
        )
        fig_rev_per_cust.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_rev_per_cust, use_container_width=True)
    
    st.markdown("---")
    
    # Campaign Metrics Table
    if show_tables:
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">📋 Campaign Metrics Details</h3>', unsafe_allow_html=True)
        
        campaign_table = kpis['kpi_campaign'][['net_revenue', 'customer_id', 'quantity', 'revenue_per_customer', 'roi']].round(2)
        st.dataframe(campaign_table, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: CUSTOMER INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">👥 Customer Insights & Segmentation</h2>', unsafe_allow_html=True)
    
    # Customer Segment Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">💎 Customer Segment Analysis</h3>', unsafe_allow_html=True)
    
    col_seg1, col_seg2 = st.columns(2)
    
    with col_seg1:
        # Revenue by Customer Segment Pie Chart
        fig_segment_pie = px.pie(
            values=kpis['kpi_segment']['net_revenue'],
            names=kpis['kpi_segment'].index,
            title='💎 Revenue Distribution by Customer Segment',
            color_discrete_sequence=['#3647F5', '#FF9F0D', '#1B2346', '#D9D9D9', '#00C851']
        )
        fig_segment_pie.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400
        )
        st.plotly_chart(fig_segment_pie, use_container_width=True)
    
    with col_seg2:
        # Customer Lifetime Value by Segment
        fig_clv_segment = go.Figure(data=[
            go.Bar(name='💰 Avg CLV', 
                   x=kpis['kpi_segment'].index, 
                   y=kpis['kpi_segment']['customer_lifetime_value'],
                   marker_color=COLORS['primary']),
            go.Bar(name='⭐ Retention Score', 
                   x=kpis['kpi_segment'].index, 
                   y=kpis['kpi_segment']['retention_score'],
                   marker_color=COLORS['accent'])
        ])
        
        fig_clv_segment.update_layout(
            title='Customer Lifetime Value & Retention by Segment',
            xaxis_title='Customer Segment',
            yaxis_title='Value',
            barmode='group',
            plot_bgcolor=COLORS['bg_dark'],
            paper_bgcolor=COLORS['bg_dark'],
            font=dict(color=COLORS['light']),
            height=400
        )
        st.plotly_chart(fig_clv_segment, use_container_width=True)
    
    st.markdown("---")
    
    # Regional Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">🗺️ Regional Performance</h3>', unsafe_allow_html=True)
    
    col_reg1, col_reg2 = st.columns(2)
    
    with col_reg1:
        # Revenue by Region
        fig_region = px.bar(
            kpis['kpi_region'].reset_index(),
            x='region',
            y='net_revenue',
            title='💰 Revenue by Region',
            color='net_revenue',
            color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'region': 'Region', 'net_revenue': 'Revenue ($)'},
            text_auto='$.0f'
        )
        fig_region.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col_reg2:
        # ROI by Region
        fig_region_roi = px.bar(
            kpis['kpi_region'].reset_index(),
            x='region',
            y='roi',
            title='📈 ROI by Region',
            color='roi',
            color_continuous_scale=['#FF4444', '#FF9F0D', '#00C851'],
            labels={'region': 'Region', 'roi': 'ROI'},
            text_auto='.2f'
        )
        fig_region_roi.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_region_roi, use_container_width=True)
    
    st.markdown("---")
    
    # Customer Metrics Table
    if show_tables:
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">📋 Customer Segment Metrics</h3>', unsafe_allow_html=True)
        
        segment_table = kpis['kpi_segment'][['net_revenue', 'customer_id', 'avg_order_value', 'revenue_per_customer', 'roi', 'customer_lifetime_value', 'retention_score']].round(2)
        st.dataframe(segment_table, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: TRENDS & SEASONALITY
# ═══════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">📈 Trends & Seasonality Analysis</h2>', unsafe_allow_html=True)
    
    # Monthly Trends
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📅 Monthly Performance Trends</h3>', unsafe_allow_html=True)
    
    # Prepare monthly data
    monthly_data = kpis['kpi_month'].reset_index()
    monthly_data['month_name'] = pd.to_datetime(monthly_data['month'], format='%m').dt.month_name()
    
    col_month1, col_month2 = st.columns(2)
    
    with col_month1:
        # Monthly Revenue Trend
        fig_monthly_rev = px.line(
            monthly_data,
            x='month_name',
            y='net_revenue',
            markers=True,
            title='💰 Monthly Revenue Trend',
            labels={'month_name': 'Month', 'net_revenue': 'Revenue ($)'}
        )
        fig_monthly_rev.update_traces(
            line=dict(color=COLORS['accent'], width=3),
            marker=dict(size=10, color=COLORS['primary'], symbol='circle')
        )
        fig_monthly_rev.update_layout(
            plot_bgcolor=COLORS['bg_dark'],
            paper_bgcolor=COLORS['bg_dark'],
            font=dict(color=COLORS['light']),
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_monthly_rev, use_container_width=True)
    
    with col_month2:
        # Monthly Avg Order Value Trend
        fig_monthly_aov = px.line(
            monthly_data,
            x='month_name',
            y='avg_order_value',
            markers=True,
            title='📊 Monthly Average Order Value Trend',
            labels={'month_name': 'Month', 'avg_order_value': 'Avg Order Value ($)'}
        )
        fig_monthly_aov.update_traces(
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=10, color=COLORS['accent'], symbol='diamond')
        )
        fig_monthly_aov.update_layout(
            plot_bgcolor=COLORS['bg_dark'],
            paper_bgcolor=COLORS['bg_dark'],
            font=dict(color=COLORS['light']),
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_monthly_aov, use_container_width=True)
    
    st.markdown("---")
    
    # Seasonal Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">🌡️ Seasonal Performance Analysis</h3>', unsafe_allow_html=True)
    
    col_season1, col_season2 = st.columns(2)
    
    with col_season1:
        # Revenue by Season
        fig_season = px.bar(
            kpis['kpi_season'].reset_index(),
            x='season',
            y='net_revenue',
            title='🌡️ Revenue by Season',
            color='net_revenue',
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'season': 'Season', 'net_revenue': 'Revenue ($)'},
            text_auto='$.0f'
        )
        fig_season.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_season, use_container_width=True)
    
    with col_season2:
        # ROI by Season
        fig_season_roi = px.bar(
            kpis['kpi_season'].reset_index(),
            x='season',
            y='roi',
            title='📈 ROI by Season',
            color='roi',
            color_continuous_scale=['#FF4444', '#FF9F0D', '#00C851'],
            labels={'season': 'Season', 'roi': 'ROI'},
            text_auto='.2f'
        )
        fig_season_roi.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_season_roi, use_container_width=True)
    
    st.markdown("---")
    
    # Quarterly Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📊 Quarterly Performance</h3>', unsafe_allow_html=True)
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        # Quarterly Revenue
        fig_quarter = px.bar(
            kpis['kpi_quarter'].reset_index(),
            x='quarter',
            y='net_revenue',
            title='📊 Quarterly Revenue',
            color='net_revenue',
            color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'quarter': 'Quarter', 'net_revenue': 'Revenue ($)'},
            text_auto='$.0f'
        )
        fig_quarter.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_quarter, use_container_width=True)
    
    with col_q2:
        # Quarterly ROI
        fig_quarter_roi = px.line(
            kpis['kpi_quarter'].reset_index(),
            x='quarter',
            y='roi',
            markers=True,
            title='📈 Quarterly ROI Trend',
            labels={'quarter': 'Quarter', 'roi': 'ROI'}
        )
        fig_quarter_roi.update_traces(
            line=dict(color=COLORS['accent'], width=3),
            marker=dict(size=10, color=COLORS['primary'], symbol='square')
        )
        fig_quarter_roi.update_layout(
            plot_bgcolor=COLORS['bg_dark'],
            paper_bgcolor=COLORS['bg_dark'],
            font=dict(color=COLORS['light']),
            height=400
        )
        st.plotly_chart(fig_quarter_roi, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5: FINANCIAL METRICS
# ═══════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">💰 Financial Metrics & ROI Analysis</h2>', unsafe_allow_html=True)
    
    # ROI Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📈 ROI Analysis by Channel</h3>', unsafe_allow_html=True)
    
    roi_by_channel = kpis['kpi_channel'][['roi']].sort_values('roi', ascending=False)
    
    fig_roi_channel = px.bar(
        roi_by_channel.reset_index(),
        x='marketing_channel',
        y='roi',
        title='🎯 Average ROI by Channel',
        color='roi',
        color_continuous_scale=['#FF4444', '#FF9F0D', '#00C851'],
        labels={'marketing_channel': 'Channel', 'roi': 'ROI'},
        text_auto='.2f'
    )
    fig_roi_channel.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font=dict(color='#D9D9D9'),
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_roi_channel, use_container_width=True)
    
    st.markdown("---")
    
    # Order Value vs ROI Analysis
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">📊 Order Value vs ROI Analysis</h3>', unsafe_allow_html=True)
    
    fig_order_roi = px.scatter(
        kpis['kpi_category'].reset_index(),
        x='avg_order_value',
        y='roi',
        size='quantity',
        color='category',
        hover_name='category',
        title='📦 Order Value vs ROI by Category',
        labels={'avg_order_value': 'Average Order Value ($)', 
                'roi': 'ROI', 
                'quantity': 'Total Quantity'}
    )
    fig_order_roi.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font=dict(color='#D9D9D9'),
        height=500,
        showlegend=True
    )
    st.plotly_chart(fig_order_roi, use_container_width=True)
    
    st.markdown("---")
    
    # Channel Efficiency Metrics
    st.markdown(f'<h3 style="color: {COLORS["accent"]};">⚡ Channel Efficiency Metrics</h3>', unsafe_allow_html=True)
    
    efficiency_metrics = kpis['kpi_channel'][['avg_order_value', 'revenue_per_customer', 'roi']].round(2)
    
    # Create a grouped bar chart for channel efficiency
    fig_efficiency = go.Figure()
    
    fig_efficiency.add_trace(go.Bar(
        name='Avg Order Value',
        x=efficiency_metrics.index,
        y=efficiency_metrics['avg_order_value'],
        marker_color=COLORS['primary']
    ))
    
    fig_efficiency.add_trace(go.Bar(
        name='Revenue per Customer',
        x=efficiency_metrics.index,
        y=efficiency_metrics['revenue_per_customer'],
        marker_color=COLORS['accent']
    ))
    
    fig_efficiency.add_trace(go.Bar(
        name='ROI',
        x=efficiency_metrics.index,
        y=efficiency_metrics['roi'],
        marker_color=COLORS['success']
    ))
    
    fig_efficiency.update_layout(
        title='Channel Efficiency Metrics Comparison',
        xaxis_title='Marketing Channel',
        yaxis_title='Value',
        barmode='group',
        plot_bgcolor=COLORS['bg_dark'],
        paper_bgcolor=COLORS['bg_dark'],
        font=dict(color=COLORS['light']),
        height=500
    )
    
    st.plotly_chart(fig_efficiency, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 6: ALL TABLES
# ═══════════════════════════════════════════════════════════════════════════

with tab6:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">📋 All KPI Tables from Analysis</h2>', unsafe_allow_html=True)
    
    if show_tables:
        # 1. Category KPIs
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">📦 Category KPIs</h3>', unsafe_allow_html=True)
        category_table = kpis['kpi_category'][['gross_revenue', 'net_revenue', 'discount_amount', 'quantity', 'avg_order_value', 'roi']].round(2)
        st.dataframe(category_table, use_container_width=True)
        
        st.markdown("---")
        
        # 2. Campaign KPIs
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">🎪 Campaign KPIs</h3>', unsafe_allow_html=True)
        campaign_table = kpis['kpi_campaign'][['net_revenue', 'discount_amount', 'quantity', 'customer_id', 'revenue_per_customer', 'roi']].round(2)
        st.dataframe(campaign_table, use_container_width=True)
        
        st.markdown("---")
        
        # 3. Channel KPIs
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">📢 Channel KPIs</h3>', unsafe_allow_html=True)
        channel_table = kpis['kpi_channel'][['net_revenue', 'gross_revenue', 'discount_amount', 'quantity', 'customer_id', 'avg_order_value', 'revenue_per_customer', 'roi']].round(2)
        st.dataframe(channel_table, use_container_width=True)
        
        st.markdown("---")
        
        # 4. Segment KPIs
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">👥 Segment KPIs</h3>', unsafe_allow_html=True)
        segment_table = kpis['kpi_segment'][['net_revenue', 'gross_revenue', 'discount_amount', 'quantity', 'customer_id', 'avg_order_value', 'revenue_per_customer', 'customer_lifetime_value', 'retention_score', 'roi']].round(2)
        st.dataframe(segment_table, use_container_width=True)
        
        st.markdown("---")
        
        # 5. Region KPIs
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">🗺️ Region KPIs</h3>', unsafe_allow_html=True)
        region_table = kpis['kpi_region'][['net_revenue', 'gross_revenue', 'discount_amount', 'quantity', 'customer_id', 'avg_order_value', 'revenue_per_customer', 'roi']].round(2)
        st.dataframe(region_table, use_container_width=True)
        
        st.markdown("---")
        
        # 6. Channel Performance
        st.markdown(f'<h3 style="color: {COLORS["accent"]};">📊 Channel Performance Metrics</h3>', unsafe_allow_html=True)
        channel_perf_table = kpis['channel_perf'][['total_spend', 'total_revenue', 'total_conversions', 'avg_roi']].round(2)
        st.dataframe(channel_perf_table, use_container_width=True)
        
    else:
        st.info("🔒 Enable 'Show Data Tables' in the sidebar to view all KPI tables")

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: {COLORS['light']}; font-size: 12px; padding: 20px;'>
    <p style='margin: 5px;'>✨ Dashboard Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p style='margin: 5px;'>📊 Data Points: {len(filtered_df):,} records</p>
    <p style='margin: 5px;'>🎯 E-Commerce Analytics Dashboard | All Charts from Notebook Analysis</p>
    <p style='margin: 5px;'>© 2024 Analytics Team | All Rights Reserved</p>
    </div>
    """,
    unsafe_allow_html=True
)
