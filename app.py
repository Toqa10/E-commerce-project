import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

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

    /* App background */
    html, body, .stApp {
      background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
      color: var(--text-light) !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
      color: var(--accent-cyan) !important;
      text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
      font-weight: 700 !important;
    }

    /* Sidebar */
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

    /* Buttons */
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

    /* Metrics */
    [data-testid="stMetricValue"] {
      color: var(--secondary-green) !important;
      font-size: 2rem !important;
      font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
      color: var(--accent-cyan) !important;
      font-weight: 600 !important;
    }

    /* Cards/Containers */
    div[data-testid="stExpander"] {
      background-color: var(--panel-dark) !important;
      border: 1px solid var(--primary-blue) !important;
      border-radius: 10px !important;
    }

    /* DataFrames */
    .stDataFrame {
      background-color: var(--panel-dark) !important;
    }

    /* Tabs */
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

    /* Info boxes */
    .stAlert {
      background-color: var(--panel-dark) !important;
      border-left: 4px solid var(--accent-cyan) !important;
    }

    /* Links */
    a {
      color: var(--accent-cyan) !important;
      text-decoration: none !important;
    }

    a:hover {
      color: var(--secondary-green) !important;
    }

    /* Divider */
    hr {
      border-color: var(--primary-blue) !important;
      opacity: 0.3 !important;
    }

    /* Download button */
    .stDownloadButton > button {
      background-color: var(--secondary-green) !important;
      color: white !important;
    }

    /* Custom metric card */
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

    /* Footer */
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
    # Hero Section
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
                - 13 Interactive charts
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
                - Seasonal patterns
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

        # Sample Data
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
        channels = ['All'] + sorted(df['marketing_channel'].dropna().unique().tolist())
        selected_channel = st.sidebar.selectbox("Marketing Channel", channels)
    else:
        selected_channel = 'All'

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

    if selected_channel != 'All' and 'marketing_channel' in df.columns:
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

    col1, col2, col3, col4 = st.columns(4)

    revenue = filtered_df['net_revenue'].sum() if 'net_revenue' in filtered_df.columns else 0
    customers = filtered_df['customer_id'].nunique() if 'customer_id' in filtered_df.columns else 0
    orders = len(filtered_df)
    aov = filtered_df['final_amount'].mean() if 'final_amount' in filtered_df.columns else 0

    with col1:
        st.metric("💰 Revenue", f"${revenue:,.2f}")
        st.metric("📦 Orders", f"{orders:,}")

    with col2:
        st.metric("👥 Customers", f"{customers:,}")
        st.metric("🛍️ AOV", f"${aov:,.2f}")

    with col3:
        conv_rate = (customers / orders * 100) if orders > 0 else 0
        return_rate = (filtered_df['returned'].sum() / orders * 100) if orders > 0 and 'returned' in filtered_df.columns else 0
        st.metric("📊 Conversion", f"{conv_rate:.2f}%")
        st.metric("↩️ Returns", f"{return_rate:.2f}%")

    with col4:
        satisfaction = filtered_df['satisfaction_rating'].mean() if 'satisfaction_rating' in filtered_df.columns else 0
        roi = filtered_df['roi'].mean() if 'roi' in filtered_df.columns else 0
        st.metric("⭐ Satisfaction", f"{satisfaction:.2f}/5")
        st.metric("💹 ROI", f"{roi:.2f}%")

    st.markdown("---")

    # ========== CHARTS ==========
    st.header("📊 Visualizations")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue", "👥 Customers", "🎯 Marketing", "📦 Operations"])

    with tab1:
        # Monthly trend
        if 'month_date' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Monthly Revenue Trend")
            monthly = filtered_df.groupby('month_date')['net_revenue'].sum().reset_index()
            fig = px.line(monthly, x='month_date', y='net_revenue', markers=True)
            fig.update_traces(line_color='#2ecc71', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Revenue by category
        col1, col2 = st.columns(2)

        with col1:
            if 'category' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Revenue by Category")
                cat_rev = filtered_df.groupby('category')['net_revenue'].sum().reset_index()
                cat_rev = cat_rev.sort_values('net_revenue', ascending=False)
                fig = px.bar(cat_rev, x='category', y='net_revenue', color='net_revenue',
                           color_continuous_scale='Greens')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'region' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Revenue by Region")
                region_rev = filtered_df.groupby('region')['net_revenue'].sum().reset_index()
                fig = px.pie(region_rev, values='net_revenue', names='region', hole=0.4)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            if 'customer_segment' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Revenue by Segment")
                seg_rev = filtered_df.groupby('customer_segment')['net_revenue'].sum().reset_index()
                fig = px.pie(seg_rev, values='net_revenue', names='customer_segment')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'customer_segment' in filtered_df.columns and 'customer_lifetime_value' in filtered_df.columns:
                st.subheader("CLV by Segment")
                clv = filtered_df.groupby('customer_segment')['customer_lifetime_value'].mean().reset_index()
                fig = px.bar(clv, x='customer_segment', y='customer_lifetime_value',
                           color='customer_lifetime_value', color_continuous_scale='Blues')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if 'marketing_channel' in filtered_df.columns and 'roi' in filtered_df.columns:
            st.subheader("ROI by Marketing Channel")
            roi_ch = filtered_df.groupby('marketing_channel')['roi'].mean().reset_index()
            roi_ch = roi_ch.sort_values('roi', ascending=False)
            fig = px.bar(roi_ch, x='marketing_channel', y='roi', color='roi',
                       color_continuous_scale='RdYlGn')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if 'device_type' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Revenue by Device")
                device = filtered_df.groupby('device_type')['net_revenue'].sum().reset_index()
                fig = px.pie(device, values='net_revenue', names='device_type', hole=0.4)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'marketing_campaign' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Campaign Performance")
                camp = filtered_df.groupby('marketing_campaign')['net_revenue'].sum().reset_index()
                camp = camp.sort_values('net_revenue', ascending=False).head(10)
                fig = px.bar(camp, x='marketing_campaign', y='net_revenue',
                           color='net_revenue', color_continuous_scale='Viridis')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            if 'payment_method' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Payment Methods")
                payment = filtered_df.groupby('payment_method')['net_revenue'].sum().reset_index()
                fig = px.bar(payment, x='payment_method', y='net_revenue',
                           color='net_revenue', color_continuous_scale='Purples')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'shipping_method' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
                st.subheader("Shipping Performance")
                shipping = filtered_df.groupby('shipping_method')['net_revenue'].sum().reset_index()
                fig = px.bar(shipping, x='shipping_method', y='net_revenue',
                           color='net_revenue', color_continuous_scale='Oranges')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

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
    - **13 Visualization Types**: Charts covering all business aspects
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

    ```bash
    streamlit run app.py
    ```

    ### 📧 Support

    For issues or suggestions, check that:
    - `cleaned_data.csv` exists in the app directory
    - All required columns are present in the CSV
    - Libraries are installed correctly

    ---

    **Version**: 1.0.0  
    **Last Updated**: December 2025  
    **Built with** ❤️ **using Streamlit**
    """)

    st.markdown("---")

    # System info
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
