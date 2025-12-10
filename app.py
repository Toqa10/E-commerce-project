# app.py
# Streamlit Marketing / E‑commerce Dashboard
# مبني على cleaned_data.csv و نفس تحليلات النوتبوك

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ----------------- إعداد الصفحة العامة -----------------
st.set_page_config(
    page_title="NexaVerse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- CSS لتقليد شكل الصورة -----------------
st.markdown(
    """
    <style>
    /* خلفية عامة فاتحة */
    body {
        background-color: #f3f4f6;
    }
    .main {
        background-color: #f3f4f6;
    }

    /* Sidebar رمادي فاتح مع لوجو وقائمة */
    section[data-testid="stSidebar"] {
        background-color: #e5e7eb;
        padding-top: 1rem;
    }
    .sidebar-logo {
        font-weight: 800;
        font-size: 20px;
        margin-bottom: 1.5rem;
        color: #111827;
    }
    .sidebar-menu-item {
        font-size: 14px;
        padding: 4px 0;
        color: #111827;
    }

    /* هيدر الداشبورد + السيرش */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .dash-title {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
    }
    .dash-subtitle {
        font-size: 13px;
        color: #6b7280;
    }
    .search-box input {
        border-radius: 999px !important;
        border: 1px solid #d1d5db !important;
        padding-left: 14px !important;
        background-color: #f9fafb !important;
    }

    /* كروت KPIs */
    .kpi-card {
        border-radius: 12px;
        padding: 16px 18px;
        color: #f9fafb;
    }
    .kpi-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #e5e7eb;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #e5e7eb;
        margin-top: 4px;
    }
    .kpi-blue     { background-color: #1d4ed8; }
    .kpi-amber    { background-color: #f59e0b; }
    .kpi-indigo   { background-color: #4f46e5; }
    .kpi-sky      { background-color: #0ea5e9; }

    /* Cards داخل الصفحة (زي البوكسات في الصورة) */
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(15,23,42,0.08);
    }
    .card-title {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.25rem;
    }
    .card-subtitle {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 0.75rem;
    }

    /* Tabs بشكل قريب من التصميم */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        margin-top: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e5e7eb;
        color: #4b5563;
        border-radius: 8px 8px 0 0;
        padding-top: 6px;
        padding-bottom: 6px;
        font-size: 13px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #111827;
        border-bottom: 2px solid #0f766e;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- تحميل الداتا النهائية -----------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        st.error(f"لم أجد الملف {path} – ضعي cleaned_data.csv في نفس فولدر app.py.")
        st.stop()
    df = pd.read_csv(path)

    # تحويل التاريخ وعمود شهر-سنة
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["year_month"] = df["date"].dt.to_period("M").astype(str)
    else:
        df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

    return df


df_raw = load_data("cleaned_data.csv")  # الأعمدة حسب الملف المرفوع


# ----------------- تجهيز الأعمدة المحسوبة (KPIs) -----------------
def add_kpi_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Revenue = final_amount (أو gross_revenue لو حابة تغيريها)
    df["revenue"] = df["final_amount"]

    # Marketing Spend (افتراض 20٪ من قيمة السلعة * الكمية = تكلفة الإعلانات)
    df["marketing_spend"] = df["price"] * df["quantity"] * 0.2

    # Clicks / Visits مبنية على quantity زي ما عاملين scaling في النوتبوك
    df["clicks"] = df["quantity"] * 50
    df["visits"] = df["quantity"] * 100

    # CTR – نسبة النقرات من الزيارات
    df["CTR"] = np.where(df["visits"] > 0, df["clicks"] / df["visits"], np.nan)

    # CPC – تكلفة النقرة
    df["CPC"] = np.where(df["clicks"] > 0, df["marketing_spend"] / df["clicks"], np.nan)

    # Conversion = عدد الطلبات (تقدير لكل صف = 1)
    df["conversions"] = 1

    # Conversion Rate – مقابل الزيارات
    df["Conversion_Rate"] = np.where(
        df["visits"] > 0, df["conversions"] / df["visits"], np.nan
    )

    # ROI – عائد الاستثمار
    df["ROI"] = np.where(
        df["marketing_spend"] > 0,
        (df["revenue"] - df["marketing_spend"]) / df["marketing_spend"],
        np.nan,
    )

    return df


df = add_kpi_columns(df_raw)

# ----------------- Sidebar: Logo + Filters (Drop-down) -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">NexaVerse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">Efficiency</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">Recommendations</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Filter by channel
    channel_col = "marketing_channel"
    channels = sorted(df[channel_col].dropna().unique())
    channel_options = ["All Channels"] + channels
    selected_channel = st.selectbox("Channel", channel_options)

    # Filter by month range (Start / End) – Drop-down
    months = sorted(df["year_month"].unique())
    start_month = st.selectbox("Start month", months, index=0)
    end_month = st.selectbox("End month", months, index=len(months) - 1)

# تطبيق الفلاتر
df_f = df.copy()

if selected_channel != "All Channels":
    df_f = df_f[df_f[channel_col] == selected_channel]

df_f = df_f[(df_f["year_month"] >= start_month) & (df_f["year_month"] <= end_month)]

# ----------------- Header + Search Bar -----------------
top_left, top_right = st.columns([3, 2])

with top_left:
    st.markdown(
        """
        <div class="top-bar">
          <div>
            <div class="dash-title">Dashboard</div>
            <div class="dash-subtitle">Marketing performance overview for the selected period</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    st.text_input("Search transactions, customers, subscriptions", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- KPIs أعلى الصفحة (أربع كروت زي الصورة) -----------------
total_revenue = df_f["revenue"].sum()
total_spend = df_f["marketing_spend"].sum()
unique_customers = df_f["customer_id"].nunique()
churn_rate = (df_f["returned"].astype(str) == "True").mean() if "returned" in df_f.columns else np.nan
active_customers_pct = df_f["retention_score"].mean() / 100 if "retention_score" in df_f.columns else np.nan
avg_roi = df_f["ROI"].mean()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-blue">
          <div class="kpi-label">Total Revenue</div>
          <div class="kpi-value">${total_revenue:,.0f}</div>
          <div class="kpi-sub">All orders in filter</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-amber">
          <div class="kpi-label">Marketing Spend</div>
          <div class="kpi-value">${total_spend:,.0f}</div>
          <div class="kpi-sub">Estimated ad cost</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card kpi-indigo">
          <div class="kpi-label">Active Customers</div>
          <div class="kpi-value">{active_customers_pct*100:,.1f}%</div>
          <div class="kpi-sub">Avg retention score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card kpi-sky">
          <div class="kpi-label">Churn / Returns</div>
          <div class="kpi-value">{churn_rate*100:,.1f}%</div>
          <div class="kpi-sub">Returned orders share</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ----------------- Tabs: Overview – Trends – Efficiency – Recommendations -----------------
tab_overview, tab_trends, tab_eff, tab_recs = st.tabs(
    ["Overview", "Trends", "Efficiency", "Recommendations"]
)

# ================= OVERVIEW TAB =================
with tab_overview:
    # صف علوي: Trend + Sales Donut + Transactions (قريب من الصورة)
    left_big, right_small = st.columns([2, 1])

    # Trend (Revenue by month & channel)
    with left_big:
        with st.container():
            st.markdown('<div class="card"><div class="card-title">Revenue Trend</div>', unsafe_allow_html=True)

            monthly_trend = (
                df_f.groupby(["year_month", channel_col])
                .agg(revenue=("revenue", "sum"))
                .reset_index()
                .sort_values("year_month")
            )

            fig_trend = px.bar(
                monthly_trend,
                x="year_month",
                y="revenue",
                color=channel_col,
                barmode="group",
                title="",
            )
            fig_trend.update_layout(
                height=320,
                margin=dict(l=10, r=10, t=10, b=10),
                legend_title_text="Channel",
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Sales Donut + Top Channels
    with right_small:
        with st.container():
            st.markdown(
                '<div class="card"><div class="card-title">Sales by Channel</div>',
                unsafe_allow_html=True,
            )
            channel_perf = (
                df_f.groupby(channel_col)
                .agg(revenue=("revenue", "sum"))
                .reset_index()
                .sort_values("revenue", ascending=False)
            )
            if not channel_perf.empty:
                fig_donut = go.Figure(
                    data=[
                        go.Pie(
                            labels=channel_perf[channel_col],
                            values=channel_perf["revenue"],
                            hole=0.65,
                        )
                    ]
                )
                fig_donut.update_layout(
                    height=260,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=True,
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")

    # صف تاني: Channel performance table (Member 2)
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Channel performance summary</div>
              <div class="card-subtitle">
                Total Spend, Revenue, Conversions and average ROI per channel.
              </div>
            """,
            unsafe_allow_html=True,
        )

        channel_summary = (
            df_f.groupby(channel_col)
            .agg(
                Total_Spend=("marketing_spend", "sum"),
                Total_Revenue=("revenue", "sum"),
                Total_Conversions=("conversions", "sum"),
                Avg_ROI=("ROI", "mean"),
            )
            .reset_index()
        )
        st.dataframe(
            channel_summary.sort_values("Total_Revenue", ascending=False),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ================= TRENDS TAB (Member 3) =================
with tab_trends:
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Monthly trends by channel</div>
              <div class="card-subtitle">Revenue and conversions by month for each marketing channel.</div>
            """,
            unsafe_allow_html=True,
        )

        monthly_ch = (
            df_f.groupby(["year_month", channel_col])
            .agg(
                revenue=("revenue", "sum"),
                conversions=("conversions", "sum"),
            )
            .reset_index()
            .sort_values("year_month")
        )

        c1, c2 = st.columns(2)

        with c1:
            fig_rev_ch = px.line(
                monthly_ch,
                x="year_month",
                y="revenue",
                color=channel_col,
                markers=True,
                title="Revenue by month & channel",
            )
            fig_rev_ch.update_layout(height=320, xaxis_title="", yaxis_title="Revenue")
            st.plotly_chart(fig_rev_ch, use_container_width=True)

        with c2:
            fig_conv_ch = px.line(
                monthly_ch,
                x="year_month",
                y="conversions",
                color=channel_col,
                markers=True,
                title="Conversions by month & channel",
            )
            fig_conv_ch.update_layout(height=320, xaxis_title="", yaxis_title="Conversions")
            st.plotly_chart(fig_conv_ch, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Overall trends (كل القنوات مع بعض)
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Overall trends</div>
              <div class="card-subtitle">Total monthly revenue and conversions across all channels.</div>
            """,
            unsafe_allow_html=True,
        )

        monthly_total = (
            df_f.groupby("year_month")
            .agg(
                total_revenue=("revenue", "sum"),
                total_conversions=("conversions", "sum"),
            )
            .reset_index()
            .sort_values("year_month")
        )

        c3, c4 = st.columns(2)

        with c3:
            fig_tot_rev = px.line(
                monthly_total,
                x="year_month",
                y="total_revenue",
                markers=True,
                title="Overall monthly revenue",
            )
            fig_tot_rev.update_layout(height=300, xaxis_title="", yaxis_title="Revenue")
            st.plotly_chart(fig_tot_rev, use_container_width=True)

        with c4:
            fig_tot_conv = px.line(
                monthly_total,
                x="year_month",
                y="total_conversions",
                markers=True,
                title="Overall monthly conversions",
            )
            fig_tot_conv.update_layout(height=300, xaxis_title="", yaxis_title="Conversions")
            st.plotly_chart(fig_tot_conv, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ================= EFFICIENCY TAB (Member 4) =================
with tab_eff:
    # 1) Cost efficiency: CPC & Conversion Rate & Ranking
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Cost efficiency by channel</div>
              <div class="card-subtitle">
                CPC, Conversion Rate and combined efficiency score (عالي = قناة أكثر كفاءة).
              </div>
            """,
            unsafe_allow_html=True,
        )

        eff = (
            df_f.groupby(channel_col)
            .agg(
                Avg_CPC=("CPC", "mean"),
                Avg_ConvRate=("Conversion_Rate", "mean"),
                Total_Spend=("marketing_spend", "sum"),
                Total_Revenue=("revenue", "sum"),
            )
            .reset_index()
        )

        # نفس فكرة EfficiencyScore في النوتبوك: معدل تحويل أعلى وCPC أقل = أفضل
        eff["Efficiency_Score"] = (
            (eff["Avg_ConvRate"] / eff["Avg_CPC"]) * 1000
        ).round(2)

        c1, c2 = st.columns(2)

        with c1:
            fig_cpc = px.bar(
                eff.sort_values("Avg_CPC"),
                x="Avg_CPC",
                y=channel_col,
                title="Average CPC by channel",
                orientation="h",
                color="Avg_CPC",
                color_continuous_scale=["#3647F5", "#D9D9D9", "#FF9F0D"],
            )
            fig_cpc.update_layout(height=320, xaxis_title="CPC", yaxis_title="")
            st.plotly_chart(fig_cpc, use_container_width=True)

        with c2:
            fig_conv = px.bar(
                eff.sort_values("Avg_ConvRate", ascending=False),
                x=channel_col,
                y="Avg_ConvRate",
                title="Conversion Rate by channel",
                color="Avg_ConvRate",
                color_continuous_scale=["#3647F5", "#D9D9D9", "#FF9F0D"],
            )
            fig_conv.update_layout(height=320, xaxis_title="", yaxis_title="Conv. rate")
            st.plotly_chart(fig_conv, use_container_width=True)

        # Ranking
        eff_rank = eff.sort_values("Efficiency_Score", ascending=False).reset_index(drop=True)
        eff_rank["Rank"] = np.arange(1, len(eff_rank) + 1)
        fig_rank = px.bar(
            eff_rank.sort_values("Efficiency_Score"),
            x="Efficiency_Score",
            y=channel_col,
            orientation="h",
            color="Efficiency_Score",
            title="Channel efficiency ranking",
            color_continuous_scale=["#3647F5", "#D9D9D9", "#FF9F0D"],
        )
        fig_rank.update_layout(height=320, xaxis_title="Efficiency score", yaxis_title="")
        st.plotly_chart(fig_rank, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 2) Spend impact: Spend vs Revenue / Conversions + Correlations
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Spend impact & correlations</div>
              <div class="card-subtitle">
                علاقة حجم الإنفاق مع الإيراد والتحويلات + معاملات الارتباط.
              </div>
            """,
            unsafe_allow_html=True,
        )

        # تجميع per channel لتحليل الإنفاق
        spend_rev = (
            df_f.groupby(channel_col)
            .agg(
                Total_Spend=("marketing_spend", "sum"),
                Total_Revenue=("revenue", "sum"),
                Total_Conversions=("conversions", "sum"),
            )
            .reset_index()
        )
        spend_rev["Rev_to_Spend"] = spend_rev["Total_Revenue"] / spend_rev["Total_Spend"]

        c3, c4 = st.columns(2)

        with c3:
            fig_sr = px.scatter(
                spend_rev,
                x="Total_Spend",
                y="Total_Revenue",
                size="Rev_to_Spend",
                color="Rev_to_Spend",
                hover_name=channel_col,
                color_continuous_scale=["#FF9F0D", "#3647F5", "#D9D9D9"],
                title="Spend vs Revenue by channel",
            )
            fig_sr.update_layout(height=320, xaxis_title="Total spend", yaxis_title="Total revenue")
            st.plotly_chart(fig_sr, use_container_width=True)

        with c4:
            spend_conv = spend_rev.copy()
            spend_conv["Spend_per_Conversion"] = (
                spend_conv["Total_Spend"] / spend_conv["Total_Conversions"]
            )
            fig_spc = px.bar(
                spend_conv.sort_values("Spend_per_Conversion"),
                x=channel_col,
                y="Spend_per_Conversion",
                color="Spend_per_Conversion",
                color_continuous_scale=["#3647F5", "#D9D9D9", "#FF9F0D"],
                title="Cost per conversion by channel",
            )
            fig_spc.update_layout(height=320, xaxis_title="", yaxis_title="Spend per conversion")
            st.plotly_chart(fig_spc, use_container_width=True)

        # Correlations (Spend / Revenue / Conversions / CPC)
        corr_df = spend_rev[
            ["Total_Spend", "Total_Revenue", "Total_Conversions"]
        ].copy()
        corr_df["Avg_CPC"] = eff.set_index(channel_col)["Avg_CPC"].reindex(
            spend_rev[channel_col]
        ).values
        corr_matrix = corr_df.corr().round(3)

        st.markdown("#### Correlation matrix")
        st.dataframe(corr_matrix, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ================= RECOMMENDATIONS TAB (Member 4 summary) =================
with tab_recs:
    with st.container():
        st.markdown(
            """
            <div class="card">
              <div class="card-title">Automated recommendations</div>
              <div class="card-subtitle">
                ملخص لأفضل وأسوأ القنوات + تأثير الإنفاق بناءً على المقاييس اللي فوق.
              </div>
            """,
            unsafe_allow_html=True,
        )

        # استخدام eff_rank و spend_rev من تاب الكفاءة (نحسبهم تاني هنا عشان الاستقلالية)
        eff_local = (
            df_f.groupby(channel_col)
            .agg(
                Avg_CPC=("CPC", "mean"),
                Avg_ConvRate=("Conversion_Rate", "mean"),
            )
            .reset_index()
        )
        eff_local["Efficiency_Score"] = (
            (eff_local["Avg_ConvRate"] / eff_local["Avg_CPC"]) * 1000
        ).round(2)
        eff_rank_local = eff_local.sort_values("Efficiency_Score", ascending=False).reset_index(
            drop=True
        )

        spend_rev_local = (
            df_f.groupby(channel_col)
            .agg(
                Total_Spend=("marketing_spend", "sum"),
                Total_Revenue=("revenue", "sum"),
                Total_Conversions=("conversions", "sum"),
            )
            .reset_index()
        )
        spend_rev_local["Rev_to_Spend"] = (
            spend_rev_local["Total_Revenue"] / spend_rev_local["Total_Spend"]
        )

        best_eff = eff_rank_local.head(1).iloc[0]
        worst_eff = eff_rank_local.tail(1).iloc[0]
        best_roi = spend_rev_local.sort_values("Rev_to_Spend", ascending=False).head(1).iloc[0]
        best_cost_conv = (
            spend_rev_local.assign(
                Spend_per_Conversion=lambda d: d["Total_Spend"] / d["Total_Conversions"]
            )
            .sort_values("Spend_per_Conversion")
            .head(1)
            .iloc[0]
        )

        st.markdown("##### Cost efficiency")
        st.write(
            f"- أفضل قناة كفاءة حاليًا: **{best_eff[channel_col]}** "
            f"(Efficiency Score ≈ {best_eff['Efficiency_Score']:.2f})."
        )
        st.write(
            f"- أضعف قناة كفاءة: **{worst_eff[channel_col]}** "
            f"(Efficiency Score ≈ {worst_eff['Efficiency_Score']:.2f}) – "
            f"محتاجة مراجعة الكريتيف أو تقليل الإنفاق."
        )

        st.markdown("##### Spend impact")
        st.write(
            f"- أعلى عائد على الإنفاق (Revenue/Spend) في قناة **{best_roi[channel_col]}** "
            f"≈ {best_roi['Rev_to_Spend']:.2f}x – مرشح قوي لزيادة الميزانية."
        )
        st.write(
            f"- أقل تكلفة لكل Conversion في قناة **{best_cost_conv[channel_col]}** "
            f"≈ {best_cost_conv['Total_Spend']/best_cost_conv['Total_Conversions']:.2f} "
            f"وهي ممتازة للحملات اللي هدفها تحويلات مباشرة."
        )

        st.markdown("</div>", unsafe_allow_html=True)
