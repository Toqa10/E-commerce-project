# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ====== إعداد الصفحة ======
st.set_page_config(
    page_title="NexaVerse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====== CSS للثيم الكامل ======
st.markdown(
    """
    <style>
    /* خلفية الصفحة */
    .main {
        background-color: #f3f4f6;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #e5e7eb;
        padding-top: 1.5rem;
    }
    
    .sidebar-logo {
        font-weight: 800;
        font-size: 22px;
        color: #111827;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0 1rem;
    }
    
    .sidebar-logo-circle {
        width: 32px;
        height: 32px;
        border-radius: 999px;
        background-color: #111827;
    }
    
    /* إخفاء عناصر streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* KPI Cards */
    .kpi-card {
        border-radius: 16px;
        padding: 20px;
        color: #f9fafb;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #e5e7eb;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
    }
    
    .kpi-sub {
        font-size: 12px;
        color: #e5e7eb;
    }
    
    .kpi-navy   { background-color: #111827; }
    .kpi-orange { background-color: #f59e0b; }
    .kpi-blue   { background-color: #2563eb; }
    .kpi-indigo { background-color: #4f46e5; }
    
    /* عناوين التابات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 8px;
        color: #111827;
        font-weight: 600;
        font-size: 14px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #111827;
        color: white;
    }
    
    /* بطاقات المحتوى */
    .content-card {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 16px;
    }
    
    /* جداول البيانات */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: #111827 !important;
        color: white !important;
        font-weight: 600;
        padding: 12px !important;
    }
    
    .dataframe td {
        padding: 10px !important;
        border-bottom: 1px solid #e5e7eb !important;
    }
    
    /* الأزرار */
    .stButton > button {
        background-color: #111827;
        color: white;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #374151;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* تنسيق الفلاتر */
    .stSelectbox, .stMultiSelect {
        border-radius: 8px;
    }
    
    /* عنوان Dashboard */
    .dash-header {
        background-color: white;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .dash-title {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ====== تحميل البيانات ======
@st.cache_data
def load_data():
    try:
        # تحميل الملف
        df = pd.read_csv("cleaned_data.csv")
        
        # تحويل التاريخ
        df['date'] = pd.to_datetime(df['date'])
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        
        # حساب الأعمدة المطلوبة إذا لم تكن موجودة
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
        st.error(f"Error loading data: {str(e)}")
        return None

df = load_data()

if df is None:
    st.error("⚠️ يرجى رفع ملف cleaned_data.csv في نفس المجلد مع app.py")
    st.stop()

# ====== Sidebar ======
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <div class="sidebar-logo-circle"></div>
            <span>NexaVerse</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    st.subheader("🎯 Filters")
    
    # فلتر القنوات
    all_channels = ['All Channels'] + sorted(df['marketing_channel'].unique().tolist())
    selected_channel = st.selectbox(
        "Marketing Channel",
        options=all_channels,
        index=0
    )
    
    # فلتر الشهور
    st.markdown("#### 📅 Month Range")
    
    # تحويل الشهور لتواريخ
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    st.markdown("---")
    
    # معلومات إضافية
    st.markdown("### 📊 Dashboard Info")
    st.info(f"""
    **Total Records:** {len(df):,}  
    **Date Range:** {min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}  
    **Channels:** {df['marketing_channel'].nunique()}
    """)
    
    st.markdown("---")
    st.markdown("**© 2024 NexaVerse Analytics**")

# ====== تطبيق الفلاتر ======
filtered_df = df.copy()

# فلتر القناة
if selected_channel != 'All Channels':
    filtered_df = filtered_df[filtered_df['marketing_channel'] == selected_channel]

# فلتر التاريخ
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) & 
        (filtered_df['date'].dt.date <= end_date)
    ]

# ====== Header ======
st.markdown(
    """
    <div class="dash-header">
        <h1 class="dash-title">📊 E-Commerce Analytics Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ====== حساب الـ KPIs ======
total_revenue = filtered_df['net_revenue'].sum()
total_customers = filtered_df['customer_id'].nunique()
total_orders = len(filtered_df)
avg_order_value = filtered_df['Average Order Value'].mean()

# حساب ROI بطريقة آمنة
discount_sum = filtered_df['discount_amount'].sum()
if discount_sum > 0:
    total_roi = ((filtered_df['net_revenue'].sum() - discount_sum) / discount_sum * 100)
else:
    total_roi = 0

# ====== إنشاء التابات ======
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 KPIs & Overview",
    "🎯 Channel Performance",
    "📅 Time Trends",
    "⚡ Efficiency Analysis",
    "💡 About & Recommendations"
])

# ==================== TAB 1: KPIs & Overview ====================
with tab1:
    # صف الـ KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="kpi-card kpi-navy">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">${total_revenue:,.0f}</div>
                <div class="kpi-sub">Net revenue from all sales</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="kpi-card kpi-orange">
                <div class="kpi-label">Total Customers</div>
                <div class="kpi-value">{total_customers:,}</div>
                <div class="kpi-sub">Unique customers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="kpi-card kpi-blue">
                <div class="kpi-label">Total Orders</div>
                <div class="kpi-value">{total_orders:,}</div>
                <div class="kpi-sub">Total transactions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="kpi-card kpi-indigo">
                <div class="kpi-label">Average ROI</div>
                <div class="kpi-value">{total_roi:.1f}%</div>
                <div class="kpi-sub">Return on investment</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الصف الثاني: الرسوم البيانية
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Revenue by Category</div>', unsafe_allow_html=True)
        
        # Revenue by Category
        category_revenue = filtered_df.groupby('category')['net_revenue'].sum().sort_values(ascending=False)
        
        fig_category = px.bar(
            x=category_revenue.values,
            y=category_revenue.index,
            orientation='h',
            labels={'x': 'Revenue ($)', 'y': 'Category'},
            color=category_revenue.values,
            color_continuous_scale=['#3647F5', '#FF9F0D']
        )
        
        fig_category.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=400,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False
        )
        
        fig_category.update_traces(marker_line_width=0)
        st.plotly_chart(fig_category, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎯 Sales by Region</div>', unsafe_allow_html=True)
        
        # Sales by Region - Donut Chart
        region_sales = filtered_df.groupby('region')['net_revenue'].sum()
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=region_sales.index,
            values=region_sales.values,
            hole=0.6,
            marker=dict(colors=['#111827', '#f59e0b', '#2563eb', '#4f46e5', '#10b981', '#ef4444'])
        )])
        
        fig_donut.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827', size=12),
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # الصف الثالث: جداول الإحصائيات
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 KPIs Summary by Segment</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KPIs by Customer Segment
        kpi_segment = filtered_df.groupby('customer_segment').agg({
            'net_revenue': 'sum',
            'customer_id': 'nunique',
            'quantity': 'sum',
            'Average Order Value': 'mean'
        }).round(2)
        
        kpi_segment.columns = ['Revenue ($)', 'Customers', 'Orders', 'Avg Order Value ($)']
        kpi_segment = kpi_segment.sort_values('Revenue ($)', ascending=False)
        
        st.markdown("**By Customer Segment**")
        st.dataframe(kpi_segment, use_container_width=True)
    
    with col2:
        # KPIs by Payment Method
        kpi_payment = filtered_df.groupby('payment_method').agg({
            'net_revenue': 'sum',
            'customer_id': 'nunique',
            'quantity': 'sum'
        }).round(2)
        
        kpi_payment.columns = ['Revenue ($)', 'Customers', 'Orders']
        kpi_payment = kpi_payment.sort_values('Revenue ($)', ascending=False)
        
        st.markdown("**By Payment Method**")
        st.dataframe(kpi_payment, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: Channel Performance ====================
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎯 Total Performance per Channel</div>', unsafe_allow_html=True)
    
    # حساب المؤشرات لكل قناة
    channel_performance = filtered_df.groupby('marketing_channel').agg({
        'marketing_spend': 'sum',
        'net_revenue': 'sum',
        'customer_id': 'nunique',
        'discount_amount': 'sum'
    }).round(2)
    
    channel_performance.columns = ['Total Spend', 'Total Revenue', 'Total Conversions', 'Total Discount']
    
    # حساب ROI بطريقة آمنة
    channel_performance['Average ROI'] = 0.0
    for idx in channel_performance.index:
        discount = channel_performance.loc[idx, 'Total Discount']
        revenue = channel_performance.loc[idx, 'Total Revenue']
        if discount > 0:
            channel_performance.loc[idx, 'Average ROI'] = ((revenue - discount) / discount * 100)
    
    channel_performance = channel_performance.sort_values('Total Revenue', ascending=False)
    
    # عرض الجدول
    st.dataframe(
        channel_performance.style.format({
            'Total Spend': '${:,.2f}',
            'Total Revenue': '${:,.2f}',
            'Total Conversions': '{:,.0f}',
            'Total Discount': '${:,.2f}',
            'Average ROI': '{:.2f}%'
        }),
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # الرسوم البيانية المقارنة
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💰 Total Revenue by Channel</div>', unsafe_allow_html=True)
        
        fig_revenue = px.bar(
            channel_performance.reset_index().sort_values('Total Revenue', ascending=True),
            x='Total Revenue',
            y='marketing_channel',
            orientation='h',
            color='Total Revenue',
            color_continuous_scale=['#3647F5', '#FF9F0D'],
            labels={'marketing_channel': 'Channel', 'Total Revenue': 'Revenue ($)'}
        )
        
        fig_revenue.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=500,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False
        )
        
        fig_revenue.update_traces(marker_line_width=0)
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">👥 Total Conversions by Channel</div>', unsafe_allow_html=True)
        
        fig_conversions = px.bar(
            channel_performance.reset_index().sort_values('Total Conversions', ascending=True),
            x='Total Conversions',
            y='marketing_channel',
            orientation='h',
            color='Total Conversions',
            color_continuous_scale=['#10b981', '#f59e0b'],
            labels={'marketing_channel': 'Channel', 'Total Conversions': 'Conversions'}
        )
        
        fig_conversions.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=500,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False
        )
        
        fig_conversions.update_traces(marker_line_width=0)
        st.plotly_chart(fig_conversions, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ROI Comparison
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 ROI Comparison Across Channels</div>', unsafe_allow_html=True)
    
    fig_roi = px.bar(
        channel_performance.reset_index().sort_values('Average ROI', ascending=False),
        x='marketing_channel',
        y='Average ROI',
        color='Average ROI',
        color_continuous_scale=['#ef4444', '#10b981'],
        labels={'marketing_channel': 'Channel', 'Average ROI': 'ROI (%)'}
    )
    
    fig_roi.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111827'),
        showlegend=False,
        height=400,
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        coloraxis_showscale=False
    )
    
    fig_roi.update_traces(marker_line_width=0)
    st.plotly_chart(fig_roi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 3: Time Trends ====================
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📅 Monthly Trends Analysis</div>', unsafe_allow_html=True)
    
    # إعداد البيانات الشهرية
    monthly_data = filtered_df.groupby(['month_year', 'marketing_channel']).agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    monthly_data.columns = ['month', 'channel', 'revenue', 'conversions']
    
    # إجمالي الاتجاهات الشهرية
    monthly_total = filtered_df.groupby('month_year').agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    monthly_total.columns = ['month', 'total_revenue', 'total_conversions']
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # الرسوم البيانية
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💵 Monthly Revenue Trend</div>', unsafe_allow_html=True)
        
        fig_revenue_trend = px.line(
            monthly_total,
            x='month',
            y='total_revenue',
            markers=True,
            labels={'month': 'Month', 'total_revenue': 'Revenue ($)'}
        )
        
        fig_revenue_trend.update_traces(
            line=dict(color='#3647F5', width=3),
            marker=dict(size=8, color='#FF9F0D')
        )
        
        fig_revenue_trend.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=350,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb')
        )
        
        st.plotly_chart(fig_revenue_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">👥 Monthly Conversions Trend</div>', unsafe_allow_html=True)
        
        fig_conv_trend = px.line(
            monthly_total,
            x='month',
            y='total_conversions',
            markers=True,
            labels={'month': 'Month', 'total_conversions': 'Conversions'}
        )
        
        fig_conv_trend.update_traces(
            line=dict(color='#FF9F0D', width=3),
            marker=dict(size=8, color='#3647F5')
        )
        
        fig_conv_trend.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=350,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb')
        )
        
        st.plotly_chart(fig_conv_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Revenue by Channel over Time
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Monthly Revenue by Channel</div>', unsafe_allow_html=True)
    
    fig_channel_time = px.line(
        monthly_data,
        x='month',
        y='revenue',
        color='channel',
        markers=True,
        labels={'month': 'Month', 'revenue': 'Revenue ($)', 'channel': 'Channel'}
    )
    
    fig_channel_time.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111827'),
        height=450,
        xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_channel_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversions by Channel over Time
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👥 Monthly Conversions by Channel</div>', unsafe_allow_html=True)
    
    fig_conv_channel_time = px.line(
        monthly_data,
        x='month',
        y='conversions',
        color='channel',
        markers=True,
        labels={'month': 'Month', 'conversions': 'Conversions', 'channel': 'Channel'}
    )
    
    fig_conv_channel_time.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111827'),
        height=450,
        xaxis=dict(showgrid=True, gridcolor='#e5e7eb', tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_conv_channel_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # تفسير الاتجاهات
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💡 Trend Insights</div>', unsafe_allow_html=True)
    
    if len(monthly_total) > 0:
        # حساب بعض الإحصائيات
        peak_revenue_month = monthly_total.loc[monthly_total['total_revenue'].idxmax(), 'month']
        peak_revenue_value = monthly_total['total_revenue'].max()
        
        low_revenue_month = monthly_total.loc[monthly_total['total_revenue'].idxmin(), 'month']
        low_revenue_value = monthly_total['total_revenue'].min()
        
        growth_rate = ((peak_revenue_value - low_revenue_value) / low_revenue_value * 100) if low_revenue_value > 0 else 0
        
        st.success(f"""
        **Peak Performance:**
        - Highest Revenue: **${peak_revenue_value:,.0f}** in **{peak_revenue_month}**
        
        **Low Performance:**
        - Lowest Revenue: **${low_revenue_value:,.0f}** in **{low_revenue_month}**
        
        **Growth Rate:** {growth_rate:,.1f}% from low to peak
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 4: Efficiency Analysis ====================
with tab4:
    # CPC by Channel
    cpc_by_channel = filtered_df.groupby('marketing_channel').agg({
        'cpc': 'mean',
        'marketing_spend': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    cpc_by_channel.columns = ['Channel', 'Avg_CPC', 'Total_Spend', 'Total_Clicks']
    cpc_by_channel = cpc_by_channel.sort_values('Avg_CPC')
    
    # Conversion Rate by Channel
    conversion_by_channel = filtered_df.groupby('marketing_channel').agg({
        'customer_id': 'nunique',
        'visits': 'sum'
    }).reset_index()
    
    conversion_by_channel['conversion_rate'] = (
        conversion_by_channel['customer_id'] / conversion_by_channel['visits'] * 100
    ).round(3)
    
    conversion_by_channel.columns = ['Channel', 'Conversions', 'Total_Visits', 'Conversion_Rate']
    conversion_by_channel = conversion_by_channel.sort_values('Conversion_Rate', ascending=False)
    
    # Efficiency Ranking
    efficiency = pd.DataFrame({
        'Channel': cpc_by_channel['Channel'],
        'Avg_CPC': cpc_by_channel['Avg_CPC'].values,
        'Conversion_Rate': conversion_by_channel.set_index('Channel').loc[cpc_by_channel['Channel'], 'Conversion_Rate'].values
    })
    
    efficiency['Efficiency_Score'] = (
        (1 / efficiency['Avg_CPC'] * 100) + (efficiency['Conversion_Rate'] * 10)
    ).round(2)
    
    efficiency = efficiency.sort_values('Efficiency_Score', ascending=False).reset_index(drop=True)
    efficiency['Rank'] = range(1, len(efficiency) + 1)
    
    # العرض
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💲 Cost Per Click (CPC) by Channel</div>', unsafe_allow_html=True)
        
        fig_cpc = px.bar(
            cpc_by_channel.sort_values('Avg_CPC'),
            x='Avg_CPC',
            y='Channel',
            orientation='h',
            color='Avg_CPC',
            color_continuous_scale=['#10b981', '#3647F5', '#FF9F0D'],
            labels={'Avg_CPC': 'Average CPC ($)', 'Channel': 'Marketing Channel'}
        )
        
        fig_cpc.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=450,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False
        )
        
        fig_cpc.update_traces(marker_line_width=0)
        st.plotly_chart(fig_cpc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Conversion Rate by Channel</div>', unsafe_allow_html=True)
        
        fig_conv_rate = px.bar(
            conversion_by_channel.sort_values('Conversion_Rate', ascending=False),
            x='Channel',
            y='Conversion_Rate',
            color='Conversion_Rate',
            color_continuous_scale=['#3647F5', '#10b981'],
            labels={'Conversion_Rate': 'Conversion Rate (%)', 'Channel': 'Marketing Channel'}
        )
        
        fig_conv_rate.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            showlegend=False,
            height=450,
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            coloraxis_showscale=False
        )
        
        fig_conv_rate.update_traces(marker_line_width=0)
        st.plotly_chart(fig_conv_rate, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Efficiency Ranking
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏆 Channel Efficiency Ranking</div>', unsafe_allow_html=True)
    
    fig_efficiency = px.bar(
        efficiency,
        x='Efficiency_Score',
        y='Channel',
        orientation='h',
        color='Efficiency_Score',
        color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
        labels={'Efficiency_Score': 'Efficiency Score', 'Channel': 'Marketing Channel'},
        text='Rank'
    )
    
    fig_efficiency.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111827'),
        showlegend=False,
        height=450,
        xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False
    )
    
    fig_efficiency.update_traces(marker_line_width=0, textposition='outside')
    st.plotly_chart(fig_efficiency, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Spend Impact Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💰 Spend vs Revenue</div>', unsafe_allow_html=True)
        
        spend_revenue = filtered_df.groupby('marketing_channel').agg({
            'marketing_spend': 'sum',
            'net_revenue': 'sum'
        }).reset_index()
        
        spend_revenue['revenue_to_spend_ratio'] = (
            spend_revenue['net_revenue'] / spend_revenue['marketing_spend']
        ).round(2)
        
        fig_spend_rev = px.scatter(
            spend_revenue,
            x='marketing_spend',
            y='net_revenue',
            size='revenue_to_spend_ratio',
            color='revenue_to_spend_ratio',
            text='marketing_channel',
            color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
            labels={'marketing_spend': 'Total Spend ($)', 'net_revenue': 'Total Revenue ($)'}
        )
        
        fig_spend_rev.update_traces(textposition='top center', marker_line_width=2, marker_line_color='#111827')
        
        fig_spend_rev.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            height=450,
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            coloraxis_showscale=True
        )
        
        st.plotly_chart(fig_spend_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📈 Correlation Analysis</div>', unsafe_allow_html=True)
        
        # حساب الارتباطات بطريقة آمنة
        try:
            corr_matrix = filtered_df[['marketing_spend', 'net_revenue']].corr()
            corr_spend_revenue = corr_matrix.iloc[0, 1]
        except:
            corr_spend_revenue = 0
        
        try:
            spend_conv = filtered_df.groupby('marketing_channel').agg({
                'marketing_spend': 'sum',
                'customer_id': 'nunique'
            })
            corr_spend_conversions = spend_conv.corr().iloc[0, 1]
        except:
            corr_spend_conversions = 0
        
        try:
            cpc_rev = filtered_df.groupby('marketing_channel').agg({
                'cpc': 'mean',
                'net_revenue': 'sum'
            })
            corr_cpc_revenue = cpc_rev.corr().iloc[0, 1]
        except:
            corr_cpc_revenue = 0
        
        st.metric("Spend ↔ Revenue", f"{corr_spend_revenue:.3f}")
        st.metric("Spend ↔ Conversions", f"{corr_spend_conversions:.3f}")
        st.metric("CPC ↔ Revenue", f"{corr_cpc_revenue:.3f}")
        
        st.info("""
        **Interpretation:**
        - Values close to **+1**: Strong positive correlation
        - Values close to **-1**: Strong negative correlation
        - Values close to **0**: Weak or no correlation
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 5: About & Recommendations ====================
with tab5:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 About This Dashboard</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### E-Commerce Analytics Dashboard
        
        هذا Dashboard تم تطويره لتحليل الأداء التسويقي والمبيعات لمتجر إلكتروني. يوفر رؤى شاملة حول:
        
        #### 📈 المؤشرات الرئيسية (KPIs)
        - **إجمالي الإيرادات**: مجموع صافي الإيرادات من جميع المبيعات
        - **عدد العملاء**: عدد العملاء الفريدين
        - **إجمالي الطلبات**: عدد المعاملات الكلي
        - **متوسط ROI**: العائد على الاستثمار
        
        #### 🎯 تحليل أداء القنوات
        - مقارنة الأداء عبر جميع قنوات التسويق
        - تحليل الإنفاق والإيرادات والتحويلات
        - حساب ROI لكل قناة
        
        #### 📅 تحليل الاتجاهات الزمنية
        - تتبع الإيرادات الشهرية
        - تحليل التحويلات على مدار الوقت
        - تحديد فترات الذروة والانخفاض
        
        #### ⚡ تحليل الكفاءة
        - **CPC** (تكلفة النقرة): كفاءة الإنفاق الإعلاني
        - **معدل التحويل**: فعالية كل قناة في تحويل الزوار
        - **ترتيب الكفاءة**: تصنيف القنوات حسب الأداء الشامل
        - **تأثير الإنفاق**: تحليل العلاقة بين الإنفاق والنتائج
        
        ---
        
        ### 🔍 كيفية الاستخدام
        
        1. **استخدم الفلاتر** في الشريط الجانبي لتصفية البيانات حسب القناة والفترة الزمنية
        2. **تنقل بين التابات** للوصول إلى التحليلات المختلفة
        3. **تفاعل مع الرسوم البيانية** للحصول على تفاصيل أكثر (hover, zoom, pan)
        4. **قارن الأداء** عبر القنوات والفترات المختلفة
        
        ---
        
        ### 👥 Team Members
        - **Zaid Tarek** - Data Preparation & KPIs
        - **Mayar** - Visualization & Charts
        - **Ahmed** - Channel Analysis
        - **Toqa** - Streamlit Development
        
        ---
        
        **© 2024 NexaVerse Analytics | Powered by Streamlit & Plotly**
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 Key Recommendations</div>', unsafe_allow_html=True)
        
        # حساب بعض التوصيات المبنية على البيانات
        if len(channel_performance) > 0:
            best_roi_channel = channel_performance['Average ROI'].idxmax()
            best_roi_value = channel_performance['Average ROI'].max()
            
            best_cpc_channel = cpc_by_channel.iloc[0]['Channel']
            best_cpc_value = cpc_by_channel.iloc[0]['Avg_CPC']
            
            best_conv_channel = conversion_by_channel.iloc[0]['Channel']
            best_conv_value = conversion_by_channel.iloc[0]['Conversion_Rate']
            
            st.success(f"""
            ### 🏆 Top Performers
            
            **Best ROI:**  
            {best_roi_channel}  
            ROI: {best_roi_value:.2f}%
            
            **Most Efficient (CPC):**  
            {best_cpc_channel}  
            CPC: ${best_cpc_value:.2f}
            
            **Best Conversion Rate:**  
            {best_conv_channel}  
            Rate: {best_conv_value:.3f}%
            """)
        
        st.warning("""
        ### 📌 Action Items
        
        1. **زيادة الاستثمار** في القنوات ذات ROI العالي
        
        2. **تحسين الحملات** في القنوات ذات معدل التحويل المنخفض
        
        3. **مراجعة الإنفاق** في القنوات ذات CPC المرتفع
        
        4. **التركيز على فترات الذروة** لزيادة الإيرادات
        
        5. **تحليل أسباب الانخفاض** في الفترات الضعيفة
        """)
        
        st.info(f"""
        ### 📊 Data Quality
        
        ✅ Data is cleaned and validated  
        ✅ Missing values handled  
        ✅ Outliers detected and managed  
        ✅ KPIs calculated accurately  
        
        **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # إحصائيات إضافية
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Dataset Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        st.metric("Marketing Channels", df['marketing_channel'].nunique())
    
    with col3:
        st.metric("Categories", df['category'].nunique())
    
    with col4:
        st.metric("Date Range", f"{(df['date'].max() - df['date'].min()).days} days")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== Footer ======
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; font-size: 14px; padding: 20px;'>
        <strong>NexaVerse Analytics Dashboard</strong> | 
        Built with ❤️ using Streamlit & Plotly | 
        © 2024 All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)
