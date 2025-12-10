# E-Commerce Analytics Dashboard - Jupyter Notebook Version
# ═════════════════════════════════════════════════════════════════════════════

# Cell 1: Load Libraries and Data
# ─────────────────────────────────────────────────────────────────────────────

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# تحميل البيانات
df = pd.read_csv('cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])

print("✅ تم تحميل البيانات بنجاح!")
print(f"📊 عدد الصفوف: {len(df):,}")
print(f"📅 نطاق التاريخ: {df['date'].min().date()} إلى {df['date'].max().date()}")
print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 2: KPI Overview
# ─────────────────────────────────────────────────────────────────────────────

print("\n🎯 KEY PERFORMANCE INDICATORS (KPIs)")
print("="*70)

total_revenue = df['net_revenue'].sum()
total_customers = df['customer_id'].nunique()
avg_order_value = df['final_amount'].mean()
avg_satisfaction = df['satisfaction_rating'].mean()
total_orders = len(df)
conversion_rate = (total_customers / total_orders * 100) if total_orders > 0 else 0
return_rate = (df['returned'].sum() / len(df) * 100) if len(df) > 0 else 0
avg_roi = df['roi'].replace([np.inf, -np.inf], np.nan).mean()

kpis = pd.DataFrame({
    '📊 Metric': [
        '💰 Total Revenue',
        '👥 Total Customers',
        '📦 Avg Order Value',
        '⭐ Satisfaction Rating',
        '📋 Total Orders',
        '📊 Conversion Rate',
        '🔄 Return Rate',
        '📈 Avg ROI'
    ],
    '📈 Value': [
        f"${total_revenue:,.0f}",
        f"{total_customers:,}",
        f"${avg_order_value:,.2f}",
        f"{avg_satisfaction:.2f}/5",
        f"{total_orders:,}",
        f"{conversion_rate:.2f}%",
        f"{return_rate:.2f}%",
        f"{avg_roi:.2f}x"
    ]
})

print(kpis.to_string(index=False))
print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 3: Channel Performance
# ─────────────────────────────────────────────────────────────────────────────

print("\n📢 MARKETING CHANNEL PERFORMANCE")
print("="*70)

channel_stats = df.groupby('marketing_channel').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique',
    'final_amount': 'mean'
}).sort_values('net_revenue', ascending=False)

channel_stats.columns = ['Revenue', 'Customers', 'Avg Order Value']
print(channel_stats)

# Chart 1: Revenue by Channel
fig1 = px.bar(
    x=channel_stats.index,
    y=channel_stats['Revenue'],
    title='💰 Revenue by Marketing Channel',
    labels={'x': 'Channel', 'y': 'Revenue ($)'},
    color=channel_stats['Revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig1.update_layout(
    height=400,
    showlegend=False,
    hovermode='x unified'
)
fig1.show()

# Chart 2: Customer Distribution by Channel (Pie)
fig2 = px.pie(
    values=channel_stats['Customers'],
    names=channel_stats.index,
    title='👥 Customer Distribution by Channel'
)
fig2.update_layout(height=400)
fig2.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 4: Campaign Analysis
# ─────────────────────────────────────────────────────────────────────────────

print("\n🎪 MARKETING CAMPAIGN PERFORMANCE")
print("="*70)

campaign_stats = df.groupby('marketing_campaign').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False)

campaign_stats.columns = ['Revenue', 'Customers']
print(campaign_stats)

# Chart 3: Revenue by Campaign (Bar)
fig3 = px.bar(
    x=campaign_stats.index,
    y=campaign_stats['Revenue'],
    title='💰 Revenue by Campaign',
    labels={'x': 'Campaign', 'y': 'Revenue ($)'},
    color=campaign_stats['Revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig3.update_layout(
    height=400,
    showlegend=False,
    xaxis_tickangle=-45
)
fig3.show()

# Chart 4: Campaign Revenue Distribution (Pie)
fig4 = px.pie(
    values=campaign_stats['Revenue'],
    names=campaign_stats.index,
    title='📊 Revenue Distribution by Campaign'
)
fig4.update_layout(height=400)
fig4.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 5: Regional Analysis
# ─────────────────────────────────────────────────────────────────────────────

print("\n🗺️ REGIONAL PERFORMANCE")
print("="*70)

region_stats = df.groupby('region').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False)

region_stats.columns = ['Revenue', 'Customers']
print(region_stats)

# Chart 5: Revenue by Region (Bar)
fig5 = px.bar(
    x=region_stats.index,
    y=region_stats['Revenue'],
    title='💰 Revenue by Region',
    labels={'x': 'Region', 'y': 'Revenue ($)'},
    color=region_stats['Revenue'],
    color_continuous_scale=['#3647F5', '#FF9F0D']
)
fig5.update_layout(height=400, showlegend=False)
fig5.show()

# Chart 6: Region Revenue Distribution (Pie)
fig6 = px.pie(
    values=region_stats['Revenue'],
    names=region_stats.index,
    title='📊 Revenue Distribution by Region'
)
fig6.update_layout(height=400)
fig6.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 6: Customer Segment Analysis
# ─────────────────────────────────────────────────────────────────────────────

print("\n👥 CUSTOMER SEGMENT ANALYSIS")
print("="*70)

segment_stats = df.groupby('customer_segment').agg({
    'net_revenue': 'sum',
    'customer_lifetime_value': 'mean',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False)

segment_stats.columns = ['Revenue', 'Avg CLV', 'Customers']
print(segment_stats)

# Chart 7: Revenue by Segment (Bar)
fig7 = px.bar(
    x=segment_stats.index,
    y=segment_stats['Revenue'],
    title='💰 Revenue by Customer Segment',
    labels={'x': 'Segment', 'y': 'Revenue ($)'},
    color=segment_stats['Revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig7.update_layout(height=400, showlegend=False)
fig7.show()

# Chart 8: CLV by Segment (Bar)
fig8 = px.bar(
    x=segment_stats.index,
    y=segment_stats['Avg CLV'],
    title='💎 Customer Lifetime Value by Segment',
    labels={'x': 'Segment', 'y': 'Avg CLV ($)'},
    color=segment_stats['Avg CLV'],
    color_continuous_scale=['#3647F5', '#FF9F0D']
)
fig8.update_layout(height=400, showlegend=False)
fig8.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 7: Monthly Trends
# ─────────────────────────────────────────────────────────────────────────────

print("\n📅 MONTHLY TRENDS")
print("="*70)

monthly_data = df.groupby(df['date'].dt.to_period('M')).agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique',
    'final_amount': 'mean'
}).reset_index()
monthly_data['date'] = monthly_data['date'].astype(str)
monthly_data.columns = ['Date', 'Revenue', 'Customers', 'Avg Order Value']

print(monthly_data.to_string(index=False))

# Chart 9: Monthly Revenue Trend (Line)
fig9 = px.line(
    monthly_data,
    x='Date',
    y='Revenue',
    markers=True,
    title='📈 Monthly Revenue Trend',
    labels={'Date': 'Month', 'Revenue': 'Revenue ($)'}
)
fig9.update_traces(line=dict(color='#FF9F0D', width=3), marker=dict(size=8, color='#3647F5'))
fig9.update_layout(height=400, hovermode='x unified')
fig9.show()

# Chart 10: Monthly Customer Growth (Line)
fig10 = px.line(
    monthly_data,
    x='Date',
    y='Customers',
    markers=True,
    title='👥 Monthly Customer Growth',
    labels={'Date': 'Month', 'Customers': 'Number of Customers'}
)
fig10.update_traces(line=dict(color='#3647F5', width=3), marker=dict(size=8, color='#FF9F0D'))
fig10.update_layout(height=400, hovermode='x unified')
fig10.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 8: Category Analysis
# ─────────────────────────────────────────────────────────────────────────────

print("\n📦 PRODUCT CATEGORY PERFORMANCE")
print("="*70)

category_stats = df.groupby('category').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False).head(10)

category_stats.columns = ['Revenue', 'Customers']
print(category_stats)

# Chart 11: Top 10 Categories (Horizontal Bar)
fig11 = px.bar(
    x=category_stats['Revenue'],
    y=category_stats.index,
    orientation='h',
    title='💰 Top 10 Categories by Revenue',
    labels={'x': 'Revenue ($)', 'y': 'Category'},
    color=category_stats['Revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig11.update_layout(height=500, showlegend=False)
fig11.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 9: Seasonal Analysis
# ─────────────────────────────────────────────────────────────────────────────

print("\n🌡️ SEASONAL PERFORMANCE")
print("="*70)

season_stats = df.groupby('season').agg({
    'net_revenue': 'sum',
    'customer_id': 'nunique'
}).sort_values('net_revenue', ascending=False)

season_stats.columns = ['Revenue', 'Customers']
print(season_stats)

# Chart 12: Revenue by Season (Bar)
fig12 = px.bar(
    x=season_stats.index,
    y=season_stats['Revenue'],
    title='💰 Revenue by Season',
    labels={'x': 'Season', 'y': 'Revenue ($)'},
    color=season_stats['Revenue'],
    color_continuous_scale=['#FF9F0D', '#3647F5']
)
fig12.update_layout(height=400, showlegend=False)
fig12.show()

print("\n" + "="*70)

# ═════════════════════════════════════════════════════════════════════════════
# Cell 10: Key Insights & Recommendations
# ─────────────────────────────────────────────────────────────────────────────

print("\n💡 KEY INSIGHTS & RECOMMENDATIONS")
print("="*70)

best_channel = channel_stats['Revenue'].idxmax()
best_channel_revenue = channel_stats.loc[best_channel, 'Revenue']

best_campaign = campaign_stats['Revenue'].idxmax()
best_campaign_revenue = campaign_stats.loc[best_campaign, 'Revenue']

best_segment = segment_stats['Revenue'].idxmax()
best_segment_revenue = segment_stats.loc[best_segment, 'Revenue']

best_region = region_stats['Revenue'].idxmax()
best_region_revenue = region_stats.loc[best_region, 'Revenue']

best_category = category_stats['Revenue'].idxmax()
best_category_revenue = category_stats.loc[best_category, 'Revenue']

best_season = season_stats['Revenue'].idxmax()
best_season_revenue = season_stats.loc[best_season, 'Revenue']

insights = pd.DataFrame({
    '🏆 Top Performer': [
        f'🥇 Channel: {best_channel}',
        f'🎯 Campaign: {best_campaign}',
        f'👑 Segment: {best_segment}',
        f'🗺️ Region: {best_region}',
        f'📦 Category: {best_category}',
        f'🌡️ Season: {best_season}'
    ],
    '💰 Revenue': [
        f"${best_channel_revenue:,.0f}",
        f"${best_campaign_revenue:,.0f}",
        f"${best_segment_revenue:,.0f}",
        f"${best_region_revenue:,.0f}",
        f"${best_category_revenue:,.0f}",
        f"${best_season_revenue:,.0f}"
    ]
})

print("\n📊 TOP PERFORMERS:")
print(insights.to_string(index=False))

print("\n\n📌 RECOMMENDATIONS:")
recommendations = f"""
1. ✅ Focus on Top Performers
   → Allocate more budget to {best_channel}, which generated ${best_channel_revenue:,.0f}
   
2. 🎯 Segment Strategy
   → Develop loyalty programs for {best_segment} segment
   → Average CLV: ${segment_stats.loc[best_segment, 'Avg CLV']:,.0f}
   
3. 📅 Seasonal Planning
   → Plan inventory around {best_season} season
   → Revenue peak: ${best_season_revenue:,.0f}
   
4. 🗺️ Regional Expansion
   → Strengthen {best_region} region (Top revenue region)
   → Revenue: ${best_region_revenue:,.0f}
   
5. 📦 Category Focus
   → Promote {best_category} category
   → Revenue: ${best_category_revenue:,.0f}
   
6. 💡 Quality Improvement
   → Monitor customer satisfaction metrics
   → Current average rating: {avg_satisfaction:.2f}/5
"""

print(recommendations)

print("\n" + "="*70)
print(f"✨ Dashboard Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)
