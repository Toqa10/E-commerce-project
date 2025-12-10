# app.py  (Member 5: Streamlit app)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Config (Streamlit)
# -------------------------
st.set_page_config(page_title="Marketing Dashboard", layout="wide", page_icon="📊")  # (must be first) :contentReference[oaicite:0]{index=0}

# -------------------------
# Brand colors (from your palette)
# -------------------------
COL = {
    "primary": "#3647F5",
    "navy": "#1B2346",
    "accent": "#FF9F0D",
    "dark": "#040D2F",
    "soft": "#D9D9D9",
}

# Small CSS to mimic card layout and dark header feel
st.markdown(f"""
<style>
/* background / text */
.stApp {{
    background: radial-gradient(1200px 900px at 10% 5%, {COL['primary']}22, transparent 55%),
                radial-gradient(1100px 900px at 110% 15%, {COL['accent']}12, transparent 60%),
                linear-gradient(180deg, {COL['navy']} 0%, {COL['dark']} 100%);
    color: #ffffff;
}}
h1, h2, h3 {{
    color: #ffffff !important;
}}
/* cards */
.kpi {{
    border-radius: 14px;
    padding: 14px;
    background: linear-gradient(145deg, rgba(27,35,70,.92), rgba(4,13,47,.92));
    border: 1px solid rgba(217,217,217,.22);
    box-shadow: 0 14px 30px rgba(0,0,0,.45);
}}
.kpi .label {{ color: rgba(217,217,217,.9); font-size: 13px; }}
.kpi .value {{ color: #fff; font-size: 22px; font-weight: 800; margin-top: 2px; }}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load data (from Member 1 output)
# -------------------------
@st.cache_data
def load_final():
    df = pd.read_csv("cleaned_data_final.csv")

    # Safety: ensure key types (same logic as notebook)
    for c in ["date", "registration_date", "month"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    if "month" in df.columns and df["month"].isna().mean() > 0 and "date" in df.columns:
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Numeric normalization (safe)
    numeric = [
        "price","quantity","discount_percent","final_amount","income",
        "customer_lifetime_value","retention_score",
        "Average Order Value","revenue_per_customer",
        "discount_amount","gross_revenue","net_revenue",
        "roi","conversion_rate"
    ]
    for c in numeric:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Ensure required derived columns exist (same as notebook)
    if "net_revenue" not in df.columns:
        df["net_revenue"] = df["final_amount"]
    if "gross_revenue" not in df.columns:
        df["gross_revenue"] = df["net_revenue"]

    return df

df = load_final()

# -------------------------
# Sidebar filters (dropdowns)
# -------------------------
st.sidebar.markdown("## Filters")

# Channel filter (dropdown; includes ALL)
if "marketing_channel" in df.columns:
    channels = sorted([c for c in df["marketing_channel"].dropna().unique() if str(c).strip() != ""])
    channel_choice = st.sidebar.selectbox("Channel", options=["All"] + channels, index=0)
else:
    channel_choice = "All"

# Month filter as two dropdowns (start/end) — as requested (dropdown list)
if "month" in df.columns and df["month"].dropna().any():
    months = sorted(df["month"].dropna().unique())
    # Convert to human-readable labels but keep the underlying datetime for filtering
    month_labels = [pd.to_datetime(m).strftime("%b %Y") for m in months]
    start_label = st.sidebar.selectbox("Start month", options=month_labels, index=0)
    end_label = st.sidebar.selectbox("End month", options=month_labels, index=len(month_labels)-1)

    # Map labels back to datetime
    label_to_dt = {lbl: pd.to_datetime(m) for lbl, m in zip(month_labels, months)}
    start_month = label_to_dt[start_label]
    end_month = label_to_dt[end_label]
else:
    start_month = None
    end_month = None

# Apply filters
df_f = df.copy()
if channel_choice != "All" and "marketing_channel" in df_f.columns:
    df_f = df_f[df_f["marketing_channel"] == channel_choice]

if start_month is not None and end_month is not None and "month" in df_f.columns:
    # ensure start <= end (if user reversed)
    if start_month > end_month:
        start_month, end_month = end_month, start_month
    df_f = df_f[(df_f["month"] >= start_month) & (df_f["month"] <= end_month)]

# -------------------------
# Helper stats for KPIs
# -------------------------
def safe_sum(s): 
    return float(pd.Series(s).fillna(0).sum())

def safe_mean(s):
    s = pd.Series(s).dropna()
    return float(s.mean()) if len(s) else np.nan

total_orders = df_f["order_id"].nunique() if "order_id" in df_f.columns else 0
total_customers = df_f["customer_id"].nunique() if "customer_id" in df_f.columns else 0
net_revenue = safe_sum(df_f["net_revenue"]) if "net_revenue" in df_f.columns else safe_sum(df_f["final_amount"])
gross_revenue = safe_sum(df_f["gross_revenue"]) if "gross_revenue" in df_f.columns else net_revenue

aov = (net_revenue / total_orders) if total_orders else np.nan
rev_per_cust = safe_mean(df_f["revenue_per_customer"]) if "revenue_per_customer" in df_f.columns else (net_revenue / total_customers if total_customers else np.nan)
clv = safe_mean(df_f["customer_lifetime_value"]) if "customer_lifetime_value" in df_f.columns else np.nan
roi = safe_mean(df_f["roi"]) if "roi" in df_f.columns else np.nan
conv = safe_mean(df_f["conversion_rate"]) if "conversion_rate" in df_f.columns else np.nan

# -------------------------
# Simple plotting helpers (matplotlib/seaborn)
# -------------------------
def plot_bar(x, y, title, xlabel="", ylabel=""):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(9, 4.2))  # (subplots API) :contentReference[oaicite:1]{index=1}
    sns.barplot(data=df_f, x=x, y=y, ax=ax, errorbar=None)  # (barplot doc) :contentReference[oaicite:2]{index=2}
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=25)
    return fig

def plot_line(x, y, title, xlabel="", ylabel=""):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(9, 4.2))
    sns.lineplot(data=df_f, x=x, y=y, ax=ax, marker="o")  # (lineplot doc) :contentReference[oaicite:3]{index=3}
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=25)
    return fig

# -------------------------
# Header + tabs (Overview / Trends / Efficiency / Recommendations)
# -------------------------
st.title("📊 Marketing Dashboard (Final Deliverable)")
st.caption("Filters: Channel + Month range (dropdowns). Metrics and charts are computed from the cleaned dataset (Member 1–4).")

tab_overview, tab_trends, tab_eff, tab_rec = st.tabs(["Overview", "Trends", "Efficiency", "Recommendations"])  # multipage-like navigation (tabs) :contentReference[oaicite:4]{index=4}

# =========================
# TAB 1 — OVERVIEW (KPIs + channel snapshot)
# =========================
with tab_overview:
    st.subheader("KPIs (Member 1)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='kpi'><div class='label'>Net Revenue</div><div class='value'>${net_revenue:,.0f}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='kpi'><div class='label'>Orders</div><div class='value'>{total_orders:,}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='kpi'><div class='label'>Customers</div><div class='value'>{total_customers:,}</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='kpi'><div class='label'>AOV</div><div class='value'>{'—' if np.isnan(aov) else f'${aov:,.0f}'}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Channel snapshot (Member 2 — summary view)")
    if "marketing_channel" in df_f.columns and "net_revenue" in df_f.columns:
        st.pyplot(plot_bar("marketing_channel", "net_revenue", "Net revenue by channel", "Channel", "Net revenue"))
    else:
        st.info("No required columns (marketing_channel/net_revenue) available for channel snapshot.")

# =========================
# TAB 2 — TRENDS (Monthly revenue + conversions)
# =========================
with tab_trends:
    st.subheader("Monthly trends (Member 3)")
    if "month" in df_f.columns and "net_revenue" in df_f.columns:
        st.pyplot(plot_line("month", "net_revenue", "Monthly net revenue", "Month", "Net revenue"))
    else:
        st.info("Missing month or net_revenue columns for trend chart.")

    # Lows/peaks (simple textual summary derived from the same aggregated data)
    if "month" in df_f.columns and "net_revenue" in df_f.columns and not df_f.empty:
        monthly = (df_f.groupby("month", dropna=False)["net_revenue"].sum().reset_index()
                   .sort_values("net_revenue", ascending=False))
        top = monthly.head(2)
        low = monthly.tail(2)

        st.markdown("**Peaks (top months by revenue):**")
        for _, r in top.iterrows():
            st.write(f"- {pd.to_datetime(r['month']).strftime('%b %Y')}: ${r['net_revenue']:,.0f}")

        st.markdown("**Lows (lowest months by revenue):**")
        for _, r in low.iterrows():
            st.write(f"- {pd.to_datetime(r['month']).strftime('%b %Y')}: ${r['net_revenue']:,.0f}")

# =========================
# TAB 3 — EFFICIENCY (CPC + conversion rate + ranking)
# =========================
with tab_eff:
    st.subheader("Efficiency (Member 4)")

    # Build efficiency table (works even if spend/clicks are missing)
    spend = df_f["spend"] if "spend" in df_f.columns else pd.Series(np.nan, index=df_f.index)
    clicks = df_f["clicks"] if "clicks" in df_f.columns else pd.Series(np.nan, index=df_f.index)
    conversions = df_f["conversions"] if "conversions" in df_f.columns else pd.Series(np.nan, index=df_f.index)

    cpc = np.where((clicks > 0) & (spend >= 0), spend / clicks, np.nan)
    conv_rate = df_f["conversion_rate"] if "conversion_rate" in df_f.columns else np.where((clicks > 0) & (conversions >= 0), conversions / clicks, np.nan)

    eff = pd.DataFrame({
        "channel": df_f["marketing_channel"] if "marketing_channel" in df_f.columns else "Unknown",
        "avg_cpc": cpc,
        "avg_conversion_rate": conv_rate
    }).groupby("channel", dropna=False).mean(numeric_only=True).reset_index()

    if not eff.empty:
        eff["cpc_rank"] = eff["avg_cpc"].rank(ascending=True, method="min")
        eff["conv_rank"] = eff["avg_conversion_rate"].rank(ascending=False, method="min")
        eff["overall_rank"] = eff["cpc_rank"].fillna(eff["cpc_rank"].max()+1) + eff["conv_rank"].fillna(eff["conv_rank"].max()+1)
        eff = eff.sort_values("overall_rank")

        st.dataframe(eff.style.format({"avg_cpc":"{:.2f}", "avg_conversion_rate":"{:.2%}"}), use_container_width=True)
    else:
        st.info("No efficiency data available (missing spend/clicks/conversions).")

    # Spend impact (correlations)
    if "spend" in df_f.columns:
        corr_rev = df_f["spend"].corr(df_f["net_revenue"]) if "net_revenue" in df_f.columns else np.nan
        corr_conv = df_f["spend"].corr(df_f["conversions"]) if "conversions" in df_f.columns else np.nan
        st.markdown("**Spend impact (correlations):**")
        st.write(f"- Spend vs Revenue: {corr_rev if pd.notna(corr_rev) else '—'}")
        st.write(f"- Spend vs Conversions: {corr_conv if pd.notna(corr_conv) else '—'}")

# =========================
# TAB 4 — RECOMMENDATIONS (rules derived from Member 1–4 metrics)
# =========================
with tab_rec:
    st.subheader("Recommendations (Member 5 — based on computed results)")
    recs = []

    if "marketing_channel" in df_f.columns and "net_revenue" in df_f.columns and not df_f.empty:
        top_channels = (df_f.groupby("marketing_channel")["net_revenue"].sum()
                        .sort_values(ascending=False).head(2).index.tolist())
        if top_channels:
            recs.append(f"Increase budget/effort on top channels: {', '.join(top_channels)} (highest net revenue in selected window).")

    if pd.notna(roi) and roi < 0:
        recs.append("ROI is negative in the selected window — review spend allocation and creative/landing page alignment.")

    if pd.notna(conv) and conv < 0.02:
        recs.append("Conversion rate is low (below ~2%) — simplify checkout and tighten targeting/offer fit.")

    if not recs:
        recs.append("No strong recommendation can be generated from the current filters — widen month range or include more channels.")

    for i, r in enumerate(recs, 1):
        st.markdown(f"**{i}.** {r}")
