# app.py
# ===============================
# Marketing / E‑commerce Dashboard
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ========= إعداد عام للتطبيق =========
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========= إعداد أسماء الأعمدة (عدّليها حسب داتا مشروعك) =========
COLUMN_CONFIG = {
    "date": "date",                            # تاريخ العملية
    "channel": "marketingchannel",             # قناة التسويق
    "campaign": "marketingcampaign",           # الحملة
    "spend": "netrevenue",                     # أو ad_spend لو عندك عمود منفصل
    "revenue": "grossrevenuenetrevenueroi".split("netrevenue")[0].strip() \
        if "grossrevenue" in [] else "grossrevenue",  # غيّريها لاسم عمود الإيراد
    "impressions": "impressions",              # عدديها لو موجودة
    "clicks": "clicks",                        # عدديها لو موجودة
    "conversions": "conversions",              # أو استخدمي عدد الأوردرز
    "order_id": "orderid",
    "region": "region",
    "city": "city",
}

# لو الأعمدة مش موجودة بالأسماء دي في cleaned_data.csv عدّلي القيم فوق قبل التشغيل.


# ========= CSS للتصميم (ألوان وكروت وتابات) =========
st.markdown(
    """
    <style>
    /* خلفية عامة */
    .main {
        background-color: #0f172a;
        color: #f9fafb;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        padding-top: 1rem;
    }
    /* عنوان الداشبورد */
    .dashboard-title {
        font-size: 28px;
        font-weight: 700;
        color: #f9fafb;
        margin-bottom: 0.25rem;
    }
    .dashboard-subtitle {
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }

    /* كروت KPIs */
    .kpi-card {
        border-radius: 12px;
        padding: 16px 18px;
        color: #f9fafb;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .kpi-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #e5e7eb;
        letter-spacing: 0.06em;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
    }
    .kpi-sub {
        font-size: 12px;
        color: #d1d5db;
    }
    .kpi-blue  { background: #1d4ed8; }
    .kpi-amber { background: #f59e0b; }
    .kpi-indigo{ background: #4f46e5; }
    .kpi-rose  { background: #e11d48; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #111827;
        color: #9ca3af;
        border-radius: 8px 8px 0 0;
        padding-top: 8px;
        padding-bottom: 8px;
        font-weight: 600;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f2937;
        color: #f9fafb;
        border-bottom: 2px solid #6366f1;
    }

    /* بطاقات داخل التابات */
    .card {
        background-color: #111827;
        border-radius: 12px;
        padding: 16px 18px;
    }
    .card-title {
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 0.5rem;
        color: #e5e7eb;
    }
    .card-subtitle {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }

    /* إخفاء footer الافتراضي لستريمليت */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ========= تحميل البيانات =========
@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        st.error(f"لم أجد الملف {csv_path} – تأكد أنه في نفس فولدر app.py.")
        st.stop()

    df = pd.read_csv(csv_path)

    # تحويل التاريخ
    date_col = COLUMN_CONFIG["date"]
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])

        if "month" not in df.columns:
            df["month"] = df[date_col].dt.to_period("M").astype(str)

        if "year" not in df.columns:
            df["year"] = df[date_col].dt.year

    return df


df_raw = load_data("cleaned_data.csv")


# ========= تحضير KPIs و الأعمدة المحسوبة =========
def add_calculated_columns(df: pd.DataFrame) -> pd.DataFrame:
    cfg = COLUMN_CONFIG.copy()
    df = df.copy()

    # أسماء الأعمدة
    ch_col  = cfg["channel"]
    rev_col = cfg["revenue"]
    sp_col  = cfg["spend"]
    imp_col = cfg["impressions"]
    clk_col = cfg["clicks"]
    conv_col = cfg["conversions"]

    # تأكّد من وجود أعمدة الإنفاق والإيراد
    if sp_col not in df.columns:
        st.warning(f"عمود الإنفاق '{sp_col}' غير موجود، سيتم افتراض الإنفاق = finalamount.")
        if "finalamount" in df.columns:
            df[sp_col] = df["finalamount"]
        else:
            df[sp_col] = np.nan

    if rev_col not in df.columns:
        if "grossrevenue" in df.columns:
            df[rev_col] = df["grossrevenue"]
        elif "netrevenue" in df.columns:
            df[rev_col] = df["netrevenue"]
        else:
            st.warning("لا يوجد عمود واضح للإيراد، سيتم استخدام finalamount كإيراد.")
            df[rev_col] = df[sp_col]

    # CTR = Clicks / Impressions
    if imp_col in df.columns and clk_col in df.columns:
        df["CTR"] = df[clk_col] / df[imp_col]
    else:
        df["CTR"] = np.nan

    # CPC = Spend / Clicks
    if clk_col in df.columns:
        df["CPC"] = np.where(df[clk_col] > 0, df[sp_col] / df[clk_col], np.nan)
    else:
        df["CPC"] = np.nan

    # Conversion Rate = Conversions / Clicks
    if conv_col in df.columns and clk_col in df.columns:
        df["Conversion_Rate"] = np.where(
            df[clk_col] > 0, df[conv_col] / df[clk_col], np.nan
        )
    else:
        # fallback: اعتبر كل أوردر Conversion
        df["Conversion_Rate"] = 1.0

    # ROI = (Revenue - Spend) / Spend
    df["ROI"] = np.where(
        df[sp_col] > 0,
        (df[rev_col] - df[sp_col]) / df[sp_col],
        np.nan,
    )

    return df


df = add_calculated_columns(df_raw)

# ========= تطبيق الفلاتر (Sidebar) =========
with st.sidebar:
    st.markdown("### NexaVerse")
    st.markdown("لوحة تحكم أداء التسويق والمبيعات")

    ch_col = COLUMN_CONFIG["channel"]
    date_col = COLUMN_CONFIG["date"]

    # Filter by channel
    if ch_col in df.columns:
        all_channels = sorted(df[ch_col].dropna().unique())
        selected_channels = st.multiselect(
            "Marketing Channel",
            options=all_channels,
            default=all_channels,
        )
    else:
        selected_channels = None

    # Filter by month range
    if "month" in df.columns:
        months = sorted(df["month"].unique())
        if months:
            month_range = st.select_slider(
                "Month range",
                options=months,
                value=(months[0], months[-1]),
            )
        else:
            month_range = None
    else:
        month_range = None

    st.markdown("---")
    st.markdown("**ملاحظات:** غيّر أسماء الأعمدة في أعلى الملف لو اختلفت عن داتاسيتك.")

# تطبيق الفلاتر
df_filtered = df.copy()

if selected_channels and ch_col in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[ch_col].isin(selected_channels)]

if month_range and "month" in df_filtered.columns:
    start_m, end_m = month_range
    df_filtered = df_filtered[
        (df_filtered["month"] >= start_m) & (df_filtered["month"] <= end_m)
    ]

# ========= حساب KPIs إجمالية =========
cfg = COLUMN_CONFIG
rev_col = cfg["revenue"]
sp_col = cfg["spend"]

total_revenue = df_filtered[rev_col].sum()
total_spend   = df_filtered[sp_col].sum()
total_orders  = len(df_filtered)
avg_roi       = df_filtered["ROI"].mean(skipna=True)
avg_conv_rate = df_filtered["Conversion_Rate"].mean(skipna=True)

# ========= Header =========
st.markdown('<div class="dashboard-title">Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dashboard-subtitle">Marketing & E‑commerce Performance Overview</div>',
    unsafe_allow_html=True,
)

# ========= كروت KPIs أعلى الصفحة =========
kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.markdown(
        f"""
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${total_revenue:,.0f}</div>
            <div class="kpi-sub">Filtered period</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[1]:
    st.markdown(
        f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">${total_spend:,.0f}</div>
            <div class="kpi-sub">Acquisition & marketing cost</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[2]:
    st.markdown(
        f"""
        <div class="kpi-card kpi-indigo">
            <div class="kpi-label">AVG ROI</div>
            <div class="kpi-value">{avg_roi:,.2f}x</div>
            <div class="kpi-sub">Return on investment</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[3]:
    st.markdown(
        f"""
        <div class="kpi-card kpi-rose">
            <div class="kpi-label">AVG Conversion Rate</div>
            <div class="kpi-value">{avg_conv_rate*100:,.2f}%</div>
            <div class="kpi-sub">Across all channels</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ========= Tabs الرئيسية =========
overview_tab, trends_tab, efficiency_tab, recs_tab = st.tabs(
    ["Overview", "Trends", "Efficiency", "Recommendations"]
)

# -------------------- 1) Overview Tab --------------------
with overview_tab:
    col_left, col_right = st.columns([2, 1])

    # Trend (Revenue by month & channel)
    with col_left:
        if "month" in df_filtered.columns and ch_col in df_filtered.columns:
            trend_df = (
                df_filtered.groupby(["month", ch_col])[rev_col]
                .sum()
                .reset_index()
                .sort_values("month")
            )
            fig_trend = px.bar(
                trend_df,
                x="month",
                y=rev_col,
                color=ch_col,
                barmode="group",
                title="Revenue trend by month & channel",
            )
            fig_trend.update_layout(
                template="plotly_dark",
                height=320,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("لا يوجد عمود month أو channel كافي لبناء ترند.")

    # Sales donut by channel
    with col_right:
        if ch_col in df_filtered.columns:
            channel_rev = (
                df_filtered.groupby(ch_col)[rev_col]
                .sum()
                .reset_index()
                .sort_values(rev_col, ascending=False)
            )
            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=channel_rev[ch_col],
                        values=channel_rev[rev_col],
                        hole=0.6,
                    )
                ]
            )
            fig_donut.update_layout(
                template="plotly_dark",
                title="Revenue share by channel",
                margin=dict(l=0, r=0, t=40, b=0),
                height=320,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("لا يوجد عمود channel لبناء Donut Chart.")

    # جدول معاملات (Top orders)
    st.markdown("### Top Transactions")
    order_col = cfg["order_id"]
    cols_to_show = [
        order_col if order_col in df_filtered.columns else df_filtered.columns[0],
        date_col if date_col in df_filtered.columns else None,
        ch_col if ch_col in df_filtered.columns else None,
        rev_col,
        sp_col,
        "ROI",
        "Conversion_Rate",
    ]
    cols_to_show = [c for c in cols_to_show if c and c in df_filtered.columns]

    st.dataframe(
        df_filtered.sort_values(rev_col, ascending=False)[cols_to_show].head(15),
        use_container_width=True,
        height=350,
    )

# -------------------- 2) Trends Tab --------------------
with trends_tab:
    st.markdown('<div class="card"><div class="card-title">Time trends</div>', unsafe_allow_html=True)

    if "month" in df_filtered.columns and ch_col in df_filtered.columns:
        monthly = (
            df_filtered.groupby(["month", ch_col])
            .agg(
                revenue=(rev_col, "sum"),
                spend=(sp_col, "sum"),
                avg_roi=("ROI", "mean"),
            )
            .reset_index()
            .sort_values("month")
        )

        c1, c2 = st.columns(2)

        with c1:
            fig_rev = px.line(
                monthly,
                x="month",
                y="revenue",
                color=ch_col,
                markers=True,
                title="Monthly revenue by channel",
            )
            fig_rev.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_rev, use_container_width=True)

        with c2:
            fig_roi = px.line(
                monthly,
                x="month",
                y="avg_roi",
                color=ch_col,
                markers=True,
                title="Monthly ROI by channel",
            )
            fig_roi.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_roi, use_container_width=True)

    else:
        st.info("يلزم وجود month و channel لتحليل الترند الزمني.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 3) Efficiency Tab --------------------
with efficiency_tab:
    st.markdown('<div class="card"><div class="card-title">Cost efficiency</div>', unsafe_allow_html=True)

    if ch_col in df_filtered.columns:
        eff = (
            df_filtered.groupby(ch_col)
            .agg(
                total_spend=(sp_col, "sum"),
                total_revenue=(rev_col, "sum"),
                avg_cpc=("CPC", "mean"),
                avg_ctr=("CTR", "mean"),
                avg_conv=("Conversion_Rate", "mean"),
                avg_roi=("ROI", "mean"),
            )
            .reset_index()
        )

        c1, c2 = st.columns(2)

        with c1:
            fig_cpc = px.bar(
                eff.sort_values("avg_cpc"),
                x=ch_col,
                y="avg_cpc",
                title="Average CPC by channel",
                color=ch_col,
            )
            fig_cpc.update_layout(template="plotly_dark", height=320, showlegend=False)
            st.plotly_chart(fig_cpc, use_container_width=True)

        with c2:
            fig_conv = px.bar(
                eff.sort_values("avg_conv", ascending=False),
                x=ch_col,
                y="avg_conv",
                title="Conversion rate by channel",
                color=ch_col,
            )
            fig_conv.update_layout(template="plotly_dark", height=320, showlegend=False)
            st.plotly_chart(fig_conv, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">Spend impact & correlations</div>', unsafe_allow_html=True)

        # Scatter Spend vs Revenue / Conversions
        c3, c4 = st.columns(2)

        with c3:
            fig_sr = px.scatter(
                df_filtered,
                x=sp_col,
                y=rev_col,
                color=ch_col if ch_col in df_filtered.columns else None,
                trendline="ols",
                title="Spend vs Revenue",
            )
            fig_sr.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_sr, use_container_width=True)

        conv_col = cfg["conversions"]
        if conv_col in df_filtered.columns:
            with c4:
                fig_sc = px.scatter(
                    df_filtered,
                    x=sp_col,
                    y=conv_col,
                    color=ch_col if ch_col in df_filtered.columns else None,
                    trendline="ols",
                    title="Spend vs Conversions",
                )
                fig_sc.update_layout(template="plotly_dark", height=320)
                st.plotly_chart(fig_sc, use_container_width=True)

        # Correlation table
        numeric_cols = [c for c in [sp_col, rev_col, conv_col] if c in df_filtered.columns]
        corr_df = df_filtered[numeric_cols].corr().round(3)
        st.markdown("#### Correlation matrix")
        st.dataframe(corr_df, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("لا يوجد عمود channel لإجراء تحليل الكفاءة.")

# -------------------- 4) Recommendations Tab --------------------
with recs_tab:
    st.markdown(
        '<div class="card"><div class="card-title">Automatic recommendations</div>'
        '<div class="card-subtitle">ملخص لأداء القنوات والفترات بناءً على ROI و Conversion Rate.</div>',
        unsafe_allow_html=True,
    )

    if ch_col in df_filtered.columns:
        eff = (
            df_filtered.groupby(ch_col)
            .agg(
                avg_roi=("ROI", "mean"),
                avg_conv=("Conversion_Rate", "mean"),
                total_revenue=(rev_col, "sum"),
            )
            .reset_index()
        )

        best_roi = eff.sort_values("avg_roi", ascending=False).head(3)
        worst_roi = eff.sort_values("avg_roi", ascending=True).head(3)
        best_conv = eff.sort_values("avg_conv", ascending=False).head(3)

        st.markdown("##### أفضل القنوات (ROI):")
        for _, row in best_roi.iterrows():
            st.write(
                f"- **{row[ch_col]}**: ROI متوسط ≈ {row['avg_roi']:.2f}x "
                f"وإيراد إجمالي ≈ ${row['total_revenue']:,.0f}"
            )

        st.markdown("##### قنوات تحتاج تحسين (ROI الأقل):")
        for _, row in worst_roi.iterrows():
            st.write(
                f"- **{row[ch_col]}**: ROI منخفض ≈ {row['avg_roi']:.2f}x. "
                "جرّبي تقليل الإنفاق أو تحسين الاستهداف / الكريتيف."
            )

        st.markdown("##### أعلى القنوات في Conversion Rate:")
        for _, row in best_conv.iterrows():
            st.write(
                f"- **{row[ch_col]}**: Conversion Rate متوسط ≈ {row['avg_conv']*100:.1f}% – "
                "مناسبة لتخصيص مزيد من الميزانية."
            )

    else:
        st.info("لا يوجد عمود channel لبناء توصيات على مستوى القناة.")

    st.markdown("</div>", unsafe_allow_html=True)
