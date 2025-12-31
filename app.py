import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------
# PAGE CONFIG
# ------------------------------------
st.set_page_config(
    page_title="Benford Fraud Detection Dashboard",
    layout="wide"
)

st.title("📊 Benford’s Law + Isolation Forest Fraud Detection")
st.markdown("**Interactive Dashboard for Forensic Auditing & Financial Analysis**")

# ------------------------------------
# LOAD DATA
# ------------------------------------
DATA_PATH = "Benford_IsolationForest_Output.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)

df = load_data()

# ------------------------------------
# SIDEBAR FILTERS
# ------------------------------------
st.sidebar.header("🔎 Filters")

years = st.sidebar.multiselect(
    "Select Year(s)",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

statements = st.sidebar.multiselect(
    "Select Statement Type",
    df["Statement Type"].unique(),
    default=df["Statement Type"].unique()
)

filtered_df = df[
    (df["Year"].isin(years)) &
    (df["Statement Type"].isin(statements))
]

# ------------------------------------
# KPI METRICS
# ------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Observations", len(filtered_df))
col2.metric("Fraud Flags", int(filtered_df["Fraud_Flag"].sum()))
col3.metric("Avg MAD", round(filtered_df["MAD"].mean(), 4))
col4.metric("Avg Anomaly Score", round(filtered_df["Anomaly_Score"].mean(), 4))

st.divider()

# ------------------------------------
# BENFORD METRICS TABLE
# ------------------------------------
st.subheader("📋 Benford Deviation Metrics & Fraud Flags")

st.dataframe(
    filtered_df.sort_values("Anomaly_Score"),
    use_container_width=True
)

# ------------------------------------
# ANOMALY SCORE DISTRIBUTION
# ------------------------------------
st.subheader("📉 Anomaly Score Distribution")

fig_anomaly = px.histogram(
    filtered_df,
    x="Anomaly_Score",
    color="Fraud_Flag",
    nbins=20,
    title="Isolation Forest Anomaly Scores",
    labels={"Fraud_Flag": "Fraud Flag"}
)

st.plotly_chart(fig_anomaly, use_container_width=True)

# ------------------------------------
# MAD vs CHI-SQUARE SCATTER
# ------------------------------------
st.subheader("📌 MAD vs Chi-Square (Fraud Highlighted)")

fig_scatter = px.scatter(
    filtered_df,
    x="MAD",
    y="Chi_Square",
    color="Fraud_Flag",
    size="Avg_Z_Score",
    hover_data=["Year", "Statement Type"],
    title="Benford Deviation Space"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------------
# STATEMENT-WISE COMPARISON
# ------------------------------------
st.subheader("📊 Statement-wise Risk Comparison")

fig_bar = px.bar(
    filtered_df,
    x="Statement Type",
    y="Anomaly_Score",
    color="Year",
    barmode="group",
    title="Anomaly Scores by Statement Type"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------
# FRAUD FLAG SUMMARY
# ------------------------------------
st.subheader("🚩 Fraud Flag Summary")

fig_flag = px.pie(
    filtered_df,
    names="Fraud_Flag",
    title="Fraud vs Non-Fraud Distribution"
)

st.plotly_chart(fig_flag, use_container_width=True)

# ------------------------------------
# FOOTER
# ------------------------------------
st.divider()
st.caption(
    "⚠️ Disclaimer: Flags indicate statistical anomalies and do not constitute proof of fraud. "
    "This dashboard supports risk-based forensic auditing and analytical review."
)
