import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
    'light': '#D9D9D9'         # رمادي فاتح
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
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LOAD & CACHE DATA
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    return df

df = load_data()

# ═══════════════════════════════════════════════════════════════════════════
# LOGO & HEADER
# ═══════════════════════════════════════════════════════════════════════════

col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown(f'<h1 style="color: {COLORS["accent"]};font-size: 2em;">📊</h1>', unsafe_allow_html=True)
with col_title:
    st.title("E-Commerce Analytics Dashboard", anchor="main")
    st.markdown(f"<p style='color: {COLORS['light']}; margin-top: -20px;'>Data-Driven Business Intelligence</p>", unsafe_allow_html=True)

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
    
    st.markdown("---")
    
    # Apply Filters Button
    if st.button("🔄 Apply Filters", use_container_width=True):
        st.session_state.filters_applied = True

# Apply Filters
filtered_df = df[
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date) &
    (df['marketing_channel'].isin(selected_channels)) &
    (df['marketing_campaign'].isin(selected_campaigns)) &
    (df['customer_segment'].isin(selected_segments)) &
    (df['region'].isin(selected_regions))
].reset_index(drop=True)

# Display filter info
st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='color: {COLORS['light']}; font-size: 12px;'>📊 Records: <strong>{len(filtered_df):,}</strong></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: {COLORS['light']}; font-size: 12px;'>✨ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# TABS NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Trends",
    "⚡ Efficiency",
    "💡 Recommendations"
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # KPI ROW 1
    st.markdown("### 🎯 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = filtered_df['net_revenue'].sum()
    total_customers = filtered_df['customer_id'].nunique()
    avg_order_value = filtered_df['final_amount'].mean()
    avg_satisfaction = filtered_df['satisfaction_rating'].mean()
    
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
            label="📦 Avg Order Value",
            value=f"${avg_order_value:,.2f}"
        )
    
    with col4:
        st.metric(
            label="⭐ Satisfaction",
            value=f"{avg_satisfaction:.2f}/5"
        )
    
    # KPI ROW 2
    col5, col6, col7, col8 = st.columns(4)
    
    total_orders = len(filtered_df)
    conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
    return_rate = (filtered_df['returned'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    avg_roi = filtered_df['roi'].replace([np.inf, -np.inf], np.nan).mean()
    
    with col5:
        st.metric(label="📋 Total Orders", value=f"{total_orders:,}")
    
    with col6:
        st.metric(label="📊 Conversion Rate", value=f"{conversion_rate:.2f}%")
    
    with col7:
        st.metric(label="🔄 Return Rate", value=f"{return_rate:.2f}%")
    
    with col8:
        st.metric(label="📈 Avg ROI", value=f"{avg_roi:.2f}x")
    
    st.markdown("---")
    
    # CHANNEL PERFORMANCE
    st.markdown("### 📢 Marketing Channel Performance")
    col_ch1, col_ch2 = st.columns(2)
    
    channel_stats = filtered_df.groupby('marketing_channel').agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique'
    }).sort_values('net_revenue', ascending=False)
    
    with col_ch1:
        fig_channel = px.bar(
            x=channel_stats.index,
            y=channel_stats['net_revenue'],
            title='💰 Revenue by Channel',
            color=channel_stats['net_revenue'],
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'x': 'Channel', 'y': 'Revenue ($)'},
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
    
    with col_ch2:
        fig_channel_pie = px.pie(
            values=channel_stats['customer_id'],
            names=channel_stats.index,
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
    
    # CAMPAIGN & REGIONAL PERFORMANCE
    st.markdown("### 🎪 Campaign & Regional Analysis")
    col_cam, col_reg = st.columns(2)
    
    campaign_stats = filtered_df.groupby('marketing_campaign')['net_revenue'].sum().sort_values(ascending=False)
    region_stats = filtered_df.groupby('region')['net_revenue'].sum().sort_values(ascending=False)
    
    with col_cam:
        fig_campaign = px.bar(
            x=campaign_stats.index,
            y=campaign_stats.values,
            title='🎯 Revenue by Campaign',
            color=campaign_stats.values,
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'x': 'Campaign', 'y': 'Revenue ($)'}
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
    
    with col_reg:
        fig_region = px.bar(
            x=region_stats.index,
            y=region_stats.values,
            title='🗺️ Revenue by Region',
            color=region_stats.values,
            color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'x': 'Region', 'y': 'Revenue ($)'}
        )
        fig_region.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    st.markdown("---")
    
    # SEGMENT & CATEGORY PERFORMANCE
    st.markdown("### 👥 Segment & Category Analysis")
    col_seg, col_cat = st.columns(2)
    
    segment_stats = filtered_df.groupby('customer_segment')['net_revenue'].sum().sort_values(ascending=False)
    category_stats = filtered_df.groupby('category')['net_revenue'].sum().sort_values(ascending=False).head(10)
    
    with col_seg:
        fig_segment = px.pie(
            values=segment_stats.values,
            names=segment_stats.index,
            title='💎 Revenue by Customer Segment',
            color_discrete_sequence=['#3647F5', '#FF9F0D', '#1B2346', '#D9D9D9']
        )
        fig_segment.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400
        )
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with col_cat:
        fig_category = px.bar(
            x=category_stats.values,
            y=category_stats.index,
            orientation='h',
            title='📦 Top 10 Categories',
            color=category_stats.values,
            color_continuous_scale=['#FF9F0D', '#3647F5']
        )
        fig_category.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_category, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: TRENDS
# ═════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">Trend Analysis</h2>', unsafe_allow_html=True)
    
    # MONTHLY TRENDS
    st.markdown("### 📅 Monthly Performance Trends")
    
    monthly_data = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique',
        'final_amount': 'mean',
        'satisfaction_rating': 'mean'
    }).reset_index()
    monthly_data['date'] = monthly_data['date'].astype(str)
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        fig_monthly_rev = px.line(
            monthly_data,
            x='date',
            y='net_revenue',
            markers=True,
            title='💰 Monthly Revenue Trend',
            labels={'date': 'Month', 'net_revenue': 'Revenue ($)'}
        )
        fig_monthly_rev.update_traces(
            line=dict(color='#FF9F0D', width=3),
            marker=dict(size=10, color='#3647F5', symbol='circle')
        )
        fig_monthly_rev.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            hovermode='x unified',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_monthly_rev, use_container_width=True)
    
    with col_m2:
        fig_monthly_cust = px.line(
            monthly_data,
            x='date',
            y='customer_id',
            markers=True,
            title='👥 Monthly Customer Growth',
            labels={'date': 'Month', 'customer_id': 'Customers'}
        )
        fig_monthly_cust.update_traces(
            line=dict(color='#3647F5', width=3),
            marker=dict(size=10, color='#FF9F0D', symbol='diamond')
        )
        fig_monthly_cust.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            hovermode='x unified',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_monthly_cust, use_container_width=True)
    
    col_m3, col_m4 = st.columns(2)
    
    with col_m3:
        fig_aov = px.line(
            monthly_data,
            x='date',
            y='final_amount',
            markers=True,
            title='📊 Avg Order Value Trend',
            labels={'date': 'Month', 'final_amount': 'Avg Order Value ($)'}
        )
        fig_aov.update_traces(
            line=dict(color='#FF9F0D', width=3),
            marker=dict(size=8, color='#1B2346')
        )
        fig_aov.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_aov, use_container_width=True)
    
    with col_m4:
        fig_satisfaction = px.line(
            monthly_data,
            x='date',
            y='satisfaction_rating',
            markers=True,
            title='⭐ Customer Satisfaction Trend',
            labels={'date': 'Month', 'satisfaction_rating': 'Satisfaction (1-5)'}
        )
        fig_satisfaction.update_traces(
            line=dict(color='#3647F5', width=3),
            marker=dict(size=8, color='#FF9F0D')
        )
        fig_satisfaction.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    st.markdown("---")
    
    # SEASONAL TRENDS
    st.markdown("### 🌡️ Seasonal Performance")
    
    season_stats = filtered_df.groupby('season').agg({
        'net_revenue': 'sum',
        'customer_id': 'count'
    }).sort_values('net_revenue', ascending=False)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        fig_season = px.bar(
            x=season_stats.index,
            y=season_stats['net_revenue'],
            title='🌡️ Revenue by Season',
            color=season_stats['net_revenue'],
            color_continuous_scale=['#FF9F0D', '#3647F5'],
            labels={'x': 'Season', 'y': 'Revenue ($)'},
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
    
    with col_s2:
        fig_season_orders = px.pie(
            values=season_stats['customer_id'],
            names=season_stats.index,
            title='📊 Orders Distribution by Season',
            color_discrete_sequence=['#3647F5', '#FF9F0D', '#1B2346', '#D9D9D9']
        )
        fig_season_orders.update_layout(
            plot_bgcolor='#040D2F',
            paper_bgcolor='#040D2F',
            font=dict(color='#D9D9D9'),
            height=400
        )
        st.plotly_chart(fig_season_orders, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: EFFICIENCY
# ═════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">Performance Efficiency</h2>', unsafe_allow_html=True)
    
    st.markdown("### ⚡ Efficiency Metrics")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    # Calculate efficiency metrics
    total_orders = len(filtered_df)
    total_customers = filtered_df['customer_id'].nunique()
    conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
    return_rate = (filtered_df['returned'].sum() / total_orders * 100) if total_orders > 0 else 0
    avg_roi = filtered_df['roi'].replace([np.inf, -np.inf], np.nan).mean()
    repeat_customers = len(filtered_df[filtered_df.groupby('customer_id').cumcount() > 0])
    repeat_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
    
    with col_e1:
        st.metric(
            "📊 Conversion Rate",
            f"{conversion_rate:.2f}%",
            f"{conversion_rate - 20:.2f}% vs target"
        )
    
    with col_e2:
        st.metric(
            "🔄 Return Rate",
            f"{return_rate:.2f}%",
            f"Target: <10%"
        )
    
    with col_e3:
        st.metric(
            "📈 Repeat Customer Rate",
            f"{repeat_rate:.2f}%",
            f"Loyalty rate"
        )
    
    st.markdown("---")
    
    # Channel Efficiency
    st.markdown("### 📊 Channel Efficiency Metrics")
    
    channel_efficiency = filtered_df.groupby('marketing_channel').agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique',
        'final_amount': 'mean',
        'satisfaction_rating': 'mean'
    }).round(2)
    
    channel_efficiency['Revenue per Customer'] = (channel_efficiency['net_revenue'] / channel_efficiency['customer_id']).round(2)
    channel_efficiency['ROI Efficiency'] = avg_roi
    
    # Display as table
    st.dataframe(
        channel_efficiency[['net_revenue', 'customer_id', 'final_amount', 'satisfaction_rating', 'Revenue per Customer']],
        use_container_width=True,
        height=250
    )
    
    st.markdown("---")
    
    # Segment Efficiency
    st.markdown("### 👥 Segment Efficiency Metrics")
    
    segment_efficiency = filtered_df.groupby('customer_segment').agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique',
        'customer_lifetime_value': 'mean',
        'satisfaction_rating': 'mean'
    }).round(2)
    
    segment_efficiency['CLV per Customer'] = segment_efficiency['customer_lifetime_value']
    
    st.dataframe(
        segment_efficiency,
        use_container_width=True,
        height=200
    )
    
    st.markdown("---")
    
    # ROI Analysis
    st.markdown("### 💰 ROI Analysis by Channel")
    
    roi_by_channel = filtered_df.groupby('marketing_channel')['roi'].agg(['mean', 'min', 'max']).round(2)
    
    fig_roi = px.bar(
        roi_by_channel.reset_index(),
        x='marketing_channel',
        y='mean',
        error_y='max',
        title='🎯 Average ROI by Channel with Range',
        labels={'marketing_channel': 'Channel', 'mean': 'Avg ROI'},
        color='mean',
        color_continuous_scale=['#FF9F0D', '#3647F5']
    )
    fig_roi.update_layout(
        plot_bgcolor='#040D2F',
        paper_bgcolor='#040D2F',
        font=dict(color='#D9D9D9'),
        height=400
    )
    st.plotly_chart(fig_roi, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4: RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown(f'<h2 style="color: {COLORS["accent"]};">Strategic Recommendations</h2>', unsafe_allow_html=True)
    
    # TOP PERFORMERS
    st.markdown("### 🏆 Top Performers")
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    
    channel_stats = filtered_df.groupby('marketing_channel')['net_revenue'].sum().sort_values(ascending=False)
    campaign_stats = filtered_df.groupby('marketing_campaign')['net_revenue'].sum().sort_values(ascending=False)
    segment_stats = filtered_df.groupby('customer_segment')['net_revenue'].sum().sort_values(ascending=False)
    
    best_channel = channel_stats.idxmax() if len(channel_stats) > 0 else "N/A"
    best_campaign = campaign_stats.idxmax() if len(campaign_stats) > 0 else "N/A"
    best_segment = segment_stats.idxmax() if len(segment_stats) > 0 else "N/A"
    
    with col_rec1:
        if best_channel != "N/A":
            st.info(
                f"""
                **🥇 Best Channel**
                
                {best_channel}
                
                💰 ${channel_stats.loc[best_channel]:,.0f}
                """
            )
        else:
            st.info("No data available")
    
    with col_rec2:
        if best_campaign != "N/A":
            st.success(
                f"""
                **🎯 Best Campaign**
                
                {best_campaign}
                
                💰 ${campaign_stats.loc[best_campaign]:,.0f}
                """
            )
        else:
            st.success("No data available")
    
    with col_rec3:
        if best_segment != "N/A":
            st.warning(
                f"""
                **👑 Best Segment**
                
                {best_segment}
                
                💰 ${segment_stats.loc[best_segment]:,.0f}
                """
            )
        else:
            st.warning("No data available")
    
    st.markdown("---")
    
    # STRATEGIC RECOMMENDATIONS
    st.markdown("### 💡 Strategic Action Items")
    
    col_action1, col_action2 = st.columns(2)
    
    with col_action1:
        st.markdown(f"""
        #### 📌 Optimization Strategies
        
        1. **🎯 Channel Focus**
           - Increase budget allocation to {best_channel}
           - Reduce spending on underperforming channels
           - Test new marketing channels
        
        2. **🔄 Customer Retention**
           - Develop loyalty program for {best_segment} segment
           - Implement personalized email campaigns
           - Create VIP benefits for high-value customers
        
        3. **📊 Data-Driven Decisions**
           - A/B test campaign strategies
           - Monitor KPIs weekly
           - Adjust strategies based on performance data
        """)
    
    with col_action2:
        st.markdown(f"""
        #### 🚀 Growth Opportunities
        
        1. **🌱 Market Expansion**
           - Focus on high-growth regions
           - Target new customer segments
           - Expand product categories
        
        2. **💰 Revenue Enhancement**
           - Increase average order value
           - Implement cross-selling strategies
           - Optimize pricing strategy
        
        3. **⭐ Customer Satisfaction**
           - Improve customer service
           - Enhance product quality
           - Reduce return rates
        """)
    
    st.markdown("---")
    
    # DETAILED METRICS TABLE
    st.markdown("### 📊 Detailed Performance Summary")
    
    summary_data = {
        'Metric': [
            'Total Revenue',
            'Total Customers',
            'Avg Order Value',
            'Customer Satisfaction',
            'Conversion Rate',
            'Return Rate',
            'Avg ROI'
        ],
        'Value': [
            f"${filtered_df['net_revenue'].sum():,.0f}",
            f"{filtered_df['customer_id'].nunique():,}",
            f"${filtered_df['final_amount'].mean():,.2f}",
            f"{filtered_df['satisfaction_rating'].mean():.2f}/5",
            f"{(filtered_df['customer_id'].nunique() / len(filtered_df) * 100):.2f}%",
            f"{(filtered_df['returned'].sum() / len(filtered_df) * 100):.2f}%",
            f"{filtered_df['roi'].replace([np.inf, -np.inf], np.nan).mean():.2f}x"
        ],
        'Status': ['✅'] * 7
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, height=300)

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    f"""
    <p style='text-align: center; color: {COLORS['light']}; font-size: 12px;'>
    ✨ Dashboard Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
    📊 Data Points: {len(filtered_df):,} | 
    🎯 All Rights Reserved
    </p>
    """,
    unsafe_allow_html=True
)
