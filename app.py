import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time

# =============================================================================
# THEME MANAGEMENT
# =============================================================================
def get_theme_css(theme_mode):
    """إرجاع CSS حسب وضع السمة"""
    
    # إعدادات الألوان للوضع النهاري (لايت مود)
    light_mode = {
        "primary_blue": "#1f77b4",
        "secondary_green": "#2ecc71",
        "bg_color": "#ffffff",
        "panel_color": "#f8f9fa",
        "text_color": "#333333",
        "accent_cyan": "#00bcd4",
        "warning_orange": "#ff9800",
        "border_color": "#e0e0e0",
        "shadow_color": "rgba(0, 0, 0, 0.1)"
    }
    
    # إعدادات الألوان للوضع الليلي (داكن)
    dark_mode = {
        "primary_blue": "#1f77b4",
        "secondary_green": "#2ecc71",
        "bg_color": "#0f1419",
        "panel_color": "#1a1f2e",
        "text_color": "#f5f5f5",
        "accent_cyan": "#00d9ff",
        "warning_orange": "#ff9800",
        "border_color": "#2a3240",
        "shadow_color": "rgba(0, 0, 0, 0.3)"
    }
    
    # اختيار السمة بناءً على الوضع
    colors = light_mode if theme_mode == "light" else dark_mode
    
    return f"""
    <style>
    :root {{
      --primary-blue: {colors['primary_blue']};
      --secondary-green: {colors['secondary_green']};
      --bg-color: {colors['bg_color']};
      --panel-color: {colors['panel_color']};
      --text-color: {colors['text_color']};
      --accent-cyan: {colors['accent_cyan']};
      --warning-orange: {colors['warning_orange']};
      --border-color: {colors['border_color']};
      --shadow-color: {colors['shadow_color']};
    }}

    html, body, .stApp {{
      background: {colors['bg_color']} !important;
      color: {colors['text_color']} !important;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
      color: {colors['accent_cyan']} !important;
      font-weight: 700 !important;
    }}

    section[data-testid="stSidebar"] {{
      background: {colors['panel_color']} !important;
      border-right: 2px solid {colors['primary_blue']};
    }}

    section[data-testid="stSidebar"] * {{
      color: {colors['text_color']} !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stDateInput label {{
      color: {colors['accent_cyan']} !important;
      font-weight: 600 !important;
    }}

    div.stButton > button {{
      background: linear-gradient(135deg, {colors['primary_blue']} 0%, {colors['secondary_green']} 100%) !important;
      color: white !important;
      border: none !important;
      font-weight: 700 !important;
      padding: 0.6rem 2rem !important;
      border-radius: 8px !important;
      box-shadow: 0 4px 15px rgba(31, 119, 180, 0.4) !important;
      transition: all 0.3s ease !important;
    }}

    div.stButton > button:hover {{
      transform: translateY(-2px) !important;
      box-shadow: 0 6px 20px rgba(31, 119, 180, 0.6) !important;
    }}

    [data-testid="stMetricValue"] {{
      color: {colors['secondary_green']} !important;
      font-size: 2rem !important;
      font-weight: 700 !important;
    }}

    [data-testid="stMetricLabel"] {{
      color: {colors['accent_cyan']} !important;
      font-weight: 600 !important;
    }}

    div[data-testid="stExpander"] {{
      background-color: {colors['panel_color']} !important;
      border: 1px solid {colors['border_color']} !important;
      border-radius: 10px !important;
    }}

    .stDataFrame {{
      background-color: {colors['panel_color']} !important;
      border: 1px solid {colors['border_color']} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
      gap: 8px;
      background-color: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
      background-color: {colors['panel_color']};
      border-radius: 8px 8px 0 0;
      color: {colors['text_color']};
      border: 1px solid {colors['border_color']};
      padding: 10px 20px;
    }}

    .stTabs [aria-selected="true"] {{
      background: linear-gradient(135deg, {colors['primary_blue']} 0%, {colors['secondary_green']} 100%);
      color: white;
    }}

    .stAlert {{
      background-color: {colors['panel_color']} !important;
      border-left: 4px solid {colors['accent_cyan']} !important;
    }}

    a {{
      color: {colors['accent_cyan']} !important;
      text-decoration: none !important;
    }}

    a:hover {{
      color: {colors['secondary_green']} !important;
    }}

    hr {{
      border-color: {colors['border_color']} !important;
      opacity: 0.5 !important;
    }}

    .stDownloadButton > button {{
      background-color: {colors['secondary_green']} !important;
      color: white !important;
    }}

    .metric-card {{
      background: linear-gradient(135deg, {colors['panel_color']} 0%, rgba(31, 119, 180, 0.1) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      border: 1px solid {colors['border_color']};
      box-shadow: 0 4px 15px {colors['shadow_color']};
      text-align: center;
      margin-bottom: 1rem;
    }}

    .metric-value {{
      font-size: 2.5rem;
      font-weight: 700;
      color: {colors['secondary_green']};
      margin: 0.5rem 0;
    }}

    .metric-label {{
      font-size: 1rem;
      color: {colors['accent_cyan']};
      font-weight: 600;
    }}

    .footer {{
      text-align: center;
      padding: 2rem;
      color: {colors['text_color']};
      opacity: 0.7;
      border-top: 1px solid {colors['border_color']};
      margin-top: 3rem;
    }}

    /* Chart styling */
    .js-plotly-plot .plotly .modebar {{
      background: {colors['panel_color']} !important;
    }}

    .theme-status {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 5px 10px;
      background: {colors['panel_color']};
      border-radius: 20px;
      border: 1px solid {colors['border_color']};
      margin: 5px 0;
    }}

    .theme-status-icon {{
      font-size: 20px;
    }}
    </style>
    """

def get_auto_theme():
    """تحديد الوضع التلقائي بناءً على الوقت"""
    current_hour = datetime.now().hour
    
    # الوضع النهاري من 6 صباحاً إلى 6 مساءً
    if 6 <= current_hour < 18:
        return "light"
    else:
        return "dark"

def set_plotly_theme(theme_mode):
    """تعيين سمة Plotly حسب الوضع"""
    if theme_mode == "light":
        return {
            "paper_bgcolor": "#f8f9fa",
            "plot_bgcolor": "#ffffff",
            "font_color": "#333333",
            "gridcolor": "#e0e0e0"
        }
    else:
        return {
            "paper_bgcolor": "#1a1f2e",
            "plot_bgcolor": "#0f1419",
            "font_color": "#f5f5f5",
            "gridcolor": "#2a3240"
        }

# =============================================================================
# STREAMLIT APP CONFIG
# =============================================================================
st.set_page_config(
    page_title="📊 E-commerce Analytics Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME SELECTION IN SIDEBAR
# =============================================================================
with st.sidebar:
    st.title("🎨 Theme Settings")
    
    # Theme selection
    theme_mode = st.radio(
        "Select Theme Mode",
        ["🌙 Dark Mode", "☀️ Light Mode", "🔄 Auto Mode"],
        index=0,
        key="theme_mode"
    )
    
    # Extract theme from selection
    if "Light" in theme_mode:
        current_theme = "light"
        st.success("☀️ Light Mode Active")
    elif "Dark" in theme_mode:
        current_theme = "dark"
        st.info("🌙 Dark Mode Active")
    else:  # Auto Mode
        current_theme = get_auto_theme()
        if current_theme == "light":
            st.success("🔆 Auto Mode: Daylight Hours (Light)")
        else:
            st.success("🌙 Auto Mode: Night Hours (Dark)")
    
    # Display current time
    current_time = datetime.now().strftime("%I:%M %p")
    st.caption(f"🕐 Current Time: {current_time}")
    
    st.markdown("---")

# Apply theme CSS
st.markdown(get_theme_css(current_theme), unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION (المتبقي من السايدبار)
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

# Get plotly theme settings
plotly_theme = set_plotly_theme(current_theme)

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
# UPDATE ALL CHART FUNCTIONS TO USE DYNAMIC THEME
# =============================================================================
def create_chart_with_theme(fig, title=""):
    """تحديث جميع الرسوم البيانية بالسمة المختارة"""
    fig.update_layout(
        title=title,
        paper_bgcolor=plotly_theme["paper_bgcolor"],
        plot_bgcolor=plotly_theme["plot_bgcolor"],
        font_color=plotly_theme["font_color"],
        xaxis=dict(
            gridcolor=plotly_theme["gridcolor"],
            linecolor=plotly_theme["gridcolor"]
        ),
        yaxis=dict(
            gridcolor=plotly_theme["gridcolor"],
            linecolor=plotly_theme["gridcolor"]
        ),
        legend=dict(
            bgcolor=plotly_theme["paper_bgcolor"],
            bordercolor=plotly_theme["gridcolor"]
        )
    )
    return fig

# =============================================================================
# HOME PAGE (مع التحديثات)
# =============================================================================
if page == "🏠 Home":
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🛒 E-commerce Analytics Pro</h1>
            <p style='font-size: 1.3rem; margin-top: 0.5rem;'>
                Advanced Business Intelligence Dashboard
            </p>
            <div class='theme-status'>
                <span class='theme-status-icon'>{"☀️" if current_theme == "light" else "🌙"}</span>
                <span>Current Theme: {"Light Mode" if current_theme == "light" else "Dark Mode"}</span>
            </div>
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
                ### 🎨 Smart Themes
                - Light & Dark modes
                - Auto theme based on time
                - Eye-friendly design
                - Customizable colors
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
# ANALYTICS DASHBOARD (مع تحديث الرسوم البيانية)
# =============================================================================
elif page == "📊 Analytics Dashboard":
    st.title("📊 Analytics Dashboard")
    st.markdown(f"Interactive visualizations • Current Theme: **{'☀️ Light' if current_theme == 'light' else '🌙 Dark'}**")

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

    st.markdown("---")

    # ========== CHARTS FROM NOTEBOOK ==========
    st.header("📊 Data Visualizations")

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🎯 Marketing", "📦 Performance"])

    # ========== TAB 1: TRENDS (مع السمة الديناميكية) ==========
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
            
            fig_revenue_trend = create_chart_with_theme(fig_revenue_trend)
            fig_revenue_trend.update_layout(
                height=500,
                xaxis_title="Month",
                yaxis_title="Revenue",
                legend_title="Channel",
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_revenue_trend, use_container_width=True)

    # ========== TAB 2: MARKETING (مع السمة الديناميكية) ==========
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
                
                fig_rev = px.scatter(
                    channel_perf,
                    x=channel_perf.index,
                    y="total_revenue",
                    title="Total Revenue per Marketing Channel",
                    color_discrete_sequence=["#3647F5"],
                    text="total_revenue"
                )
                
                fig_rev.update_traces(
                    marker=dict(size=25),
                    textposition='top center',
                    texttemplate='%{text:.2s}'
                )
                
                fig_rev = create_chart_with_theme(fig_rev)
                fig_rev.update_layout(
                    height=450,
                    margin=dict(t=60)
                )
                
                st.plotly_chart(fig_rev, use_container_width=True)

    # ========== TAB 3: PERFORMANCE (مع السمة الديناميكية) ==========
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
            
            fig_revenue_order = create_chart_with_theme(fig_revenue_order)
            fig_revenue_order.update_layout(
                height=450,
                xaxis_title="Revenue Per Order ($)",
                yaxis_title="Marketing Channel"
            )
            
            st.plotly_chart(fig_revenue_order, use_container_width=True)

# =============================================================================
# DATA EXPLORER
# =============================================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown(f"Browse and filter your data • Current Theme: **{'☀️ Light' if current_theme == 'light' else '🌙 Dark'}**")

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

    ### 🎨 Smart Theme Features

    - **Light Mode**: Eye-friendly daytime theme
    - **Dark Mode**: Comfortable night viewing
    - **Auto Mode**: Automatically switches based on time
    - **Dynamic Charts**: All visualizations adapt to theme

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
    - **Styling**: Dynamic CSS themes

    ### 📝 How to Use

    1. **Select Theme**: Choose from Light/Dark/Auto modes
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

    **Version**: 2.0.0 (with Theme Support)  
    **Last Updated**: December 2025  
    **Current Theme**: {'☀️ Light' if current_theme == 'light' else '🌙 Dark'} Mode
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
        <p>© 2025 | Current Theme: {'☀️ Light' if current_theme == 'light' else '🌙 Dark'} Mode</p>
    </div>
""", unsafe_allow_html=True)
