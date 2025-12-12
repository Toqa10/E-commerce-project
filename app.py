import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# E-COMMERCE THEME (Professional Blue/Green)
# =============================================================================
st.set_page_config(
    page_title="📊 E-commerce Analytics Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME MANAGEMENT - LIGHT MODE FEATURE
# =============================================================================
# Initialize theme in session state
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'  # Default is dark mode

# Function to toggle theme
def toggle_theme():
    if st.session_state.theme_mode == 'dark':
        st.session_state.theme_mode = 'light'
    else:
        st.session_state.theme_mode = 'dark'

# Function to get current theme CSS
def get_theme_css():
    if st.session_state.theme_mode == 'light':
        return """
        <style>
        :root {
          --primary-blue: #1f77b4;
          --secondary-green: #2ecc71;
          --bg-dark: #f8f9fa;
          --panel-dark: #ffffff;
          --text-light: #333333;
          --accent-cyan: #007bff;
          --warning-orange: #ff9800;
        }

        html, body, .stApp {
          background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
          color: var(--text-light) !important;
        }

        h1, h2, h3, h4, h5, h6,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
          color: var(--accent-cyan) !important;
          text-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
          font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
          border-right: 2px solid #e0e0e0;
        }

        section[data-testid="stSidebar"] * {
          color: var(--text-light) !important;
        }

        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stDateInput label {
          color: var(--accent-cyan) !important;
          font-weight: 600 !important;
        }

        div.stButton > button {
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%) !important;
          color: white !important;
          border: none !important;
          font-weight: 700 !important;
          padding: 0.6rem 2rem !important;
          border-radius: 8px !important;
          box-shadow: 0 4px 15px rgba(31, 119, 180, 0.3) !important;
          transition: all 0.3s ease !important;
        }

        div.stButton > button:hover {
          transform: translateY(-2px) !important;
          box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4) !important;
        }

        [data-testid="stMetricValue"] {
          color: var(--secondary-green) !important;
          font-size: 2rem !important;
          font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
          color: var(--accent-cyan) !important;
          font-weight: 600 !important;
        }

        div[data-testid="stExpander"] {
          background-color: var(--panel-dark) !important;
          border: 1px solid #e0e0e0 !important;
          border-radius: 10px !important;
        }

        .stDataFrame {
          background-color: var(--panel-dark) !important;
          border: 1px solid #e0e0e0 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
          gap: 8px;
          background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
          background-color: var(--panel-dark);
          border-radius: 8px 8px 0 0;
          color: var(--text-light);
          border: 1px solid #e0e0e0;
          padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%);
          color: white;
        }

        .stAlert {
          background-color: var(--panel-dark) !important;
          border-left: 4px solid var(--accent-cyan) !important;
        }

        a {
          color: var(--accent-cyan) !important;
          text-decoration: none !important;
        }

        a:hover {
          color: var(--secondary-green) !important;
        }

        hr {
          border-color: #e0e0e0 !important;
          opacity: 0.5 !important;
        }

        .stDownloadButton > button {
          background-color: var(--secondary-green) !important;
          color: white !important;
        }

        .metric-card {
          background: linear-gradient(135deg, var(--panel-dark) 0%, rgba(31, 119, 180, 0.05) 100%);
          padding: 1.5rem;
          border-radius: 12px;
          border: 1px solid #e0e0e0;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
          text-align: center;
          margin-bottom: 1rem;
        }

        .metric-value {
          font-size: 2.5rem;
          font-weight: 700;
          color: var(--secondary-green);
          margin: 0.5rem 0;
        }

        .metric-label {
          font-size: 1rem;
          color: var(--accent-cyan);
          font-weight: 600;
        }

        .footer {
          text-align: center;
          padding: 2rem;
          color: var(--text-light);
          opacity: 0.7;
          border-top: 1px solid #e0e0e0;
          margin-top: 3rem;
        }
        
        .theme-indicator {
          display: inline-block;
          padding: 5px 15px;
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%);
          color: white;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 600;
          margin: 10px 0;
        }
        
        .plotly .modebar {
          background-color: var(--panel-dark) !important;
        }
        
        .plotly .modebar-btn path {
          fill: var(--text-light) !important;
        }
        </style>
        """
    else:
        return """
        <style>
        :root {
          --primary-blue: #1f77b4;
          --secondary-green: #2ecc71;
          --bg-dark: #0f1419;
          --panel-dark: #1a1f2e;
          --text-light: #f5f5f5;
          --accent-cyan: #00d9ff;
          --warning-orange: #ff9800;
        }

        html, body, .stApp {
          background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
          color: var(--text-light) !important;
        }

        h1, h2, h3, h4, h5, h6,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
          color: var(--accent-cyan) !important;
          text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
          font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%) !important;
          border-right: 2px solid var(--primary-blue);
        }

        section[data-testid="stSidebar"] * {
          color: var(--text-light) !important;
        }

        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stDateInput label {
          color: var(--accent-cyan) !important;
          font-weight: 600 !important;
        }

        div.stButton > button {
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%) !important;
          color: white !important;
          border: none !important;
          font-weight: 700 !important;
          padding: 0.6rem 2rem !important;
          border-radius: 8px !important;
          box-shadow: 0 4px 15px rgba(31, 119, 180, 0.4) !important;
          transition: all 0.3s ease !important;
        }

        div.stButton > button:hover {
          transform: translateY(-2px) !important;
          box-shadow: 0 6px 20px rgba(31, 119, 180, 0.6) !important;
        }

        [data-testid="stMetricValue"] {
          color: var(--secondary-green) !important;
          font-size: 2rem !important;
          font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
          color: var(--accent-cyan) !important;
          font-weight: 600 !important;
        }

        div[data-testid="stExpander"] {
          background-color: var(--panel-dark) !important;
          border: 1px solid var(--primary-blue) !important;
          border-radius: 10px !important;
        }

        .stDataFrame {
          background-color: var(--panel-dark) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
          gap: 8px;
          background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
          background-color: var(--panel-dark);
          border-radius: 8px 8px 0 0;
          color: var(--text-light);
          border: 1px solid var(--primary-blue);
          padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%);
          color: white;
        }

        .stAlert {
          background-color: var(--panel-dark) !important;
          border-left: 4px solid var(--accent-cyan) !important;
        }

        a {
          color: var(--accent-cyan) !important;
          text-decoration: none !important;
        }

        a:hover {
          color: var(--secondary-green) !important;
        }

        hr {
          border-color: var(--primary-blue) !important;
          opacity: 0.3 !important;
        }

        .stDownloadButton > button {
          background-color: var(--secondary-green) !important;
          color: white !important;
        }

        .metric-card {
          background: linear-gradient(135deg, var(--panel-dark) 0%, rgba(31, 119, 180, 0.1) 100%);
          padding: 1.5rem;
          border-radius: 12px;
          border: 1px solid var(--primary-blue);
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
          text-align: center;
          margin-bottom: 1rem;
        }

        .metric-value {
          font-size: 2.5rem;
          font-weight: 700;
          color: var(--secondary-green);
          margin: 0.5rem 0;
        }

        .metric-label {
          font-size: 1rem;
          color: var(--accent-cyan);
          font-weight: 600;
        }

        .footer {
          text-align: center;
          padding: 2rem;
          color: var(--text-light);
          opacity: 0.7;
          border-top: 1px solid var(--primary-blue);
          margin-top: 3rem;
        }
        
        .theme-indicator {
          display: inline-block;
          padding: 5px 15px;
          background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-green) 100%);
          color: white;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 600;
          margin: 10px 0;
        }
        </style>
        """

# Apply theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION WITH THEME TOGGLE
# =============================================================================
st.sidebar.title("🎨 Theme Settings")

# Theme toggle button
theme_icon = "☀️" if st.session_state.theme_mode == 'dark' else "🌙"
theme_text = "Switch to Light Mode" if st.session_state.theme_mode == 'dark' else "Switch to Dark Mode"

if st.sidebar.button(f"{theme_icon} {theme_text}", use_container_width=True, type="primary"):
    toggle_theme()
    st.rerun()

# Display current theme status
st.sidebar.markdown(f"""
<div class='theme-indicator'>
    Current Theme: {'🌙 Dark Mode' if st.session_state.theme_mode == 'dark' else '☀️ Light Mode'}
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "📊 Analytics Dashboard", "🔍 Data Explorer", "ℹ️ About"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info(f"💡 **Tip**: {'Use Light Mode for daytime viewing' if st.session_state.theme_mode == 'dark' else 'Use Dark Mode for nighttime viewing'}")

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cleaned_data.csv')

        # Date conversions
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            if 'month_date' not in df.columns:
                df['month_date'] = df['date'].dt.to_period('M').dt.to_timestamp()

        if 'registration_date' in df.columns:
            df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')

        return df
    except FileNotFoundError:
        st.error("⚠️ File 'cleaned_data.csv' not found!")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Load data
df = load_data()

# =============================================================================
# HOME PAGE
# =============================================================================
if page == "🏠 Home":
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🛒 E-commerce Analytics Pro</h1>
            <p style='font-size: 1.3rem; margin-top: 0.5rem;'>
                Advanced Business Intelligence Dashboard • {'🌙 Dark Mode' if st.session_state.theme_mode == 'dark' else '☀️ Light Mode'}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if df is not None:
        # Quick Stats
        st.header("📈 Quick Overview")

        col1, col2, col3, col4 = st.columns(4)

        total_revenue = df['net_revenue'].sum() if 'net_revenue' in df.columns else 0
        total_orders = len(df)
        total_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
        avg_order = df['final_amount'].mean() if 'final_amount' in df.columns else 0

        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>💰 Total Revenue</div>
                    <div class='metric-value'>${total_revenue:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>📦 Total Orders</div>
                    <div class='metric-value'>{total_orders:,}</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>👥 Customers</div>
                    <div class='metric-value'>{total_customers:,}</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>🛍️ Avg Order</div>
                    <div class='metric-value'>${avg_order:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Features Section
        st.header("🚀 Key Features")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                ### 📊 Analytics Dashboard
                - 15+ Interactive charts
                - 8 Key Performance Indicators
                - Real-time filtering
                - Multi-dimensional analysis
            """)

        with col2:
            st.markdown("""
                ### 🔍 Data Explorer
                - Advanced filtering
                - Sortable data table
                - Export to CSV
                - Search capabilities
            """)

        with col3:
            theme_feature = "🌙 Dark Mode" if st.session_state.theme_mode == 'dark' else "☀️ Light Mode"
            st.markdown(f"""
                ### 🎨 Smart Themes
                - {theme_feature} active
                - Easy toggle switch
                - Eye comfort optimization
                - Professional design
            """)

        st.markdown("---")

        # Dataset Info
        st.header("📋 Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                **Records**: {len(df):,}  
                **Columns**: {len(df.columns)}  
                **Date Range**: {df['date'].min().strftime('%Y-%m-%d') if 'date' in df.columns else 'N/A'} 
                to {df['date'].max().strftime('%Y-%m-%d') if 'date' in df.columns else 'N/A'}
            """)

        with col2:
            if st.button("📋 View Column Names"):
                st.write(df.columns.tolist())

        with st.expander("👁️ Preview Data (First 10 Rows)"):
            st.dataframe(df.head(10), use_container_width=True)

    else:
        st.warning("⚠️ No data available. Please check the CSV file.")

# =============================================================================
# ANALYTICS DASHBOARD
# =============================================================================
elif page == "📊 Analytics Dashboard":
    st.title("📊 Analytics Dashboard")
    st.markdown(f"Interactive visualizations • Current Theme: **{'🌙 Dark' if st.session_state.theme_mode == 'dark' else '☀️ Light'}**")

    if df is None:
        st.error("❌ Data not loaded!")
        st.stop()

    # ========== FILTERS ==========
    st.sidebar.header("🔍 Filters")

    # Channel filter
    if 'marketing_channel' in df.columns:
        channels = ['All Channels'] + sorted(df['marketing_channel'].dropna().unique().tolist())
        selected_channel = st.sidebar.selectbox("Marketing Channel", channels)
    else:
        selected_channel = 'All Channels'

    # Date filter
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

     # ========== KPIs ==========
    st.header("📈 Key Performance Indicators")
    
    # إنشاء tabs للـ KPIs المختلفة
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

    # ========== CHARTS FROM NOTEBOOK ==========
    st.header("📊 Data Visualizations")

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🎯 Marketing", "📦 Performance"])

    # ========== TAB 1: TRENDS ==========
    with tab1:
        # Chart 1: Monthly Revenue Trends by Marketing Channel
        if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Monthly Revenue Trends by Marketing Channel")
            
            monthly_channel = filtered_df.groupby(['month_date', 'marketing_channel']).agg({
                'net_revenue': 'sum',
                'customer_id': 'nunique'
            }).reset_index()
            monthly_channel.columns = ['month', 'channel', 'revenue', 'conversions']
            
            fig_revenue_trend = px.line(
                monthly_channel,
                x='month',
                y='revenue',
                color='channel',
                markers=True,
                title='Monthly Revenue Trends by Marketing Channel'
            )
            
            # تطبيق السمة على الرسوم البيانية
            bg_color = '#ffffff' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            paper_color = '#f8f9fa' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            text_color = '#333333' if st.session_state.theme_mode == 'light' else '#f5f5f5'
            grid_color = '#e0e0e0' if st.session_state.theme_mode == 'light' else '#2a3240'
            
            fig_revenue_trend.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=paper_color,
                font_color=text_color,
                height=500,
                xaxis_title="Month",
                yaxis_title="Revenue",
                legend_title="Channel",
                xaxis=dict(
                    tickangle=45,
                    gridcolor=grid_color,
                    linecolor=grid_color
                ),
                yaxis=dict(
                    gridcolor=grid_color,
                    linecolor=grid_color
                )
            )
            
            st.plotly_chart(fig_revenue_trend, use_container_width=True)

        # Chart 2: Monthly Conversions Trends by Marketing Channel
        if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns and 'customer_id' in filtered_df.columns:
            st.subheader("Monthly Conversions Trends by Marketing Channel")
            
            monthly_channel = filtered_df.groupby(['month_date', 'marketing_channel']).agg({
                'customer_id': 'nunique'
            }).reset_index()
            monthly_channel.columns = ['month', 'channel', 'conversions']
            
            fig_conv_trend = px.line(
                monthly_channel,
                x='month',
                y='conversions',
                color='channel',
                markers=True,
                title='Monthly Conversions Trends by Marketing Channel'
            )
            
            bg_color = '#ffffff' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            paper_color = '#f8f9fa' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            text_color = '#333333' if st.session_state.theme_mode == 'light' else '#f5f5f5'
            grid_color = '#e0e0e0' if st.session_state.theme_mode == 'light' else '#2a3240'
            
            fig_conv_trend.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=paper_color,
                font_color=text_color,
                height=500,
                xaxis_title="Month",
                yaxis_title="Conversions (Unique Customers)",
                legend_title="Channel",
                xaxis=dict(
                    tickangle=45,
                    gridcolor=grid_color,
                    linecolor=grid_color
                ),
                yaxis=dict(
                    gridcolor=grid_color,
                    linecolor=grid_color
                )
            )
            
            st.plotly_chart(fig_conv_trend, use_container_width=True)

    # ========== TAB 2: MARKETING ==========   
    with tab2:
        if 'marketing_channel' in df.columns:
            revenue_col = 'net_revenue' if 'net_revenue' in df.columns else 'final_amount'
            
            if revenue_col in df.columns and 'customer_id' in df.columns and 'roi' in df.columns:
                # تنظيف ROI من inf قبل الـ groupby
                df_clean = df.copy()
                df_clean['roi'] = df_clean['roi'].replace([float('inf'), float('-inf')], float('nan'))
                
                # تحضير البيانات
                channel_perf = df_clean.groupby('marketing_channel').agg({
                    revenue_col: 'sum',
                    'customer_id': 'nunique',
                    'roi': 'mean'
                }).reset_index()
                channel_perf.columns = ['channel', 'total_revenue', 'total_conversions', 'avg_roi']
                channel_perf = channel_perf.set_index('channel')
                
                # Chart 1: Total Revenue per Marketing Channel
                st.subheader("Total Revenue per Marketing Channel")
                bar_width = 25
                
                fig_rev = px.scatter(
                    channel_perf,
                    x=channel_perf.index,
                    y="total_revenue",
                    title="Total Revenue per Marketing Channel",
                    color_discrete_sequence=["#3647F5"],
                    text="total_revenue"
                )
                
                fig_rev.update_traces(
                    marker=dict(size=bar_width),
                    textposition='top center',
                    texttemplate='%{text:.2s}'
                )
                
                for x_val, y_val in zip(channel_perf.index, channel_perf["total_revenue"]):
                    fig_rev.add_shape(
                        type="line",
                        x0=x_val, y0=0,
                        x1=x_val, y1=y_val,
                        line=dict(color="#3647F5", width=bar_width),
                        layer="below"
                    )
                
                bg_color = '#ffffff' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
                paper_color = '#f8f9fa' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
                text_color = '#333333' if st.session_state.theme_mode == 'light' else '#f5f5f5'
                grid_color = '#e0e0e0' if st.session_state.theme_mode == 'light' else '#2a3240'
                
                fig_rev.update_layout(
                    plot_bgcolor=bg_color,
                    paper_bgcolor=paper_color,
                    font_color=text_color,
                    height=450,
                    margin=dict(t=60),
                    xaxis=dict(
                        gridcolor=grid_color,
                        linecolor=grid_color
                    ),
                    yaxis=dict(
                        gridcolor=grid_color,
                        linecolor=grid_color
                    )
                )
                
                st.plotly_chart(fig_rev, use_container_width=True)

    # ========== TAB 3: PERFORMANCE ==========
    with tab3:
        st.subheader("📊 Marketing Channel Performance Analysis")
        
        if 'marketing_channel' in filtered_df.columns:
            # تحضير البيانات الأساسية
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
            
            bg_color = '#ffffff' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            paper_color = '#f8f9fa' if st.session_state.theme_mode == 'light' else 'rgba(0,0,0,0)'
            text_color = '#333333' if st.session_state.theme_mode == 'light' else '#f5f5f5'
            grid_color = '#e0e0e0' if st.session_state.theme_mode == 'light' else '#2a3240'
            
            fig_revenue_order.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )
            fig_revenue_order.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=paper_color,
                font_color=text_color,
                height=450,
                xaxis_title="Revenue Per Order ($)",
                yaxis_title="Marketing Channel",
                xaxis=dict(
                    gridcolor=grid_color,
                    linecolor=grid_color
                )
            )
            st.plotly_chart(fig_revenue_order, use_container_width=True)

# =============================================================================
# DATA EXPLORER
# =============================================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown(f"Browse and filter your data • Current Theme: **{'🌙 Dark' if st.session_state.theme_mode == 'dark' else '☀️ Light'}**")

    if df is None:
        st.error("❌ Data not loaded!")
        st.stop()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'category' in df.columns:
            categories = ['All'] + sorted(df['category'].dropna().unique().tolist())
            selected_cat = st.selectbox("Category", categories)
        else:
            selected_cat = 'All'

    with col2:
        if 'region' in df.columns:
            regions = ['All'] + sorted(df['region'].dropna().unique().tolist())
            selected_region = st.selectbox("Region", regions)
        else:
            selected_region = 'All'

    with col3:
        if 'customer_segment' in df.columns:
            segments = ['All'] + sorted(df['customer_segment'].dropna().unique().tolist())
            selected_segment = st.selectbox("Segment", segments)
        else:
            selected_segment = 'All'

    # Apply filters
    explorer_df = df.copy()

    if selected_cat != 'All' and 'category' in df.columns:
        explorer_df = explorer_df[explorer_df['category'] == selected_cat]

    if selected_region != 'All' and 'region' in df.columns:
        explorer_df = explorer_df[explorer_df['region'] == selected_region]

    if selected_segment != 'All' and 'customer_segment' in df.columns:
        explorer_df = explorer_df[explorer_df['customer_segment'] == selected_segment]

    st.info(f"📊 Displaying {len(explorer_df):,} records")

    # Display data
    st.dataframe(explorer_df, use_container_width=True, height=500)

    # Download
    csv = explorer_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name=f'ecommerce_filtered_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
    )

# =============================================================================
# ABOUT
# =============================================================================
elif page == "ℹ️ About":
    st.title("ℹ️ About This Application")

    st.markdown(f"""
    ## 🛒 E-commerce Analytics Pro

    A comprehensive business intelligence dashboard for e-commerce data analysis.

    ### 🎨 Theme Features

    - **🌙 Dark Mode**: Default professional dark theme
    - **☀️ Light Mode**: Bright theme for daytime use
    - **Easy Toggle**: Switch between themes with one click
    - **Session Persistence**: Theme preferences saved during session

    ### 🎯 Features

    - **Real-time Analytics**: Interactive KPIs and metrics
    - **15+ Visualization Types**: Charts covering all business aspects
    - **Advanced Filtering**: Multi-dimensional data exploration
    - **Export Capabilities**: Download filtered data as CSV
    - **Responsive Design**: Works on all screen sizes

    ### 📊 Key Metrics Tracked

    - Revenue (Gross & Net)
    - Customer Lifetime Value
    - Return on Investment
    - Conversion Rates
    - Customer Satisfaction
    - Return Rates

    ### 🔧 Technical Stack

    - **Framework**: Streamlit
    - **Data Processing**: Pandas, NumPy
    - **Visualizations**: Plotly
    - **Styling**: Custom CSS with dual themes

    ### 📝 How to Use

    1. **Toggle Theme**: Use the button in sidebar to switch between Dark/Light modes
    2. **Home**: Get quick overview of your business
    3. **Analytics Dashboard**: Dive deep into visualizations
    4. **Data Explorer**: Filter and export specific data

    ### 💻 Requirements

    ```
    streamlit>=1.29.0
    pandas>=2.1.0
    plotly>=5.18.0
    numpy>=1.24.0
    ```

    ### 🚀 Running the App

    ```
    streamlit run app.py
    ```

    ---

    **Version**: 1.1.0 (with Theme Support)  
    **Last Updated**: December 2025  
    **Current Theme**: {'🌙 Dark Mode' if st.session_state.theme_mode == 'dark' else '☀️ Light Mode'}
    """)

    st.markdown("---")

    with st.expander("🔍 System Information"):
        if df is not None:
            st.write("**Dataset Info:**")
            st.write(f"- Total Records: {len(df):,}")
            st.write(f"- Total Columns: {len(df.columns)}")
            st.write(f"- Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

            st.write("\n**Available Columns:**")
            st.write(df.columns.tolist())

# =============================================================================
# FOOTER
# =============================================================================
st.markdown(f"""
    <div class='footer'>
        <p>📊 E-commerce Analytics Pro | Built with Streamlit</p>
        <p>© 2025 | Current Theme: {'🌙 Dark Mode' if st.session_state.theme_mode == 'dark' else '☀️ Light Mode'}</p>
    </div>
""", unsafe_allow_html=True)
