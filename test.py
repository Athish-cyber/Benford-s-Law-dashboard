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

c1.metric("Total Records", len(fi
