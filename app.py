import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# 1) PAGE CONFIG + THEME COLORS
# =========================
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

COL = {
    "primary": "#3647F5",
    "navy": "#1B2346",
    "accent": "#FF9F0D",
    "dark": "#040D2F",
    "soft": "#D9D9D9",
}

st.markdown(f"""
<style>
/* Background + base typography */
.stApp {{
    background: linear-gradient(180deg, {COL['navy']} 0%, {COL['dark']} 100%);
    color: #ffffff;
}}

/* Headings */
h1, h2, h3, h4 {{
    color: #FFFFFF !important;
}}

/* Cards (KPI + content) */
.kpi-card {{
    background: linear-gradient(145deg, rgba(27,35,70,.92), rgba(4,13,47,.92));
    border: 1px solid rgba(217, 217, 217, 0.22);
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 14px 30px rgba(0,0,0,.45);
    height: 100%;
}}
.kpi-label {{ color: rgba(217,217,217,.9); font-size: 13px; }}
.kpi-value {{ color: #FFFFFF; font-size: 22px; font-weight: 800; letter-spacing: .2px; margin-top: 2px; }}

.subtle {{ color: rgba(217,217,217,.9); }}
</style>
""", unsafe_allow_html=True)

# =========================
# 2) DATA LOADING + PREP (Member 1)
# =========================
@st.cache_data
def load_data(path: str = "cleaned_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # ---- Clean object columns (missing/blank) ----
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (df[col].astype(str)
                          .str.strip()
                          .replace({"": np.nan, "nan": np.nan, "None": np.nan}))

    # ---- Fix date types (date + registration_date) ----
    for dcol in ["date", "registration_date"]:
        if dcol in df.columns:
            df[dcol] = pd.to_datetime(df[dcol], errors="coerce")

    # ---- Month column: ensure a usable month period for filtering ----
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"], errors="coerce")

    if "month" not in df.columns or df["month"].isna().mean() > 0.5:
        if "date" in df.columns:
            df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # ---- Numeric coercion for key measures (safe) ----
    numeric_cols = [
        "price", "quantity", "discount_percent", "final_amount",
        "income", "customer_lifetime_value", "retention_score",
        "Average Order Value", "revenue_per_customer", "discount_amount",
        "gross_revenue", "net_revenue", "roi", "conversion_rate"
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- Derived / standardized columns (Member 1 required KPIs) ----
    # CTR/CPC: only if base columns exist; otherwise they remain NaN (no fabrication)
    if "impressions" not in df.columns:
        df["impressions"] = np.nan
    if "clicks" not in df.columns:
        df["clicks"] = np.nan
    if "spend" not in df.columns:
        df["spend"] = np.nan

    df["ctr"] = np.where((df["impressions"] > 0) & (df["clicks"] >= 0),
                         df["clicks"] / df["impressions"], np.nan)

    df["cpc"] = np.where((df["clicks"] > 0) & (df["spend"] >= 0),
                         df["spend"] / df["clicks"], np.nan)

    # Conversion rate (if not provided, try build from conversions/clicks if available)
    if "conversion_rate" not in df.columns or df["conversion_rate"].isna().all():
        if "conversions" in df.columns:
            df["conversion_rate"] = np.where((df["clicks"] > 0) & (df["conversions"] >= 0),
                                           df["conversions"] / df["clicks"], np.nan)
        else:
            df["conversion_rate"] = np.nan

    # ROI (if not provided): (revenue - spend) / spend (only when spend exists)
    if "roi" not in df.columns or df["roi"].isna().all():
        base_rev = df["net_revenue"] if "net_revenue" in df.columns else df.get("final_amount", np.nan)
        df["roi"] = np.where((df["spend"] > 0) & pd.Series(base_rev).notna(),
                             (base_rev - df["spend"]) / df["spend"], np.nan)

    return df

df = load_data("cleaned_data.csv")

if df.empty:
    st.error("Data is empty or 'cleaned_data.csv' is missing/invalid.")
    st.stop()

# =========================
# 3) SIDEBAR FILTERS (Channel + Month range as Dropdowns)
# =========================
st.sidebar.markdown("## Filters")

# --- Channel (dropdown multi-select) ---
channels = sorted([c for c in df.get("marketing_channel", pd.Series([])).dropna().unique() if str(c).strip() != ""])
sel_channels = st.sidebar.multiselect("Channel", options=channels, default=channels)

# --- Month range (two dropdowns: start + end) ---
months = sorted([m for m in df.get("month", pd.Series([])).dropna().unique()])
if len(months) == 0:
    st.sidebar.warning("No valid 'month' values found (check 'date' / 'month' columns).")
    start_month = end_month = None
else:
    month_labels = [pd.to_datetime(m).strftime("%b %Y") for m in months]
    label_to_month = {lab: pd.to_datetime(m) for lab, m in zip(month_labels, months)}

    start_label = st.sidebar.selectbox("Start month", options=month_labels, index=0)
    end_label = st.sidebar.selectbox("End month", options=month_labels, index=len(month_labels) - 1)

    start_month = label_to_month[start_label]
    end_month = label_to_month[end_label]

# =========================
# 4) APPLY FILTERS
# =========================
df_f = df.copy()

if sel_channels:
    df_f = df_f[df_f["marketing_channel"].isin(sel_channels)]

if start_month is not None and end_month is not None:
    if start_month > end_month:
        start_month, end_month = end_month, start_month
    df_f = df_f[(pd.to_datetime(df_f["month"]) >= start_month) &
                (pd.to_datetime(df_f["month"]) <= end_month)]

# =========================
# 5) KPI CALCULATIONS (Member 1 deliverables)
# =========================
def safe_sum(s): 
    return float(pd.Series(s).fillna(0).sum())

def safe_mean(s):
    s = pd.Series(s).dropna()
    return float(s.mean()) if len(s) else np.nan

total_orders = df_f["order_id"].nunique() if "order_id" in df_f.columns else 0
total_customers = df_f["customer_id"].nunique() if "customer_id" in df_f.columns else 0

net_revenue = safe_sum(df_f["net_revenue"]) if "net_revenue" in df_f.columns else safe_sum(df_f.get("final_amount", 0))
gross_revenue = safe_sum(df_f["gross_revenue"]) if "gross_revenue" in df_f.columns else net_revenue

aov = (net_revenue / total_orders) if total_orders else np.nan
rev_per_customer = safe_mean(df_f["revenue_per_customer"]) if "revenue_per_customer" in df_f.columns else (net_revenue / total_customers if total_customers else np.nan)
clv = safe_mean(df_f["customer_lifetime_value"]) if "customer_lifetime_value" in df_f.columns else np.nan
retention = safe_mean(df_f["retention_score"]) if "retention_score" in df_f.columns else np.nan
conv_rate = safe_mean(df_f["conversion_rate"]) if "conversion_rate" in df_f.columns else np.nan
roi_avg = safe_mean(df_f["roi"]) if "roi" in df_f.columns else np.nan

# =========================
# 6) HEADER + TABS (Required structure)
# =========================
st.title("📊 Marketing Analytics Dashboard (Streamlit)")
st.caption("Filters (Channel + Month range) apply to all tabs. All metrics are computed from the loaded dataset (no external data).")

tab_kpis, tab_channel, tab_trends, tab_eff, tab_about = st.tabs([
    "KPIs & Overview",
    "Analyze total performance per channel",
    "Time trends analysis",
    "Efficiency",
    "About & Recommendations"
])

# =========================
# 7) TAB 1 — KPIs & OVERVIEW (Member 1)
# =========================
with tab_kpis:
    st.subheader("KPIs (Overview)")

    c1, c2, c3, c4 = st.columns(4)
    def kpi(col, label, value):
        col.markdown(
            f"<div class='kpi-card'><div class='kpi-label'>{label}</div>"
            f"<div class='kpi-value'>{value}</div></div>",
            unsafe_allow_html=True
        )

    kpi(c1, "Net Revenue", f"${net_revenue:,.0f}")
    kpi(c2, "Orders", f"{total_orders:,}")
    kpi(c3, "Customers", f"{total_customers:,}")
    kpi(c4, "AOV", "—" if np.isnan(aov) else f"${aov:,.0f}")

    c5, c6, c7, c8 = st.columns(4)
    kpi(c5, "Conversion Rate", "—" if np.isnan(conv_rate) else f"{conv_rate*100:.2f}%")
    kpi(c6, "Avg ROI", "—" if np.isnan(roi_avg) else f"{roi_avg:.2f}x")
    kpi(c7, "CLV (avg)", "—" if np.isnan(clv) else f"${clv:,.0f}")
    kpi(c8, "Retention (avg)", "—" if np.isnan(retention) else f"{retention:.2f}")

    st.markdown("---")
    st.markdown("### Quick snapshot (available fields)")
    st.write("This app uses your dataset columns (e.g., `net_revenue`, `roi`, `conversion_rate`, etc.). "
             "If some columns (like `spend/clicks/impressions`) are missing, related KPIs will show as ‘—’ (no invented numbers).")

# =========================
# 8) TAB 2 — CHANNEL PERFORMANCE (Member 2)
# =========================
with tab_channel:
    st.subheader("Analyze total performance per channel")

    if "marketing_channel" not in df_f.columns:
        st.warning("Column 'marketing_channel' is missing — cannot compute channel performance.")
    else:
        # Spend is only computed if 'spend' exists; otherwise stays NaN (no fabrication)
        spend_col = "spend" if "spend" in df_f.columns else None
        spend_series = df_f[spend_col] if spend_col else pd.Series(np.nan, index=df_f.index)

        chan = (df_f.assign(_spend=spend_series,
                            _revenue=df_f["net_revenue"] if "net_revenue" in df_f.columns else df_f.get("final_amount", np.nan),
                            _conversions=df_f["customer_id"].where(df_f["customer_id"].notna(), np.nan))
                .groupby("marketing_channel", dropna=False)
                .agg(
                    total_spend=("_spend", "sum"),
                    total_revenue=("_revenue", "sum"),
                    total_conversions=("_conversions", "nunique"),
                    avg_roi=("roi" if "roi" in df_f.columns else "_revenue", "mean")
                )
                .reset_index()
                .rename(columns={"marketing_channel": "Channel"})
        )

        # Derived per-channel metrics (safe)
        chan["CPC"] = np.where(chan["total_conversions"] > 0, chan["total_spend"] / chan["total_conversions"], np.nan)
        chan["Conversion Rate"] = np.where(chan["total_conversions"] > 0,
                                           chan["total_conversions"] / chan["total_conversions"].sum()
                                           if chan["total_conversions"].sum() > 0 else np.nan,
                                           np.nan)
        chan["Avg Order Value"] = np.where(chan["total_conversions"] > 0, chan["total_revenue"] / chan["total_conversions"], np.nan)
        chan["ROI"] = np.where(chan["total_spend"] > 0, (chan["total_revenue"] - chan["total_spend"]) / chan["total_spend"], np.nan)

        st.markdown("#### Channel table (computed from your dataset)")
        st.dataframe(chan, use_container_width=True, hide_index=True)

        st.markdown("#### Charts (top channels)")
        col_a, col_b = st.columns(2)
        with col_a:
            fig = px.bar(chan.sort_values("total_revenue", ascending=False).head(10),
                         x="Channel", y="total_revenue", title="Total Revenue by Channel")
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            fig = px.bar(chan.sort_values("total_conversions", ascending=False).head(10),
                         x="Channel", y="total_conversions", title="Total Conversions by Channel")
            st.plotly_chart(fig, use_container_width=True)

# =========================
# 9) TAB 3 — TIME TRENDS (Member 3)
# =========================
with tab_trends:
    st.subheader("Time trends analysis (monthly)")

    if "month" not in df_f.columns:
        st.warning("Column 'month' is missing (or not computable). Add 'date' or 'month' to your dataset.")
    else:
        monthly = (df_f.assign(_revenue=df_f["net_revenue"] if "net_revenue" in df_f.columns else df_f.get("final_amount", np.nan),
                               _conversions=df_f["customer_id"])
                   .groupby("month", dropna=False)
                   .agg(revenue=("_revenue", "sum"),
                        conversions=("_conversions", "nunique"))
                   .reset_index()
                   .sort_values("month")
        )

        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(monthly, x="month", y="revenue", markers=True, title="Revenue by month")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(monthly, x="month", y="conversions", markers=True, title="Conversions by month")
            st.plotly_chart(fig, use_container_width=True)

        if len(monthly) >= 2:
            peak = monthly.sort_values("revenue", ascending=False).head(1).iloc[0]
            low = monthly.sort_values("revenue", ascending=True).head(1).iloc[0]
            st.markdown("### Peaks / Lows (based on revenue)")
            st.write(f"- Peak month: **{pd.to_datetime(peak['month']).strftime('%b %Y')}** (Revenue = ${peak['revenue']:,.0f})")
            st.write(f"- Low month: **{pd.to_datetime(low['month']).strftime('%b %Y')}** (Revenue = ${low['revenue']:,.0f})")

# =========================
# 10) TAB 4 — EFFICIENCY (Member 4)
# =========================
with tab_eff:
    st.subheader("Efficiency (CPC, Conversion Rate) + Spend impact (correlations)")

    if "marketing_channel" not in df_f.columns:
        st.warning("Missing 'marketing_channel' → cannot compute efficiency.")
    else:
        # Efficiency table (only meaningful when spend/clicks/conversions exist)
        has_spend = "spend" in df_f.columns and df_f["spend"].notna().any()
        has_clicks = "clicks" in df_f.columns and df_f["clicks"].notna().any()
        has_conversions = "conversions" in df_f.columns and df_f["conversions"].notna().any()

        eff = (df_f.groupby("marketing_channel", dropna=False)
               .agg(
                   avg_cpc=("cpc", "mean"),
                   avg_conv_rate=("conversion_rate", "mean")
               )
               .reset_index()
               .rename(columns={"marketing_channel": "Channel"})
        )

        st.markdown("#### Efficiency table (per channel)")
        st.dataframe(eff, use_container_width=True, hide_index=True)

        # Correlations (spend vs revenue / conversions) if spend exists
        if has_spend:
            spend = df_f["spend"]
            revenue = df_f["net_revenue"] if "net_revenue" in df_f.columns else df_f.get("final_amount", pd.Series(np.nan, index=df_f.index))
            conv = df_f["conversions"] if has_conversions else pd.Series(np.nan, index=df_f.index)

            corr_rev = spend.corr(revenue) if spend.notna().sum() > 2 and revenue.notna().sum() > 2 else np.nan
            corr_conv = spend.corr(conv) if has_conversions and spend.notna().sum() > 2 and conv.notna().sum() > 2 else np.nan

            st.markdown("#### Spend impact (correlations)")
            st.write(f"- Spend vs Revenue correlation: **{corr_rev:.3f}**" if pd.notna(corr_rev) else "- Spend vs Revenue correlation: **—** (insufficient data)")
            st.write(f"- Spend vs Conversions correlation: **{corr_conv:.3f}**" if pd.notna(corr_conv) else "- Spend vs Conversions correlation: **—** (insufficient data)")
        else:
            st.info("No `spend` column found → spend-impact correlations cannot be computed (this is expected with the current dataset).")

# =========================
# 11) TAB 5 — ABOUT & RECOMMENDATIONS (Member 5)
# =========================
with tab_about:
    st.subheader("About")
    st.write("""
    This dashboard is built to deliver:
    - Data preparation + KPI calculation (Member 1)
    - Channel performance comparison (Member 2)
    - Time trends analysis (Member 3)
    - Efficiency + spend impact (Member 4)
    - Recommendations (Member 5)
    """)

    st.subheader("Recommendations (from computed results)")
    recs = []

    # Simple rule-based recommendations (no invented data)
    if "marketing_channel" in df_f.columns and "net_revenue" in df_f.columns and not df_f.empty:
        top = (df_f.groupby("marketing_channel")["net_revenue"].sum()
               .sort_values(ascending=False).head(2).index.tolist())
        if top:
            recs.append(f"Increase focus/budget on top channels: {', '.join(top)} (highest net revenue in selected filters).")

    if not np.isnan(roi_avg) and roi_avg < 0:
        recs.append("Overall ROI is negative in the selected window — revisit spend allocation and campaign/landing alignment.")

    if not np.isnan(conv_rate) and conv_rate < 0.02:
        recs.append("Conversion rate is low (<2%) — simplify checkout and tighten targeting/offer fit.")

    if not recs:
        recs.append("No strong recommendation can be derived from the current filters — try widening the month range or including more channels.")

    for i, r in enumerate(recs, 1):
        st.markdown(f"**{i}.** {r}")
