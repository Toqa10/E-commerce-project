import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.io as pio
import base64
from PIL import Image

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
# DISPLAY DASHBOARD IMAGE
# ═══════════════════════════════════════════════════════════════════════════

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-image: url(https://i.ibb.co/7jLm1cv/WhatsApp-Image-2025-12-08-at-21-32-57-cf4377fb.jpg);
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center top;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

# ═══════════════════════════════════════════════════════════════════════════
# LOAD & PROCESS DATA - FIXED
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv('cleaned_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['year_month'] = df['date'].dt.to_period('M')
        df['month_name'] = df['date'].dt.month_name()
        
        # Calculate all KPIs EXACTLY from notebook
        df['Average Order Value'] = df['final_amount'] / df['quantity']
        df['revenue_per_customer'] = df['final_amount'].sum() / df['customer_id'].nunique()
        df['discount_amount'] = df['price'] * df['discount_percent'] / 100
        df['gross_revenue'] = df['price'] * df['quantity']
        df['net_revenue'] = df['final_amount']
        df['roi'] = (df['net_revenue'] - df['discount_amount']) / df['discount_amount']
        
        # Conversion rate per customer
        orders_per_customer = df.groupby('customer_id').size()
        df['conversion_rate'] = df['customer_id'].map(orders_per_customer)
        
        return df
    except FileNotFoundError:
        st.error("❌ File 'cleaned_data.csv' not found. Please upload it first.")
        return pd.DataFrame()

df = load_and_process_data()

if df.empty:
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# FIXED KPI CALCULATIONS - MATCH NOTEBOOK EXACTLY
# ═══════════════════════════════════════════════════════════════════════════

def calculate_all_kpis(filtered_df):
    """Calculate KPIs exactly as in the notebook"""
    
    # Category KPIs
    kpi_category = filtered_df.groupby('category').agg({
        'gross_revenue': 'sum',
        'net_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    }).round(2)
    kpi_category['avg_order_value'] = kpi_category['net_revenue'] / kpi_category['quantity']
    kpi_category['roi'] = (kpi_category['net_revenue'] - kpi_category['discount_amount']) / kpi_category['discount_amount']
    
    # Campaign KPIs
    kpi_campaign = filtered_df.groupby('marketing_campaign').agg({
        'net_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    kpi_campaign['revenue_per_customer'] = kpi_campaign['net_revenue'] / kpi_campaign['customer_id']
    kpi_campaign['roi'] = (kpi_campaign['net_revenue'] - kpi_campaign['discount_amount']) / kpi_campaign['discount_amount']
    
    # Channel KPIs
    kpi_channel = filtered_df.groupby('marketing_channel').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    kpi_channel['avg_order_value'] = kpi_channel['net_revenue'] / kpi_channel['quantity']
    kpi_channel['revenue_per_customer'] = kpi_channel['net_revenue'] / kpi_channel['customer_id']
    kpi_channel['roi'] = (kpi_channel['net_revenue'] - kpi_channel['discount_amount']) / kpi_channel['discount_amount']
    
    # Customer Segment KPIs
    kpi_segment = filtered_df.groupby('customer_segment').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique',
        'customer_lifetime_value': 'mean',
        'retention_score': 'mean'
    }).round(2)
    kpi_segment['avg_order_value'] = kpi_segment['net_revenue'] / kpi_segment['quantity']
    kpi_segment['revenue_per_customer'] = kpi_segment['net_revenue'] / kpi_segment['customer_id']
    kpi_segment['roi'] = (kpi_segment['net_revenue'] - kpi_segment['discount_amount']) / kpi_segment['discount_amount']
    
    # Region KPIs
    kpi_region = filtered_df.groupby('region').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    kpi_region['avg_order_value'] = kpi_region['net_revenue'] / kpi_region['quantity']
    kpi_region['revenue_per_customer'] = kpi_region['net_revenue'] / kpi_region['customer_id']
    kpi_region['roi'] = (kpi_region['net_revenue'] - kpi_region['discount_amount']) / kpi_region['discount_amount']
    
    # Month KPIs
    kpi_month = filtered_df.groupby('month').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    }).round(2)
    kpi_month['avg_order_value'] = kpi_month['net_revenue'] / kpi_month['quantity']
    kpi_month['roi'] = (kpi_month['net_revenue'] - kpi_month['discount_amount']) / kpi_month['discount_amount']
    
    # Quarter KPIs
    kpi_quarter = filtered_df.groupby('quarter').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    }).round(2)
    kpi_quarter['avg_order_value'] = kpi_quarter['net_revenue'] / kpi_quarter['quantity']
    kpi_quarter['roi'] = (kpi_quarter['net_revenue'] - kpi_quarter['discount_amount']) / kpi_quarter['discount_amount']
    
    # Season KPIs
    kpi_season = filtered_df.groupby('season').agg({
        'net_revenue': 'sum',
        'gross_revenue': 'sum',
        'discount_amount': 'sum',
        'quantity': 'sum'
    }).round(2)
    kpi_season['avg_order_value'] = kpi_season['net_revenue'] / kpi_season['quantity']
    kpi_season['roi'] = (kpi_season['net_revenue'] - kpi_season['discount_amount']) / kpi_season['discount_amount']
    
    # Channel Performance (Fixed)
    channel_perf = filtered_df.groupby('marketing_channel').agg({
        'discount_percent': 'sum',
        'final_amount': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    channel_perf['total_spend'] = channel_perf['discount_percent']
    channel_perf['total_revenue'] = channel_perf['final_amount']
    channel_perf['total_conversions'] = channel_perf['customer_id']
    channel_perf['avg_roi'] = (channel_perf['total_revenue'] - channel_perf['total_spend']) / channel_perf['total_spend']
    
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
    st.title("E-Commerce Analytics Dashboard")
    st.markdown(f"<p style='color: {COLORS['light']}; margin-top: -20px;'>Data-Driven Business Intelligence | All Charts from Notebook</p>", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - FILTERS (Simplified)
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">🎛️ FILTERS</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Date Range
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        start_date = st.date_input("📅 Start Date", value=df['date'].min().date())
    with col_date2:
        end_date = st.date_input("📅 End Date", value=df['date'].max().date())
    
    # Key Filters
    selected_channels = st.multiselect("📢 Channels", options=sorted(df['marketing_channel'].unique()), default=sorted(df['marketing_channel'].unique()))
    
    st.markdown("---")
    show_tables = st.checkbox("📋 Show Data Tables", value=False)

# Apply Filters
filtered_df = df[
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date) &
    (df['marketing_channel'].isin(selected_channels))
].reset_index(drop=True)

kpis = calculate_all_kpis(filtered_df)

# ═══════════════════════════════════════════════════════════════════════════
# TABS - SIMPLIFIED WITH WORKING CHARTS
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎯 Performance", "📋 Tables"])

with tab1:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">📊 Executive Overview</h2>', unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    total_revenue = filtered_df['net_revenue'].sum()
    total_customers = filtered_df['customer_id'].nunique()
    total_orders = len(filtered_df)
    avg_order_value = filtered_df['final_amount'].mean()
    
    with col1: st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    with col2: st.metric("👥 Total Customers", f"{total_customers:,}")
    with col3: st.metric("📦 Total Orders", f"{total_orders:,}")
    with col4: st.metric("💵 Avg Order Value", f"${avg_order_value:.2f}")
    
    # Charts from Notebook Style
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Revenue by Channel (Notebook Style)
        fig_channel = px.bar(
            kpis['kpi_channel'][['net_revenue']].reset_index().sort_values('net_revenue', ascending=False),
            x='marketing_channel', y='net_revenue',
            title='💰 Revenue by Channel',
            color='net_revenue',
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            text_auto='$.0f'
        )
        fig_channel.update_layout(
            plot_bgcolor='#040D2F', paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'), height=400
        )
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col_b:
        # Top Categories (Notebook Style)
        top_cats = kpis['kpi_category']['net_revenue'].sort_values(ascending=False).head(10)
        fig_cat = px.bar(
            x=top_cats.values, y=top_cats.index,
            orientation='h', title='📦 Top Categories',
            color=top_cats.values,
            color_continuous_scale=['#FF9F0D', '#3647F5']
        )
        fig_cat.update_layout(
            plot_bgcolor='#040D2F', paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'), height=400
        )
        st.plotly_chart(fig_cat, use_container_width=True)

with tab2:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">📈 Performance Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROI by Channel
        fig_roi = px.bar(
            kpis['kpi_channel'][['roi']].sort_values('roi', ascending=False).reset_index(),
            x='marketing_channel', y='roi',
            title='📈 ROI by Channel',
            color='roi',
            color_continuous_scale=['#FF4444', '#FF9F0D', '#00C851'],
            text_auto='.2f'
        )
        fig_roi.update_layout(plot_bgcolor='#040D2F', paper_bgcolor='#040D2F', height=400)
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        # Campaign Performance
        fig_campaign = px.bar(
            kpis['kpi_campaign'][['net_revenue']].sort_values('net_revenue', ascending=False).reset_index(),
            x='marketing_campaign', y='net_revenue',
            title='🎯 Campaign Revenue',
            color='net_revenue',
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            text_auto='$.0f'
        )
        fig_campaign.update_layout(plot_bgcolor='#040D2F', paper_bgcolor='#040D2F', height=400)
        st.plotly_chart(fig_campaign, use_container_width=True)

with tab3:
    if show_tables:
        st.markdown(f'<h2 style="color: {COLORS["accent"]};">📋 All KPI Tables</h2>', unsafe_allow_html=True)
        
        st.subheader("📦 Category Performance")
        st.dataframe(kpis['kpi_category'])
        
        st.subheader("📢 Channel Performance")
        st.dataframe(kpis['kpi_channel'])
        
        st.subheader("🎪 Campaign Performance")
        st.dataframe(kpis['kpi_campaign'])
    else:
        st.info("✅ Enable 'Show Data Tables' in sidebar to view detailed KPIs")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: {COLORS['light']};'>✨ Dashboard powered by notebook analysis | {len(filtered_df):,} records analyzed</p>", unsafe_allow_html=True)
