import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .kpi-label {
        font-size: 1rem;
        color: #64748B;
        font-weight: 500;
    }
    .positive-change {
        color: #10B981;
        font-weight: 600;
    }
    .negative-change {
        color: #EF4444;
        font-weight: 600;
    }
    .tab-content {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Create month-year column for filtering
        if 'date' in df.columns:
            df['month_year'] = df['date'].dt.strftime('%Y-%m')
        
        return df
    except FileNotFoundError:
        st.error("File 'cleaned_data.csv' not found. Please ensure it's in the same directory.")
        return pd.DataFrame()

# Load the data
df = load_data()

# Check if data is loaded
if df.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("📊 Filters")

# Channel filter
available_channels = ['All'] + sorted(df['marketing_channel'].dropna().unique().tolist())
selected_channel = st.sidebar.selectbox(
    "Select Marketing Channel",
    available_channels
)

# Date range filter
if 'date' in df.columns:
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(start_date) == 2:
        start_date, end_date = start_date
    else:
        # Default to full range if not properly selected
        start_date, end_date = min_date, max_date
else:
    start_date, end_date = None, None

# Apply filters
filtered_df = df.copy()

if selected_channel != 'All':
    filtered_df = filtered_df[filtered_df['marketing_channel'] == selected_channel]

if 'date' in df.columns and start_date and end_date:
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) & 
        (filtered_df['date'].dt.date <= end_date)
    ]

# Calculate KPIs for the filtered data
if not filtered_df.empty:
    # Overall KPIs
    total_revenue = filtered_df['net_revenue'].sum()
    total_spend = filtered_df['discount_amount'].sum()
    total_conversions = filtered_df['customer_id'].nunique()
    total_orders = len(filtered_df)
    
    # Derived KPIs
    overall_conversion_rate = total_orders / total_conversions if total_conversions > 0 else 0
    overall_cpc = total_spend / total_conversions if total_conversions > 0 else 0
    overall_roi = (total_revenue - total_spend) / total_spend if total_spend > 0 else 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Channel performance
    channel_perf = filtered_df.groupby('marketing_channel').agg({
        'discount_amount': 'sum',
        'net_revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    channel_perf.columns = ['Channel', 'Total Spend', 'Total Revenue', 'Total Conversions']
    
    # Calculate channel-level KPIs
    channel_perf['CPC'] = channel_perf['Total Spend'] / channel_perf['Total Conversions']
    channel_perf['Conversion Rate'] = channel_perf['Total Conversions'] / total_conversions
    channel_perf['ROI'] = (channel_perf['Total Revenue'] - channel_perf['Total Spend']) / channel_perf['Total Spend']
    channel_perf['Avg Order Value'] = channel_perf['Total Revenue'] / channel_perf['Total Conversions']
    
    # Monthly trends
    if 'date' in filtered_df.columns:
        monthly_trends = filtered_df.groupby('month_year').agg({
            'net_revenue': 'sum',
            'discount_amount': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        monthly_trends.columns = ['Month', 'Revenue', 'Spend', 'Conversions']
        monthly_trends['CPC'] = monthly_trends['Spend'] / monthly_trends['Conversions']
        monthly_trends['ROI'] = (monthly_trends['Revenue'] - monthly_trends['Spend']) / monthly_trends['Spend']
        monthly_trends = monthly_trends.sort_values('Month')
    
    # Campaign performance
    if 'marketing_campaign' in filtered_df.columns:
        campaign_perf = filtered_df.groupby('marketing_campaign').agg({
            'net_revenue': 'sum',
            'discount_amount': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        campaign_perf.columns = ['Campaign', 'Revenue', 'Spend', 'Conversions']
        campaign_perf['ROI'] = (campaign_perf['Revenue'] - campaign_perf['Spend']) / campaign_perf['Spend']
        campaign_perf = campaign_perf.sort_values('ROI', ascending=False)

# Main page header
st.markdown("<h1 class='main-header'>📈 Marketing Analytics Dashboard</h1>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "⚡ Efficiency", "💡 Recommendations"])

with tab1:
    st.markdown("<h2 class='sub-header'>Performance Overview</h2>", unsafe_allow_html=True)
    
    # Display KPIs in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>${:,.0f}</div>".format(total_revenue), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Total Revenue</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>${:,.0f}</div>".format(total_spend), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Total Spend</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>{:,.0f}</div>".format(total_conversions), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Total Conversions</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>{:.2f}%</div>".format(overall_conversion_rate * 100), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Conversion Rate</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Second row of KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>${:.2f}</div>".format(overall_cpc), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Avg. CPC</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col6:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        roi_color = "positive-change" if overall_roi > 0 else "negative-change"
        st.markdown(f"<div class='kpi-value {roi_color}'>{overall_roi:.2f}x</div>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Overall ROI</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col7:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>${:.2f}</div>".format(avg_order_value), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Avg Order Value</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col8:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-value'>{:,.0f}</div>".format(total_orders), unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Total Orders</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Channel Performance Comparison
    st.markdown("<h3 class='sub-header'>Channel Performance Comparison</h3>", unsafe_allow_html=True)
    
    if len(channel_perf) > 0:
        # Create two columns for charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Revenue by Channel
            fig1 = px.bar(
                channel_perf.sort_values('Total Revenue', ascending=False).head(10),
                x='Channel',
                y='Total Revenue',
                title='Total Revenue by Channel',
                color='Total Revenue',
                color_continuous_scale='Blues'
            )
            fig1.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="Revenue ($)",
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with chart_col2:
            # Conversions by Channel
            fig2 = px.bar(
                channel_perf.sort_values('Total Conversions', ascending=False).head(10),
                x='Channel',
                y='Total Conversions',
                title='Total Conversions by Channel',
                color='Total Conversions',
                color_continuous_scale='Greens'
            )
            fig2.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="Conversions",
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # ROI by Channel
        st.markdown("<h4 class='sub-header'>ROI by Channel</h4>", unsafe_allow_html=True)
        
        roi_chart_data = channel_perf[channel_perf['ROI'].notna()].sort_values('ROI', ascending=False)
        
        if len(roi_chart_data) > 0:
            fig3 = px.bar(
                roi_chart_data,
                x='Channel',
                y='ROI',
                title='Return on Investment (ROI) by Channel',
                color='ROI',
                color_continuous_scale='RdYlGn'
            )
            fig3.add_hline(y=0, line_dash="dash", line_color="gray")
            fig3.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="ROI (x)",
                showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Channel Performance Table
        st.markdown("<h4 class='sub-header'>Channel Performance Details</h4>", unsafe_allow_html=True)
        
        # Format the table for display
        display_table = channel_perf.copy()
        display_table['Total Revenue'] = display_table['Total Revenue'].apply(lambda x: f"${x:,.0f}")
        display_table['Total Spend'] = display_table['Total Spend'].apply(lambda x: f"${x:,.0f}")
        display_table['CPC'] = display_table['CPC'].apply(lambda x: f"${x:.2f}")
        display_table['ROI'] = display_table['ROI'].apply(lambda x: f"{x:.2f}x")
        display_table['Avg Order Value'] = display_table['Avg Order Value'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(
            display_table.sort_values('Total Revenue', ascending=False),
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.markdown("<h2 class='sub-header'>Time Trends Analysis</h2>", unsafe_allow_html=True)
    
    if 'monthly_trends' in locals() and len(monthly_trends) > 0:
        # Create two columns for charts
        trend_col1, trend_col2 = st.columns(2)
        
        with trend_col1:
            # Revenue Trend
            fig4 = px.line(
                monthly_trends,
                x='Month',
                y='Revenue',
                title='Monthly Revenue Trend',
                markers=True,
                line_shape='spline'
            )
            fig4.update_traces(line=dict(width=3, color='#3B82F6'))
            fig4.update_layout(
                plot_bgcolor='white',
                xaxis_title="Month",
                yaxis_title="Revenue ($)",
                hovermode='x unified'
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with trend_col2:
            # Conversions Trend
            fig5 = px.line(
                monthly_trends,
                x='Month',
                y='Conversions',
                title='Monthly Conversions Trend',
                markers=True,
                line_shape='spline'
            )
            fig5.update_traces(line=dict(width=3, color='#10B981'))
            fig5.update_layout(
                plot_bgcolor='white',
                xaxis_title="Month",
                yaxis_title="Conversions",
                hovermode='x unified'
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        # ROI Trend
        st.markdown("<h4 class='sub-header'>ROI Trend Over Time</h4>", unsafe_allow_html=True)
        
        fig6 = px.line(
            monthly_trends,
            x='Month',
            y='ROI',
            title='Monthly ROI Trend',
            markers=True,
            line_shape='spline'
        )
        fig6.add_hline(y=0, line_dash="dash", line_color="gray")
        fig6.update_traces(line=dict(width=3, color='#8B5CF6'))
        fig6.update_layout(
            plot_bgcolor='white',
            xaxis_title="Month",
            yaxis_title="ROI (x)",
            hovermode='x unified'
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        # Monthly Performance Table
        st.markdown("<h4 class='sub-header'>Monthly Performance Details</h4>", unsafe_allow_html=True)
        
        # Format the table for display
        monthly_display = monthly_trends.copy()
        monthly_display['Revenue'] = monthly_display['Revenue'].apply(lambda x: f"${x:,.0f}")
        monthly_display['Spend'] = monthly_display['Spend'].apply(lambda x: f"${x:,.0f}")
        monthly_display['CPC'] = monthly_display['CPC'].apply(lambda x: f"${x:.2f}")
        monthly_display['ROI'] = monthly_display['ROI'].apply(lambda x: f"{x:.2f}x")
        
        st.dataframe(
            monthly_display.sort_values('Month', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Insights
        st.markdown("<h4 class='sub-header'>Trend Insights</h4>", unsafe_allow_html=True)
        
        # Calculate month-over-month changes
        if len(monthly_trends) > 1:
            latest_month = monthly_trends.iloc[-1]
            prev_month = monthly_trends.iloc[-2]
            
            revenue_change = ((latest_month['Revenue'] - prev_month['Revenue']) / prev_month['Revenue']) * 100
            conversions_change = ((latest_month['Conversions'] - prev_month['Conversions']) / prev_month['Conversions']) * 100
            roi_change = latest_month['ROI'] - prev_month['ROI']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                change_color = "positive-change" if revenue_change > 0 else "negative-change"
                st.metric(
                    "Revenue Change (MoM)",
                    f"{revenue_change:.1f}%",
                    delta=f"{revenue_change:.1f}%"
                )
            
            with col2:
                change_color = "positive-change" if conversions_change > 0 else "negative-change"
                st.metric(
                    "Conversions Change (MoM)",
                    f"{conversions_change:.1f}%",
                    delta=f"{conversions_change:.1f}%"
                )
            
            with col3:
                change_color = "positive-change" if roi_change > 0 else "negative-change"
                st.metric(
                    "ROI Change (MoM)",
                    f"{roi_change:.2f}x",
                    delta=f"{roi_change:.2f}x"
                )
    else:
        st.info("Monthly trend data is not available for the selected filters.")

with tab3:
    st.markdown("<h2 class='sub-header'>Cost Efficiency Analysis</h2>", unsafe_allow_html=True)
    
    if len(channel_perf) > 0:
        # Efficiency Metrics
        st.markdown("<h3 class='sub-header'>Channel Efficiency Metrics</h3>", unsafe_allow_html=True)
        
        # Create three columns for efficiency charts
        eff_col1, eff_col2, eff_col3 = st.columns(3)
        
        with eff_col1:
            # CPC by Channel
            cpc_data = channel_perf[channel_perf['CPC'].notna()].sort_values('CPC')
            fig7 = px.bar(
                cpc_data.head(10),
                x='Channel',
                y='CPC',
                title='Cost Per Conversion (CPC)',
                color='CPC',
                color_continuous_scale='Reds'
            )
            fig7.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="CPC ($)",
                showlegend=False
            )
            st.plotly_chart(fig7, use_container_width=True)
        
        with eff_col2:
            # Conversion Rate by Channel
            conv_rate_data = channel_perf[channel_perf['Conversion Rate'].notna()].sort_values('Conversion Rate', ascending=False)
            fig8 = px.bar(
                conv_rate_data.head(10),
                x='Channel',
                y='Conversion Rate',
                title='Conversion Rate by Channel',
                color='Conversion Rate',
                color_continuous_scale='Greens'
            )
            fig8.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="Conversion Rate",
                showlegend=False,
                yaxis_tickformat='.1%'
            )
            st.plotly_chart(fig8, use_container_width=True)
        
        with eff_col3:
            # Avg Order Value by Channel
            aov_data = channel_perf[channel_perf['Avg Order Value'].notna()].sort_values('Avg Order Value', ascending=False)
            fig9 = px.bar(
                aov_data.head(10),
                x='Channel',
                y='Avg Order Value',
                title='Average Order Value by Channel',
                color='Avg Order Value',
                color_continuous_scale='Purples'
            )
            fig9.update_layout(
                plot_bgcolor='white',
                xaxis_title="Channel",
                yaxis_title="Avg Order Value ($)",
                showlegend=False
            )
            st.plotly_chart(fig9, use_container_width=True)
        
        # Spend vs Revenue Analysis
        st.markdown("<h4 class='sub-header'>Spend vs Revenue Correlation</h4>", unsafe_allow_html=True)
        
        # Calculate correlation
        correlation_data = channel_perf[['Total Spend', 'Total Revenue', 'Total Conversions']].corr()
        
        # Create correlation heatmap
        fig10 = px.imshow(
            correlation_data,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu',
            title='Correlation Matrix: Spend vs Performance'
        )
        fig10.update_layout(
            plot_bgcolor='white',
            xaxis_title="Metrics",
            yaxis_title="Metrics"
        )
        st.plotly_chart(fig10, use_container_width=True)
        
        # Scatter plot: Spend vs Revenue
        st.markdown("<h4 class='sub-header'>Spend vs Revenue Relationship</h4>", unsafe_allow_html=True)
        
        fig11 = px.scatter(
            channel_perf,
            x='Total Spend',
            y='Total Revenue',
            size='Total Conversions',
            color='ROI',
            hover_name='Channel',
            title='Spend vs Revenue by Channel',
            labels={
                'Total Spend': 'Total Spend ($)',
                'Total Revenue': 'Total Revenue ($)',
                'Total Conversions': 'Conversions',
                'ROI': 'ROI'
            }
        )
        
        # Add trendline
        fig11.add_traces(px.scatter(
            channel_perf,
            x='Total Spend',
            y='Total Revenue',
            trendline="ols"
        ).data[1])
        
        fig11.update_layout(
            plot_bgcolor='white',
            showlegend=False
        )
        st.plotly_chart(fig11, use_container_width=True)
        
        # Efficiency Ranking
        st.markdown("<h4 class='sub-header'>Channel Efficiency Ranking</h4>", unsafe_allow_html=True)
        
        # Create efficiency score (weighted average of normalized metrics)
        efficiency_metrics = channel_perf.copy()
        
        # Normalize metrics (higher is better for all except CPC)
        for col in ['Total Revenue', 'Total Conversions', 'ROI', 'Conversion Rate', 'Avg Order Value']:
            if col in efficiency_metrics.columns and efficiency_metrics[col].notna().any():
                efficiency_metrics[f'{col}_norm'] = (
                    efficiency_metrics[col] - efficiency_metrics[col].min()
                ) / (efficiency_metrics[col].max() - efficiency_metrics[col].min())
        
        # For CPC, lower is better, so invert
        if 'CPC' in efficiency_metrics.columns and efficiency_metrics['CPC'].notna().any():
            efficiency_metrics['CPC_norm'] = 1 - (
                (efficiency_metrics['CPC'] - efficiency_metrics['CPC'].min()) / 
                (efficiency_metrics['CPC'].max() - efficiency_metrics['CPC'].min())
            )
        
        # Calculate efficiency score (simple average of normalized metrics)
        norm_cols = [col for col in efficiency_metrics.columns if col.endswith('_norm')]
        efficiency_metrics['Efficiency Score'] = efficiency_metrics[norm_cols].mean(axis=1)
        
        # Sort by efficiency score
        efficiency_ranking = efficiency_metrics.sort_values('Efficiency Score', ascending=False)
        
        # Display ranking
        rank_display = efficiency_ranking[['Channel', 'Efficiency Score']].head(10)
        rank_display['Efficiency Score'] = rank_display['Efficiency Score'].apply(lambda x: f"{x:.3f}")
        rank_display['Rank'] = range(1, len(rank_display) + 1)
        rank_display = rank_display[['Rank', 'Channel', 'Efficiency Score']]
        
        st.dataframe(
            rank_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Efficiency Insights
        st.markdown("<h4 class='sub-header'>Efficiency Insights</h4>", unsafe_allow_html=True)
        
        if len(efficiency_ranking) > 0:
            top_channel = efficiency_ranking.iloc[0]['Channel']
            bottom_channel = efficiency_ranking.iloc[-1]['Channel']
            
            insights = f"""
            **Key Findings:**
            
            1. **Most Efficient Channel:** **{top_channel}** has the highest overall efficiency score, 
               indicating optimal balance between spend and performance.
            
            2. **Least Efficient Channel:** **{bottom_channel}** shows the lowest efficiency score, 
               suggesting need for optimization or reduced investment.
            
            3. **CPC Analysis:** Channels with lower CPC tend to have better efficiency scores, 
               but must be balanced with conversion quality.
            
            4. **ROI Impact:** High ROI channels may still have low efficiency if they require 
               disproportionate spending to maintain.
            """
            
            st.markdown(insights)
    else:
        st.info("Efficiency data is not available for the selected filters.")

with tab4:
    st.markdown("<h2 class='sub-header'>Recommendations & Insights</h2>", unsafe_allow_html=True)
    
    # Generate insights based on the data
    if len(channel_perf) > 0:
        # Find top performing channels
        top_revenue_channel = channel_perf.loc[channel_perf['Total Revenue'].idxmax()]
        top_roi_channel = channel_perf.loc[channel_perf['ROI'].idxmax()]
        top_conversions_channel = channel_perf.loc[channel_perf['Total Conversions'].idxmax()]
        
        # Find underperforming channels
        if len(channel_perf) > 1:
            bottom_roi_channel = channel_perf.loc[channel_perf['ROI'].idxmin()]
        
        # Calculate budget allocation suggestions
        total_spend_all = channel_perf['Total Spend'].sum()
        
        # Create recommendations
        recommendations = []
        
        # Recommendation 1: Budget reallocation
        if len(channel_perf) > 1:
            roi_variance = channel_perf['ROI'].std() / channel_perf['ROI'].mean()
            if roi_variance > 0.3:  # High variance in ROI
                recommendations.append({
                    'title': 'Optimize Budget Allocation',
                    'description': f"Consider reallocating budget from lower ROI channels to {top_roi_channel['Channel']} which shows {top_roi_channel['ROI']:.2f}x ROI.",
                    'priority': 'High',
                    'impact': 'High'
                })
        
        # Recommendation 2: CPC optimization
        high_cpc_channels = channel_perf[channel_perf['CPC'] > channel_perf['CPC'].median()]
        if len(high_cpc_channels) > 0:
            recommendations.append({
                'title': 'Reduce High CPC',
                'description': f"Channels like {', '.join(high_cpc_channels['Channel'].head(3).tolist())} have above-average CPC. Consider optimizing targeting or creative.",
                'priority': 'Medium',
                'impact': 'Medium'
            })
        
        # Recommendation 3: Conversion rate improvement
        low_cr_channels = channel_perf[channel_perf['Conversion Rate'] < channel_perf['Conversion Rate'].median()]
        if len(low_cr_channels) > 0:
            recommendations.append({
                'title': 'Improve Conversion Rates',
                'description': f"Focus on improving landing pages and user experience for {', '.join(low_cr_channels['Channel'].head(3).tolist())}.",
                'priority': 'Medium',
                'impact': 'High'
            })
        
        # Recommendation 4: Seasonal trends
        if 'monthly_trends' in locals() and len(monthly_trends) > 3:
            seasonal_variance = monthly_trends['Revenue'].std() / monthly_trends['Revenue'].mean()
            if seasonal_variance > 0.2:
                peak_month = monthly_trends.loc[monthly_trends['Revenue'].idxmax(), 'Month']
                low_month = monthly_trends.loc[monthly_trends['Revenue'].idxmin(), 'Month']
                recommendations.append({
                    'title': 'Leverage Seasonal Trends',
                    'description': f"Peak performance in {peak_month}, lowest in {low_month}. Plan campaigns accordingly.",
                    'priority': 'Low',
                    'impact': 'Medium'
                })
        
        # Display recommendations
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"Recommendation {i}: {rec['title']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(rec['description'])
                with col2:
                    st.metric("Priority", rec['priority'])
                    st.metric("Impact", rec['impact'])
        
        # Action Plan
        st.markdown("<h4 class='sub-header'>30-Day Action Plan</h4>", unsafe_allow_html=True)
        
        action_plan = """
        1. **Week 1-2: Optimization Phase**
           - Implement budget reallocation based on ROI analysis
           - A/B test creatives for underperforming channels
           - Review and optimize landing pages
        
        2. **Week 3: Monitoring Phase**
           - Track performance changes daily
           - Adjust bids based on new CPC targets
           - Monitor conversion rate improvements
        
        3. **Week 4: Evaluation Phase**
           - Analyze results vs. previous period
           - Calculate new ROI and efficiency metrics
           - Prepare recommendations for next month
        """
        
        st.markdown(action_plan)
        
        # Key Metrics to Watch
        st.markdown("<h4 class='sub-header'>Key Metrics to Monitor</h4>", unsafe_allow_html=True)
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric(
                "Target ROI",
                f">{top_roi_channel['ROI']:.1f}x",
                "Overall target"
            )
        
        with metrics_col2:
            target_cpc = channel_perf['CPC'].median() * 0.9  # 10% reduction
            st.metric(
                "Target CPC",
                f"${target_cpc:.2f}",
                "10% reduction"
            )
        
        with metrics_col3:
            target_cr = channel_perf['Conversion Rate'].mean() * 1.15  # 15% improvement
            st.metric(
                "Target Conversion Rate",
                f"{target_cr:.1%}",
                "15% improvement"
            )
    
    else:
        st.info("No recommendations available for the selected filters.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748B; font-size: 0.9rem;'>
    📊 Marketing Analytics Dashboard • Data updated: {} • 
    <a href='#' style='color: #3B82F6; text-decoration: none;'>Export Report</a> • 
    <a href='#' style='color: #3B82F6; text-decoration: none;'>Schedule Email</a>
    </div>
    """.format(pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')),
    unsafe_allow_html=True
)
