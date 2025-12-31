import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------
# PAGE CONFIG
# ------------------------------------
st.set_page_config(
    page_title="Benford Fraud Detection Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# HEADER
# ------------------------------------
st.title("📊 Financial Fraud Detection Dashboard")
st.markdown(
    """
    **Benford’s Law + Isolation Forest**  
    *Risk-based forensic analytics for financial statement review*
    """
)

st.divider()

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
st.sidebar.header("🔎 Analysis Filters")

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
# EXECUTIVE SUMMARY KPIs
# ------------------------------------
st.subheader("📌 Executive Risk Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Records", len(filtered_df))
c2.metric("High-Risk Flags", int(filtered_df["Fraud_Flag"].sum()))
c3.metric("Avg Benford MAD", round(filtered_df["MAD"].mean(), 4))
c4.metric("Avg ML Anomaly Score", round(filtered_df["Anomaly_Score"].mean(), 4))

st.caption(
    "Higher MAD and lower anomaly scores indicate stronger deviation from expected financial patterns."
)

st.divider()

# ------------------------------------
# ANOMALY SCORE DISTRIBUTION
# ------------------------------------
st.subheader("📉 ML Anomaly Score Distribution")

fig_anomaly = px.histogram(
    filtered_df,
    x="Anomaly_Score",
    color="Fraud_Flag",
    nbins=25,
    title="Isolation Forest Anomaly Score Distribution",
    color_discrete_map={0: "#2E86C1", 1: "#C0392B"}
)
st.plotly_chart(fig_anomaly, use_container_width=True)

# ------------------------------------
# BENFORD DEVIATION SPACE
# ------------------------------------
st.subheader("📌 Benford Deviation Risk Map")

fig_scatter = px.scatter(
    filtered_df,
    x="MAD",
    y="Chi_Square",
    color="Fraud_Flag",
    size="Avg_Z_Score",
    hover_data=["Year", "Statement Type"],
    title="MAD vs Chi-Square with Fraud Highlighting",
    color_discrete_map={0: "#27AE60", 1: "#E74C3C"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------------
# YEAR-WISE RISK TREND
# ------------------------------------
st.subheader("📈 Year-wise Risk Trend")

trend_df = (
    filtered_df
    .groupby("Year", as_index=False)["Anomaly_Score"]
    .mean()
)

fig_trend = px.line(
    trend_df,
    x="Year",
    y="Anomaly_Score",
    markers=True,
    title="Average Anomaly Score Trend Over Time"
)
st.plotly_chart(fig_trend, use_container_width=True)

# ------------------------------------
# STATEMENT-WISE RISK COMPARISON
# ------------------------------------
st.subheader("📊 Statement-wise Risk Comparison")

fig_bar = px.bar(
    filtered_df,
    x="Statement Type",
    y="Anomaly_Score",
    color="Year",
    barmode="group",
    title="Anomaly Scores by Financial Statement"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------
# TOP HIGH-RISK OBSERVATIONS
# ------------------------------------
st.subheader("🚩 Top High-Risk Observations")

top_risk = (
    filtered_df
    .sort_values("Anomaly_Score")
    .head(10)
)

st.dataframe(
    top_risk,
    use_container_width=True
)

# ------------------------------------
# FRAUD FLAG PROPORTION
# ------------------------------------
st.subheader("🧮 Fraud vs Non-Fraud Distribution")

fig_flag = px.pie(
    filtered_df,
    names="Fraud_Flag",
    title="Fraud Flag Distribution",
    color_discrete_sequence=["#1ABC9C", "#E74C3C"]
)
st.plotly_chart(fig_flag, use_container_width=True)

# ------------------------------------
# FOOTER
# ------------------------------------
st.divider()
st.caption(
    """
    ⚠️ **Disclaimer:**  
    Fraud flags represent **statistical anomalies**, not confirmed fraud.  
    This dashboard supports **risk-based forensic auditing and investigative prioritization**.
    """
)
