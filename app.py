import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 1rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Load Data with Caching
@st.cache_data
def load_data():
    try:
        # قراءة البيانات من CSV
        df = pd.read_csv('cleaned_data.csv')

        # تحويل التواريخ
        df['date'] = pd.to_datetime(df['date'])
        df['month_date'] = pd.to_datetime(df['month_date'])
        df['registration_date'] = pd.to_datetime(df['registration_date'])

        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")
        return None

# Main Title
st.markdown('<h1 class="main-header">🛒 E-commerce Analytics Dashboard</h1>', unsafe_allow_html=True)

# Load Data
df = load_data()

if df is not None:
    # ==================== SIDEBAR FILTERS ====================
    st.sidebar.header("🔍 Filters")

    # Marketing Channel Filter
    all_channels = ['All Channels'] + sorted(df['marketing_channel'].dropna().unique().tolist())
    selected_channel = st.sidebar.selectbox(
        "Marketing Channel",
        options=all_channels,
        index=0
    )

    # Month Range Filter
    min_date = df['month_date'].min()
    max_date = df['month_date'].max()

    date_range = st.sidebar.date_input(
        "Month Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply Filters
    filtered_df = df.copy()

    if selected_channel != 'All Channels':
        filtered_df = filtered_df[filtered_df['marketing_channel'] == selected_channel]

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['month_date'] >= pd.to_datetime(start_date)) &
            (filtered_df['month_date'] <= pd.to_datetime(end_date))
        ]

    # Display filter info
    st.sidebar.info(f"📊 **Filtered Records:** {len(filtered_df):,} / {len(df):,}")

    # ==================== KPIs SECTION ====================
    st.header("📈 Key Performance Indicators")

    # Calculate KPIs
    total_revenue = filtered_df['net_revenue'].sum()
    total_customers = filtered_df['customer_id'].nunique()
    total_orders = len(filtered_df)
    avg_order_value = filtered_df['final_amount'].mean()
    conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
    return_rate = (filtered_df['returned'].sum() / total_orders * 100) if total_orders > 0 else 0
    avg_satisfaction = filtered_df['satisfaction_rating'].mean()
    avg_roi = filtered_df['roi'].mean()

    # Display KPIs in columns
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

    st.divider()

    # ==================== CHARTS SECTION ====================
    st.header("📊 Data Visualizations")

    # Chart 1 & 2: ROI by Channel & Revenue by Category
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. ROI by Marketing Channel")
        roi_channel = filtered_df.groupby('marketing_channel')['roi'].mean().reset_index()
        roi_channel = roi_channel.sort_values('roi', ascending=False)
        fig1 = px.bar(roi_channel, x='marketing_channel', y='roi',
                     labels={'roi': 'ROI (%)', 'marketing_channel': 'Channel'},
                     color='roi', color_continuous_scale='Blues')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("2. Net Revenue by Product Category")
        revenue_category = filtered_df.groupby('category')['net_revenue'].sum().reset_index()
        revenue_category = revenue_category.sort_values('net_revenue', ascending=False)
        fig2 = px.bar(revenue_category, x='category', y='net_revenue',
                     labels={'net_revenue': 'Net Revenue ($)', 'category': 'Category'},
                     color='net_revenue', color_continuous_scale='Greens')
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Monthly Revenue Trend
    st.subheader("3. Monthly Revenue Trend")
    monthly_revenue = filtered_df.groupby('month_date')['net_revenue'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('month_date')
    fig3 = px.line(monthly_revenue, x='month_date', y='net_revenue',
                  labels={'net_revenue': 'Net Revenue ($)', 'month_date': 'Month'},
                  markers=True)
    fig3.update_traces(line_color='#1f77b4', line_width=3)
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 & 5: Segment Distribution & Revenue by Region
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("4. Revenue by Customer Segment")
        segment_revenue = filtered_df.groupby('customer_segment')['net_revenue'].sum().reset_index()
        fig4 = px.pie(segment_revenue, values='net_revenue', names='customer_segment',
                     title='')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.subheader("5. Revenue by Region (Gross vs Net)")
        region_revenue = filtered_df.groupby('region').agg({
            'gross_revenue': 'sum',
            'net_revenue': 'sum'
        }).reset_index()
        fig5 = go.Figure(data=[
            go.Bar(name='Gross Revenue', x=region_revenue['region'], y=region_revenue['gross_revenue']),
            go.Bar(name='Net Revenue', x=region_revenue['region'], y=region_revenue['net_revenue'])
        ])
        fig5.update_layout(barmode='group', xaxis_title='Region', yaxis_title='Revenue ($)')
        st.plotly_chart(fig5, use_container_width=True)

    # Chart 6: Campaign Effectiveness
    st.subheader("6. Campaign Effectiveness: Revenue vs Customers")
    campaign_data = filtered_df.groupby('marketing_campaign').agg({
        'net_revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    campaign_data.columns = ['marketing_campaign', 'Revenue', 'Customers']
    fig6 = go.Figure(data=[
        go.Bar(name='Revenue ($)', x=campaign_data['marketing_campaign'], y=campaign_data['Revenue']),
        go.Bar(name='Customers', x=campaign_data['marketing_campaign'], y=campaign_data['Customers'])
    ])
    fig6.update_layout(barmode='group', xaxis_title='Campaign', yaxis_title='Value')
    st.plotly_chart(fig6, use_container_width=True)

    # Chart 7: Seasonal Analysis
    st.subheader("7. Seasonal Revenue Analysis (Gross vs Net)")
    seasonal_revenue = filtered_df.groupby('season').agg({
        'gross_revenue': 'sum',
        'net_revenue': 'sum'
    }).reset_index()
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=seasonal_revenue['season'], y=seasonal_revenue['gross_revenue'],
                             mode='lines+markers', name='Gross Revenue', line=dict(width=3)))
    fig7.add_trace(go.Scatter(x=seasonal_revenue['season'], y=seasonal_revenue['net_revenue'],
                             mode='lines+markers', name='Net Revenue', line=dict(width=3)))
    fig7.update_layout(xaxis_title='Season', yaxis_title='Revenue ($)')
    st.plotly_chart(fig7, use_container_width=True)

    # Chart 8 & 9: Order Value vs ROI & Payment Method
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("8. Order Value vs ROI by Category")
        category_metrics = filtered_df.groupby('category').agg({
            'final_amount': 'mean',
            'roi': 'mean'
        }).reset_index()
        fig8 = px.scatter(category_metrics, x='final_amount', y='roi',
                         text='category', size='roi',
                         labels={'final_amount': 'Avg Order Value ($)', 'roi': 'ROI (%)'},
                         color='roi', color_continuous_scale='Viridis')
        fig8.update_traces(textposition='top center')
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.subheader("9. Payment Method Performance")
        payment_data = filtered_df.groupby('payment_method').agg({
            'net_revenue': 'sum',
            'order_id': 'count'
        }).reset_index()
        payment_data.columns = ['payment_method', 'Revenue', 'Orders']
        fig9 = go.Figure(data=[
            go.Bar(name='Revenue ($)', x=payment_data['payment_method'], y=payment_data['Revenue']),
            go.Bar(name='Orders', x=payment_data['payment_method'], y=payment_data['Orders'])
        ])
        fig9.update_layout(barmode='group')
        st.plotly_chart(fig9, use_container_width=True)

    # Chart 10: Revenue by Device Type
    st.subheader("10. Revenue by Device Type")
    device_revenue = filtered_df.groupby('device_type')['net_revenue'].sum().reset_index()
    fig10 = px.pie(device_revenue, values='net_revenue', names='device_type',
                  hole=0.4)
    st.plotly_chart(fig10, use_container_width=True)

    # Chart 11 & 12: CLV & Retention + Shipping Performance
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("11. CLV & Retention by Segment")
        clv_data = filtered_df.groupby('customer_segment').agg({
            'customer_lifetime_value': 'mean',
            'retention_score': 'mean'
        }).reset_index()
        fig11 = go.Figure(data=[
            go.Bar(name='CLV ($)', x=clv_data['customer_segment'], y=clv_data['customer_lifetime_value']),
            go.Bar(name='Retention Score', x=clv_data['customer_segment'], y=clv_data['retention_score'])
        ])
        fig11.update_layout(barmode='group')
        st.plotly_chart(fig11, use_container_width=True)

    with col2:
        st.subheader("12. Shipping Method Performance")
        shipping_data = filtered_df.groupby('shipping_method').agg({
            'net_revenue': 'sum',
            'satisfaction_rating': 'mean'
        }).reset_index()
        fig12 = go.Figure(data=[
            go.Bar(name='Revenue ($)', x=shipping_data['shipping_method'], y=shipping_data['net_revenue']),
            go.Bar(name='Satisfaction', x=shipping_data['shipping_method'], y=shipping_data['satisfaction_rating']*1000)
        ])
        fig12.update_layout(barmode='group')
        st.plotly_chart(fig12, use_container_width=True)

    # Chart 13: Satisfaction Impact on Revenue & Returns
    st.subheader("13. Satisfaction Rating Impact on Revenue & Returns")
    satisfaction_data = filtered_df.groupby('satisfaction_rating').agg({
        'net_revenue': 'mean',
        'returned': 'sum'
    }).reset_index()
    fig13 = px.scatter(satisfaction_data, x='satisfaction_rating', y='net_revenue',
                      size='returned', color='returned',
                      labels={'net_revenue': 'Avg Revenue ($)', 'satisfaction_rating': 'Rating', 'returned': 'Returns'},
                      color_continuous_scale='Reds')
    st.plotly_chart(fig13, use_container_width=True)

    # ==================== DATA TABLE ====================
    st.divider()
    st.header("📋 Filtered Data Table")

    # Display data with download button
    st.dataframe(filtered_df.head(1000), use_container_width=True)

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_ecommerce_data.csv',
        mime='text/csv',
    )

    # Footer
    st.divider()
    st.caption("📊 E-commerce Analytics Dashboard | Built with Streamlit")

else:
    st.error("⚠️ لم يتم العثور على ملف البيانات. تأكد من وجود 'cleaned_data.csv' في نفس المجلد.")
