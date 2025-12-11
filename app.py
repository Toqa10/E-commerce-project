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

    # ========== KPIs FROM NOTEBOOK ==========
    st.header("📈 Key Performance Indicators")

    # Calculate KPIs exactly as in notebook
    total_revenue = filtered_df['net_revenue'].sum() if 'net_revenue' in filtered_df.columns else 0
    total_customers = filtered_df['customer_id'].nunique() if 'customer_id' in filtered_df.columns else 0
    total_orders = len(filtered_df)
    avg_order_value = filtered_df['final_amount'].mean() if 'final_amount' in filtered_df.columns else 0

    # Conversion Rate (same as notebook)
    conversion_rate = (total_orders / total_customers) if total_customers > 0 else 0

    # Return Rate
    return_rate = (filtered_df['returned'].sum() / total_orders * 100) if total_orders > 0 and 'returned' in filtered_df.columns else 0

    # Satisfaction
    avg_satisfaction = filtered_df['satisfaction_rating'].mean() if 'satisfaction_rating' in filtered_df.columns else 0

    # ROI (same as notebook calculation)
    if 'roi' in filtered_df.columns:
        avg_roi = filtered_df['roi'].mean()
    else:
        avg_roi = 0

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
        st.metric("📦 Total Orders", f"{total_orders:,}")

    with col2:
        st.metric("👥 Total Customers", f"{total_customers:,}")
        st.metric("🛍️ Avg Order Value", f"${avg_order_value:,.2f}")

    with col3:
        st.metric("📊 Conversion Rate", f"{conversion_rate:.2f}")
        st.metric("↩️ Return Rate", f"{return_rate:.2f}%")

    with col4:
        st.metric("⭐ Satisfaction", f"{avg_satisfaction:.2f}/5")
        st.metric("💹 Avg ROI", f"{avg_roi:.2f}")

    st.markdown("---")

    # ========== CHARTS FROM NOTEBOOK ==========
    st.header("📊 Data Visualizations")

    tab1, tab2, tab3 = st.tabs(["📈 Time Trends", "🎯 Marketing Performance", "👥 Customers & Products"])

    # ========== TAB 1: TIME TRENDS ==========
    with tab1:
        st.subheader("📅 Monthly Analysis")
        
        # Chart 1: Overall Monthly Revenue Trend
        if 'month_date' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            monthly_total = filtered_df.groupby('month_date').agg({
                'net_revenue': 'sum',
                'customer_id': 'nunique'
            }).reset_index()
            monthly_total.columns = ['month', 'totalrevenue', 'totalconversions']

            fig = px.line(
                monthly_total,
                x='month',
                y='totalrevenue',
                markers=True,
                title='Overall Monthly Revenue Trend'
            )

            fig.update_traces(
                line=dict(color='#FF9F0D', width=3),
                marker=dict(size=10, color='#3647F5')
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Month",
                yaxis_title="Total Revenue"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 2: Overall Monthly Conversions Trend
        if 'month_date' in filtered_df.columns and 'customer_id' in filtered_df.columns:
            fig = px.line(
                monthly_total,
                x='month',
                y='totalconversions',
                markers=True,
                title='Overall Monthly Conversions Trend'
            )

            fig.update_traces(
                line=dict(color='#3647F5', width=3),
                marker=dict(size=10, color='#FF9F0D')
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Month",
                yaxis_title="Total Conversions"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 3: Monthly Revenue by Channel
        if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns:
            filtered_df['month_str'] = filtered_df['month_date'].dt.to_period('M').astype(str)
            
            monthly_channel = filtered_df.groupby(['month_str', 'marketing_channel']).agg({
                'net_revenue': 'sum',
                'customer_id': 'nunique'
            }).reset_index()
            monthly_channel.columns = ['month', 'channel', 'revenue', 'conversions']

            fig = px.line(
                monthly_channel,
                x='month',
                y='revenue',
                color='channel',
                markers=True,
                title='Monthly Revenue Trends by Marketing Channel'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                xaxis=dict(tickangle=45)
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 4: Monthly Conversions by Channel
        if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns:
            fig = px.line(
                monthly_channel,
                x='month',
                y='conversions',
                color='channel',
                markers=True,
                title='Monthly Conversions Trends by Marketing Channel'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                xaxis=dict(tickangle=45),
                yaxis_title="Conversions (Unique Customers)",
                legend_title="Channel"
            )

            st.plotly_chart(fig, use_container_width=True)

    # ========== TAB 2: MARKETING PERFORMANCE ==========
    with tab2:
        st.subheader("🎯 Channel Performance Analysis")
        
        # Prepare channel performance data
        if 'marketing_channel' in filtered_df.columns:
            channel_perf = filtered_df.groupby('marketing_channel').agg({
                'discount_percent': 'sum',
                'final_amount': 'sum',
                'customer_id': 'nunique',
                'roi': 'mean'
            }).reset_index()
            channel_perf.columns = ['marketing_channel', 'total_spend', 'total_revenue', 'total_conversions', 'avg_roi']
            channel_perf_sorted = channel_perf.sort_values(by='avg_roi', ascending=True)

            # Chart 5: Total Revenue per Channel (Lollipop-style)
            st.markdown("#### 💰 Total Revenue by Marketing Channel")
            
            fig = go.Figure()
            
            # Add scatter for circles
            fig.add_trace(go.Scatter(
                x=channel_perf_sorted['marketing_channel'],
                y=channel_perf_sorted['total_revenue'],
                mode='markers+text',
                marker=dict(
                    color='#3647F5',
                    size=25
                ),
                text=[f"${val/1000:.0f}K" if val < 1000000 else f"${val/1000000:.1f}M" for val in channel_perf_sorted['total_revenue']],
                textposition='
