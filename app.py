
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
    conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0

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
        st.metric("📊 Conversion Rate", f"{conversion_rate:.2f}%")
        st.metric("↩️ Return Rate", f"{return_rate:.2f}%")

    with col4:
        st.metric("⭐ Satisfaction", f"{avg_satisfaction:.2f}/5")
        st.metric("💹 Avg ROI", f"{avg_roi:.2f}%")

    st.markdown("---")

    # ========== CHARTS FROM NOTEBOOK ==========
    st.header("📊 Data Visualizations")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🎯 Marketing", "👥 Customers", "📦 Performance"])

    # ========== TAB 1: TRENDS ==========
    with tab1:
        # Chart 1: Monthly Revenue Trend (من الـ Notebook)
        # AHMED
# -------------------------------
# LINE CHART: Monthly Revenue by Channel
# -------------------------------

fig_revenue_trend = px.line(
    monthly_channel,
    x='month',
    y='revenue',
    color='channel',
    markers=True,
    title='Monthly Revenue Trends by Marketing Channel'
)

fig_revenue_trend.update_layout(
    plot_bgcolor="#040D2F",
    paper_bgcolor="#040D2F",
    font_color="#D9D9D9",
    title_font_size=22,
    title_x=0.5,
    height=500,
    xaxis_title="Month",
    yaxis_title="Revenue",
    legend_title="Channel",
    xaxis=dict(tickangle=45)
)

fig_revenue_trend.show()
            # Same styling as notebook
            fig.update_traces(
                line=dict(color='#3647F5', width=3),
                marker=dict(size=8, color='#FF9F0D')
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

        # Chart 2: Monthly Conversions Trend (من الـ Notebook)
        if 'month_date' in filtered_df.columns and 'customer_id' in filtered_df.columns:
            st.subheader("Overall Monthly Conversions Trend")

            monthly_conversions = filtered_df.groupby('month_date').agg({
                'customer_id': 'nunique'
            }).reset_index()
            monthly_conversions.columns = ['month', 'totalconversions']
            monthly_conversions = monthly_conversions.sort_values('month')

            fig = px.line(
                monthly_conversions,
                x='month',
                y='totalconversions',
                markers=True,
                title='Overall Monthly Conversions Trend'
            )

            # Same styling as notebook
            fig.update_traces(
                line=dict(color='#FF9F0D', width=3),
                marker=dict(size=8, color='#3647F5')
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

        # Chart 3: Monthly Revenue by Channel (من الـ Notebook)
        if 'month_date' in filtered_df.columns and 'marketing_channel' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Monthly Revenue by Channel")

            monthly_channel = filtered_df.groupby(['month_date', 'marketing_channel']).agg({
                'net_revenue': 'sum'
            }).reset_index()
            monthly_channel.columns = ['month', 'channel', 'revenue']

            fig = px.line(
                monthly_channel,
                x='month',
                y='revenue',
                color='channel',
                markers=True,
                title='Monthly Revenue by Channel'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

    # ========== TAB 2: MARKETING ==========
    with tab2:
        # Chart 4: ROI by Marketing Channel (من الـ Notebook)
        if 'marketing_channel' in filtered_df.columns and 'roi' in filtered_df.columns:
            st.subheader("ROI by Marketing Channel")

            roi_channel = filtered_df.groupby('marketing_channel').agg({
                'roi': 'mean'
            }).reset_index()
            roi_channel = roi_channel.sort_values('roi', ascending=False)

            fig = px.bar(
                roi_channel,
                x='marketing_channel',
                y='roi',
                color='roi',
                color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D'],
                title='ROI by Marketing Channel'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 5: Conversion Rate by Channel (من الـ Notebook)
        if 'marketing_channel' in filtered_df.columns and 'customer_id' in filtered_df.columns and 'quantity' in filtered_df.columns:
            st.subheader("Conversion Rate by Channel")

            # Calculate conversion rate same as notebook
            filtered_df['visits'] = filtered_df['quantity'] * 100

            conversion_by_channel = filtered_df.groupby('marketing_channel').agg({
                'customer_id': 'nunique',
                'visits': 'sum'
            }).reset_index()

            conversion_by_channel['conversion_rate'] = (
                conversion_by_channel['customer_id'] / conversion_by_channel['visits'] * 100
            ).round(3)

            conversion_by_channel = conversion_by_channel.sort_values('conversion_rate', ascending=False)

            fig = px.bar(
                conversion_by_channel,
                x='marketing_channel',
                y='conversion_rate',
                color='conversion_rate',
                color_continuous_scale=['#FF9F0D', '#D9D9D9'],
                title='Conversion Rate by Channel'
            )

            fig.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                xaxis_title="Marketing Channel",
                yaxis_title="Conversion Rate (%)"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 6: Channel Efficiency Ranking (من الـ Notebook)
        if 'marketing_channel' in filtered_df.columns and 'cpc' in filtered_df.columns:
            st.subheader("Channel Efficiency Ranking")

            # CPC by channel
            cpc_by_channel = filtered_df.groupby('marketing_channel').agg({
                'cpc': 'mean'
            }).reset_index()
            cpc_by_channel.columns = ['Channel', 'AvgCPC']

            # Merge with conversion rate
            if 'conversion_rate' in conversion_by_channel.columns:
                cpc_by_channel = cpc_by_channel.merge(
                    conversion_by_channel[['marketing_channel', 'conversion_rate']],
                    left_on='Channel',
                    right_on='marketing_channel',
                    how='left'
                )

                # Calculate efficiency score same as notebook
                cpc_by_channel['EfficiencyScore'] = (
                    (1 / cpc_by_channel['AvgCPC'] * 100) + 
                    (cpc_by_channel['conversion_rate'] * 10)
                ).round(2)

                cpc_by_channel = cpc_by_channel.sort_values('EfficiencyScore', ascending=True)

                fig = px.bar(
                    cpc_by_channel,
                    x='EfficiencyScore',
                    y='Channel',
                    orientation='h',
                    color='EfficiencyScore',
                    color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D'],
                    title='Channel Efficiency Ranking'
                )

                fig.update_traces(
                    marker=dict(line=dict(width=1.5, color='#D9D9D9'))
                )

                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f5f5',
                    height=450
                )

                st.plotly_chart(fig, use_container_width=True)

        # Chart 7: Spend vs Revenue Analysis (من الـ Notebook)
        if 'marketing_channel' in filtered_df.columns and 'marketing_spend' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("ROI Analysis: Spend vs Revenue by Channel")

            spend_revenue = filtered_df.groupby('marketing_channel').agg({
                'marketing_spend': 'sum',
                'net_revenue': 'sum'
            }).reset_index()

            spend_revenue.columns = ['Channel', 'TotalSpend', 'TotalRevenue']
            spend_revenue['RevenuetoSpendRatio'] = (
                spend_revenue['TotalRevenue'] / spend_revenue['TotalSpend']
            ).round(2)

            fig = px.scatter(
                spend_revenue,
                x='TotalSpend',
                y='TotalRevenue',
                size='RevenuetoSpendRatio',
                color='RevenuetoSpendRatio',
                hover_name='Channel',
                text='Channel',
                title='ROI Analysis: Spend vs Revenue by Channel',
                size_max=60,
                color_continuous_scale=['#FF9F0D', '#3647F5', '#D9D9D9']
            )

            fig.update_traces(
                textposition='top center',
                textfont=dict(size=12, color='#D9D9D9'),
                marker=dict(line=dict(width=2, color='#D9D9D9'), opacity=0.85)
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=500,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 8: Cost Per Conversion (من الـ Notebook)
        if 'marketing_channel' in filtered_df.columns and 'marketing_spend' in filtered_df.columns and 'customer_id' in filtered_df.columns:
            st.subheader("Cost Per Conversion by Channel")

            spend_conversions = filtered_df.groupby('marketing_channel').agg({
                'marketing_spend': 'sum',
                'customer_id': 'nunique'
            }).reset_index()

            spend_conversions.columns = ['Channel', 'TotalSpend', 'TotalConversions']
            spend_conversions['SpendPerConversion'] = (
                spend_conversions['TotalSpend'] / spend_conversions['TotalConversions']
            ).round(2)

            spend_conversions = spend_conversions.sort_values('SpendPerConversion')

            fig = px.bar(
                spend_conversions,
                x='Channel',
                y='SpendPerConversion',
                color='SpendPerConversion',
                color_continuous_scale=['#3647F5', '#D9D9D9', '#FF9F0D'],
                title='Cost Per Conversion by Channel'
            )

            fig.update_traces(
                marker=dict(line=dict(width=1.5, color='#D9D9D9'))
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

    # ========== TAB 3: CUSTOMERS ==========
    with tab3:
        # Chart 9: Revenue by Customer Segment (من الـ Notebook)
        if 'customer_segment' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Revenue Distribution by Customer Segment")

            segment_revenue = filtered_df.groupby('customer_segment').agg({
                'net_revenue': 'sum'
            }).reset_index()

            fig = px.pie(
                segment_revenue,
                values='net_revenue',
                names='customer_segment',
                title='Revenue by Customer Segment'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5'
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 10: CLV & Retention by Segment (من الـ Notebook)
        if 'customer_segment' in filtered_df.columns and 'customer_lifetime_value' in filtered_df.columns and 'retention_score' in filtered_df.columns:
            st.subheader("Customer Lifetime Value & Retention by Segment")

            clv_data = filtered_df.groupby('customer_segment').agg({
                'customer_lifetime_value': 'mean',
                'retention_score': 'mean'
            }).reset_index()

            fig = go.Figure(data=[
                go.Bar(
                    name='CLV ($)',
                    x=clv_data['customer_segment'],
                    y=clv_data['customer_lifetime_value'],
                    marker_color='#3647F5'
                ),
                go.Bar(
                    name='Retention Score',
                    x=clv_data['customer_segment'],
                    y=clv_data['retention_score'],
                    marker_color='#FF9F0D'
                )
            ])

            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450,
                title='CLV & Retention by Segment'
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 11: Revenue by Region (من الـ Notebook)
        if 'region' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Revenue by Region")

            region_revenue = filtered_df.groupby('region').agg({
                'net_revenue': 'sum'
            }).reset_index()

            fig = px.pie(
                region_revenue,
                values='net_revenue',
                names='region',
                title='Revenue Distribution by Region',
                hole=0.4
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5'
            )

            st.plotly_chart(fig, use_container_width=True)

    # ========== TAB 4: PERFORMANCE ==========
    with tab4:
        # Chart 12: Revenue by Category (من الـ Notebook)
        if 'category' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Net Revenue by Product Category")

            category_revenue = filtered_df.groupby('category').agg({
                'net_revenue': 'sum'
            }).reset_index()
            category_revenue = category_revenue.sort_values('net_revenue', ascending=False)

            fig = px.bar(
                category_revenue,
                x='category',
                y='net_revenue',
                color='net_revenue',
                color_continuous_scale='Greens',
                title='Net Revenue by Product Category'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 13: Payment Method Performance (من الـ Notebook)
        if 'payment_method' in filtered_df.columns and 'net_revenue' in filtered_df.columns:
            st.subheader("Payment Method Performance")

            payment_data = filtered_df.groupby('payment_method').agg({
                'net_revenue': 'sum',
                'order_id': 'count'
            }).reset_index()
            payment_data.columns = ['payment_method', 'Revenue', 'Orders']

            fig = go.Figure(data=[
                go.Bar(
                    name='Revenue ($)',
                    x=payment_data['payment_method'],
                    y=payment_data['Revenue'],
                    marker_color='#3647F5'
                ),
                go.Bar(
                    name='Orders',
                    x=payment_data['payment_method'],
                    y=payment_data['Orders'],
                    marker_color='#FF9F0D'
                )
            ])

            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 14: Shipping Method Performance (من الـ Notebook)
        if 'shipping_method' in filtered_df.columns and 'net_revenue' in filtered_df.columns and 'satisfaction_rating' in filtered_df.columns:
            st.subheader("Shipping Method Performance")

            shipping_data = filtered_df.groupby('shipping_method').agg({
                'net_revenue': 'sum',
                'satisfaction_rating': 'mean'
            }).reset_index()

            fig = go.Figure(data=[
                go.Bar(
                    name='Revenue ($)',
                    x=shipping_data['shipping_method'],
                    y=shipping_data['net_revenue'],
                    marker_color='#3647F5'
                ),
                go.Bar(
                    name='Satisfaction',
                    x=shipping_data['shipping_method'],
                    y=shipping_data['satisfaction_rating'] * 1000,
                    marker_color='#FF9F0D'
                )
            ])

            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

        # Chart 15: Satisfaction Impact on Revenue & Returns (من الـ Notebook)
        if 'satisfaction_rating' in filtered_df.columns and 'net_revenue' in filtered_df.columns and 'returned' in filtered_df.columns:
            st.subheader("Satisfaction Rating Impact on Revenue & Returns")

            satisfaction_data = filtered_df.groupby('satisfaction_rating').agg({
                'net_revenue': 'mean',
                'returned': 'sum'
            }).reset_index()

            fig = px.scatter(
                satisfaction_data,
                x='satisfaction_rating',
                y='net_revenue',
                size='returned',
                color='returned',
                labels={
                    'net_revenue': 'Avg Revenue ($)',
                    'satisfaction_rating': 'Rating',
                    'returned': 'Returns'
                },
                color_continuous_scale='Reds',
                title='Satisfaction Impact on Revenue & Returns'
            )

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                height=450
            )

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

    ```bash
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
