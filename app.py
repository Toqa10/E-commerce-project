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

st.markdown(
    """
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
    </style>
    """,
    unsafe_allow_html=True,
)

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

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "📊 Analytics Dashboard", "🔍 Data Explorer", "ℹ️ About"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters in Analytics Dashboard for detailed insights")

# Load data
df = load_data()

# =============================================================================
# HOME PAGE
# =============================================================================
if page == "🏠 Home":
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🛒 E-commerce Analytics Pro</h1>
            <p style='font-size: 1.3rem; color: #00d9ff; margin-top: 0.5rem;'>
                Advanced Business Intelligence Dashboard
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
            st.markdown("""
                ### 📈 Insights
                - Revenue trends
                - Customer segmentation
                - Marketing ROI
                - Channel performance
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
    st.markdown("Interactive visualizations with real-time filtering")

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
        col1, col2, col3, col4 = st.columns(4)
        
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
            st.metric("📊 Conversion Rate", f"{conversion_rate:.2f}%")
            st.metric("↩️ Return Rate", f"{return_rate:.2f}%")
        
        with col4:
            avg_satisfaction = filtered_df['satisfaction_rating'].mean() if 'satisfaction_rating' in filtered_df.columns else 0
            if 'net_revenue' in filtered_df.columns and 'discount_amount' in filtered_df.columns:
                total_net = filtered_df['net_revenue'].sum()
                total_discount = filtered_df['discount_amount'].sum()
                avg_roi = ((total_net - total_discount) / total_discount * 100) if total_discount > 0 else 0
            else:
                avg_roi = 0
            st.metric("⭐ Satisfaction", f"{avg_satisfaction:.2f}/5")
            st.metric("💹 Avg ROI", f"{avg_roi:.2f}%")
    
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
            
            fig_revenue_trend.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                xaxis_title="Month",
                yaxis_title="Revenue",
                legend_title="Channel",
                xaxis=dict(tickangle=45)
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
            
            fig_conv_trend.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                xaxis_title="Month",
                yaxis_title="Conversions (Unique Customers)",
                legend_title="Channel",
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_conv_trend, use_container_width=True)

        # Chart 3: Overall Monthly Revenue Trend
        if 'month_date' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Overall Monthly Revenue Trend")
            
            monthly_total = filtered_df.groupby('month_date').agg({
                'net_revenue': 'sum',
                'customer_id': 'nunique'
            }).reset_index()
            monthly_total.columns = ['month', 'total_revenue', 'total_conversions']
            
            fig_total_rev = px.line(
                monthly_total,
                x='month',
                y='total_revenue',
                markers=True,
                title='Overall Monthly Revenue Trend'
            )
            
            fig_total_rev.update_traces(
                line=dict(color='#FF9F0D', width=3),
                marker=dict(size=10, color='#3647F5')
            )
            
            fig_total_rev.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Month",
                yaxis_title="Total Revenue",
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_total_rev, use_container_width=True)

        # Chart 4: Overall Monthly Conversions Trend
        if 'month_date' in filtered_df.columns and 'customer_id' in filtered_df.columns:
            st.subheader("Overall Monthly Conversions Trend")
            
            monthly_total = filtered_df.groupby('month_date').agg({
                'customer_id': 'nunique'
            }).reset_index()
            monthly_total.columns = ['month', 'total_conversions']
            
            fig_total_conv = px.line(
                monthly_total,
                x='month',
                y='total_conversions',
                markers=True,
                title='Overall Monthly Conversions Trend'
            )
            
            fig_total_conv.update_traces(
                line=dict(color='#3647F5', width=3),
                marker=dict(size=10, color='#FF9F0D')
            )
            
            fig_total_conv.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Month",
                yaxis_title="Total Conversions",
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_total_conv, use_container_width=True)

    # ========== TAB 2: MARKETING ==========   
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
                
                fig_rev.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f5f5',
                    height=450,
                    margin=dict(t=60)
                )
                
                st.plotly_chart(fig_rev, use_container_width=True)
                
                # Chart 2: Total Conversions per Channel
                st.subheader("Total Conversions per Channel")
                
                fig_conv = px.scatter(
                    channel_perf,
                    x=channel_perf.index,
                    y="total_conversions",
                    size="total_conversions",
                    color="total_conversions",
                    color_continuous_scale=["#FF9F0D", "#D9D9D9"],
                    title="Total Conversions per Channel"
                )
                
                fig_conv.update_traces(
                    marker=dict(symbol='circle', line=dict(width=2, color='#D9D9D9'))
                )
                
                fig_conv.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f5f5',
                    height=450,
                    yaxis_title="Total Conversions",
                    xaxis_title="Marketing Channel"
                )
                
                st.plotly_chart(fig_conv, use_container_width=True)
                
                # Chart 3: Total Orders per Channel (بدل Spend)
                st.subheader("Total Orders per Channel")
                
                # حساب عدد الطلبات لكل قناة
                orders_data = df.groupby('marketing_channel').agg({
                    'order_id': 'count'
                }).reset_index()
                orders_data.columns = ['channel', 'total_orders']
                orders_data = orders_data.set_index('channel')
                
                fig_spend = px.line(
                    orders_data,
                    x=orders_data.index,
                    y="total_orders",
                    markers=True,
                    title="Total Orders per Channel"
                )
                
                fig_spend.update_traces(
                    line=dict(color="#FF9F0D", width=4),
                    marker=dict(size=10, color="#D9D9D9", line=dict(width=2, color="#D9D9D9"))
                )
                
                fig_spend.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f5f5',
                    height=500,
                    yaxis_title="Total Orders",
                    xaxis_title="Marketing Channel"
                )
                
                st.plotly_chart(fig_spend, use_container_width=True)
                
                # Chart 4: Average ROI per Channel
                st.subheader("Average ROI per Channel")
                
                channel_perf_sorted = channel_perf.sort_values(by='avg_roi', ascending=True)
                
                fig_roi = px.bar(
                    channel_perf_sorted,
                    x='avg_roi',
                    y=channel_perf_sorted.index,
                    orientation='h',
                    color='avg_roi',
                    color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D'],
                    title="Average ROI per Channel"
                )
                
                fig_roi.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f5f5',
                    height=450,
                    xaxis_title="Average ROI",
                    yaxis_title="Marketing Channel"
                )
                
                st.plotly_chart(fig_roi, use_container_width=True)
            else:
                st.error("❌ Required columns not found!")
        else:
            st.error("❌ Column 'marketing_channel' not found!")

   
           # ========== TAB 3: PERFORMANCE (NEW) ==========
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
            fig_revenue_order.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )
            fig_revenue_order.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Revenue Per Order ($)",
                yaxis_title="Marketing Channel"
            )
            st.plotly_chart(fig_revenue_order, use_container_width=True)
            
            # Chart 2: Customer Acquisition Rate
            st.subheader("📈 Customer Acquisition Rate by Channel")
            conversion_by_channel = filtered_df.groupby('marketing_channel').agg({
                'customer_id': 'nunique',
                'order_id': 'count'
            }).reset_index()
            conversion_by_channel.columns = ['Channel', 'Unique_Customers', 'Total_Orders']
            conversion_by_channel['Customer_Acquisition_Rate_%'] = (
                (conversion_by_channel['Unique_Customers'] / conversion_by_channel['Total_Orders']) * 100
            ).round(2)
            conversion_by_channel = conversion_by_channel.sort_values('Customer_Acquisition_Rate_%', ascending=False)
            
            fig_acquisition = px.bar(
                conversion_by_channel,
                x='Channel',
                y='Customer_Acquisition_Rate_%',
                title='Customer Acquisition Rate by Channel',
                color='Customer_Acquisition_Rate_%',
                color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
            )
            fig_acquisition.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )
            fig_acquisition.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Marketing Channel",
                yaxis_title="Customer Acquisition Rate (%)",
                xaxis=dict(tickangle=45)
            )
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
            fig_efficiency.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )
            fig_efficiency.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Efficiency Score",
                yaxis_title="Marketing Channel"
            )
            st.plotly_chart(fig_efficiency, use_container_width=True)
            
            # Chart 4: Revenue vs Customer Acquisition
            st.subheader("🎯 Revenue vs Customer Acquisition")
            revenue_analysis = filtered_df.groupby('marketing_channel').agg({
                'final_amount': 'sum',
                'customer_id': 'nunique',
                'order_id': 'count'
            }).reset_index()
            revenue_analysis.columns = ['Channel', 'Total_Revenue', 'Unique_Customers', 'Total_Orders']
            revenue_analysis['Revenue_Per_Customer'] = (
                revenue_analysis['Total_Revenue'] / revenue_analysis['Unique_Customers']
            ).round(2)
            
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
                textfont=dict(size=12, color='#f5f5f5'),
                marker=dict(line=dict(width=2, color='#D9D9D9'), opacity=0.85)
            )
            fig_revenue_customers.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                showlegend=False,
                xaxis_title="Unique Customers Acquired",
                yaxis_title="Total Revenue ($)"
            )
            st.plotly_chart(fig_revenue_customers, use_container_width=True)
            
            # Chart 5: Revenue Per Customer
            st.subheader("💰 Revenue Per Customer by Channel")
            customer_value = filtered_df.groupby('marketing_channel').agg({
                'final_amount': 'sum',
                'customer_id': 'nunique',
                'order_id': 'count'
            }).reset_index()
            customer_value.columns = ['Channel', 'Total_Revenue', 'Total_Customers', 'Total_Orders']
            customer_value['Revenue_Per_Customer'] = (
                customer_value['Total_Revenue'] / customer_value['Total_Customers']
            ).round(2)
            customer_value = customer_value.sort_values('Revenue_Per_Customer')
            
            fig_revenue_customer = px.bar(
                customer_value,
                x='Channel',
                y='Revenue_Per_Customer',
                title='Revenue Per Customer by Channel',
                color='Revenue_Per_Customer',
                color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D']
            )
            fig_revenue_customer.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )
            fig_revenue_customer.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Marketing Channel",
                yaxis_title="Revenue Per Customer ($)",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_revenue_customer, use_container_width=True)
            
            # Chart 6: Performance Quadrant Analysis
            st.subheader("🏆 Performance Quadrant Analysis")
            
            quadrant_analysis = filtered_df.groupby('marketing_channel').agg({
                'customer_id': 'nunique',
                'final_amount': 'sum',
                'order_id': 'count'
            }).reset_index()
            quadrant_analysis.columns = ['Channel', 'Unique_Customers', 'Total_Revenue', 'Total_Orders']
            quadrant_analysis['Revenue_Per_Customer'] = (
                quadrant_analysis['Total_Revenue'] / quadrant_analysis['Unique_Customers']
            ).round(2)
            
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
            
            fig_quadrant.update_traces(
                marker=dict(line=dict(width=2, color='#D9D9D9'), opacity=0.9)
            )
            
            fig_quadrant.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                xaxis_title="Unique Customers Acquired",
                yaxis_title="Total Revenue ($)",
                showlegend=False
            )
            
            # Quadrant lines
            fig_quadrant.add_hline(
                y=avg_revenue,
                line_dash="dash",
                line_color="#FF9F0D",
                annotation_text=f"Avg Revenue: ${avg_revenue:,.0f}",
                annotation_position="right"
            )
            
            fig_quadrant.add_vline(
                x=avg_customers,
                line_dash="dash",
                line_color="#FF9F0D",
                annotation_text=f"Avg Customers: {avg_customers:,.0f}",
                annotation_position="top"
            )
            
            st.plotly_chart(fig_quadrant, use_container_width=True)
            
            # Best performer info
            best_channel = quadrant_analysis.loc[quadrant_analysis['Revenue_Per_Customer'].idxmax()]
            st.success(f"🌟 **Best Performer:** {best_channel['Channel']} - Revenue/Customer: ${best_channel['Revenue_Per_Customer']:,.2f}")


# =============================================================================
# DATA EXPLORER
# =============================================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("Browse and filter your data")

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

    st.markdown("""
    ## 🛒 E-commerce Analytics Pro

    A comprehensive business intelligence dashboard for e-commerce data analysis.

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
    - **Styling**: Custom CSS with gradient themes

    ### 📝 How to Use

    1. **Home**: Get quick overview of your business
    2. **Analytics Dashboard**: Dive deep into visualizations
    3. **Data Explorer**: Filter and export specific data

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

    **Version**: 1.0.0  
    **Last Updated**: December 2025  
    **Built with** ❤️ **using Streamlit**
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
st.markdown("""
    <div class='footer'>
        <p>📊 E-commerce Analytics Pro | Built with Streamlit</p>
        <p>© 2025 | All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
