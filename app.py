# ============================================================
# CUSTOMER SEGMENTATION & CHURN PATTERN ANALYTICS
# EUROPEAN BANKING
# Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="European Banking - Customer Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    .metric-title {
        font-size: 14px;
        color: #64748b;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("European_Bank.csv")

    return df


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "European_Bank.csv was not found. "
        "Place the CSV file in the same folder as app.py."
    )

    st.stop()


# ============================================================
# DATA PREPROCESSING
# ============================================================

@st.cache_data
def preprocess_data(data):

    df = data.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove unnecessary surname column
    if "Surname" in df.columns:
        df = df.drop(columns=["Surname"])

    # Convert numeric columns
    numeric_columns = [
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Remove rows with missing critical values
    required_columns = [
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited"
    ]

    available_required = [
        col for col in required_columns
        if col in df.columns
    ]

    df = df.dropna(subset=available_required)

    # --------------------------------------------------------
    # AGE SEGMENTS
    # --------------------------------------------------------

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[0, 29, 45, 60, np.inf],
        labels=[
            "<30",
            "30-45",
            "46-60",
            "60+"
        ]
    )

    # --------------------------------------------------------
    # CREDIT SCORE SEGMENTS
    # --------------------------------------------------------

    df["Credit_Score_Band"] = pd.cut(
        df["CreditScore"],
        bins=[0, 579, 669, 739, 799, np.inf],
        labels=[
            "Poor",
            "Fair",
            "Good",
            "Very Good",
            "Excellent"
        ]
    )

    # --------------------------------------------------------
    # TENURE SEGMENTS
    # --------------------------------------------------------

    df["Tenure_Group"] = pd.cut(
        df["Tenure"],
        bins=[-1, 2, 5, 8, np.inf],
        labels=[
            "New",
            "Mid-term",
            "Established",
            "Long-term"
        ]
    )

    # --------------------------------------------------------
    # BALANCE SEGMENTS
    # --------------------------------------------------------

    df["Balance_Segment"] = pd.cut(
        df["Balance"],
        bins=[
            -1,
            0,
            50000,
            100000,
            150000,
            np.inf
        ],
        labels=[
            "Zero Balance",
            "Low Balance",
            "Medium Balance",
            "High Balance",
            "Very High Balance"
        ]
    )

    # --------------------------------------------------------
    # CUSTOMER VALUE SEGMENT
    # --------------------------------------------------------

    balance_median = df["Balance"].median()

    salary_median = df["EstimatedSalary"].median()

    df["Customer_Value"] = np.where(
        (df["Balance"] >= balance_median) &
        (df["EstimatedSalary"] >= salary_median),
        "High Value",
        "Standard Value"
    )

    # --------------------------------------------------------
    # ENGAGEMENT SEGMENT
    # --------------------------------------------------------

    df["Engagement_Status"] = np.where(
        df["IsActiveMember"] == 1,
        "Active",
        "Inactive"
    )

    # --------------------------------------------------------
    # CHURN LABEL
    # --------------------------------------------------------

    df["Churn_Status"] = np.where(
        df["Exited"] == 1,
        "Churned",
        "Retained"
    )

    return df


df = preprocess_data(df)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Controls")

st.sidebar.markdown(
    "Use the filters below to explore customer churn patterns."
)


# Geography filter
geography_options = sorted(
    df["Geography"].dropna().unique().tolist()
)

selected_geography = st.sidebar.multiselect(
    "Geography",
    geography_options,
    default=geography_options
)


# Gender filter
gender_options = sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options
)


# Age group filter
age_options = [
    "<30",
    "30-45",
    "46-60",
    "60+"
]

selected_age = st.sidebar.multiselect(
    "Age Group",
    age_options,
    default=age_options
)


# Credit score filter
credit_options = [
    "Poor",
    "Fair",
    "Good",
    "Very Good",
    "Excellent"
]

selected_credit = st.sidebar.multiselect(
    "Credit Score Band",
    credit_options,
    default=credit_options
)


# Customer value
value_options = [
    "High Value",
    "Standard Value"
]

selected_value = st.sidebar.multiselect(
    "High Value",
    value_options,
    default=value_options
)


# Engagement
engagement_options = [
    "Active",
    "Inactive"
]

selected_engagement = st.sidebar.multiselect(
    "Engagement",
    engagement_options,
    default=engagement_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["Geography"].isin(selected_geography)
    &
    df["Gender"].isin(selected_gender)
    &
    df["Age_Group"].astype(str).isin(selected_age)
    &
    df["Credit_Score_Band"].astype(str).isin(selected_credit)
    &
    df["Customer_Value"].isin(selected_value)
    &
    df["Engagement_Status"].isin(selected_engagement)
].copy()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🏦 Customer Segmentation & Churn Pattern Analytics"
)

st.subheader(
    "European Banking Customer Analytics Dashboard"
)

st.write(
    """
    This interactive dashboard analyzes customer churn patterns
    across geography, demographics, financial characteristics,
    engagement levels, and customer-value segments.
    """
)

st.divider()


# ============================================================
# TOP KPIs
# ============================================================

total_customers = len(filtered_df)

churned_customers = filtered_df["Exited"].sum()

retained_customers = total_customers - churned_customers

if total_customers > 0:
    churn_rate = (
        churned_customers / total_customers
    ) * 100
else:
    churn_rate = 0

if total_customers > 0:
    active_rate = (
        filtered_df["IsActiveMember"].mean()
    ) * 100
else:
    active_rate = 0

average_balance = (
    filtered_df["Balance"].mean()
    if total_customers > 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


with col2:

    st.metric(
        "Churned Customers",
        f"{int(churned_customers):,}"
    )


with col3:

    st.metric(
        "Overall Churn Rate",
        f"{churn_rate:.2f}%"
    )


with col4:

    st.metric(
        "Active Customer Rate",
        f"{active_rate:.2f}%"
    )


with col5:

    st.metric(
        "Average Balance",
        f"${average_balance:,.0f}"
    )


st.divider()


# ============================================================
# OVERALL CHURN DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title">Overall Churn Distribution</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Churn pie chart
# ------------------------------------------------------------

with col1:

    churn_counts = (
        filtered_df["Churn_Status"]
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Churn_Status",
        "Count"
    ]

    fig = px.pie(
        churn_counts,
        names="Churn_Status",
        values="Count",
        hole=0.45,
        title="Customer Retention vs Churn"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Churn bar chart
# ------------------------------------------------------------

with col2:

    fig = px.bar(
        churn_counts,
        x="Churn_Status",
        y="Count",
        text="Count",
        title="Churn Customer Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# GEOGRAPHY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Geography-wise Churn Analysis</div>',
    unsafe_allow_html=True
)

geo_analysis = (
    filtered_df
    .groupby("Geography")
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

geo_analysis["Churn_Rate"] = (
    geo_analysis["Churned"]
    /
    geo_analysis["Customers"]
) * 100


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        geo_analysis,
        x="Geography",
        y="Customers",
        text="Customers",
        title="Customers by Geography"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        geo_analysis,
        x="Geography",
        y="Churn_Rate",
        text=geo_analysis["Churn_Rate"].round(2),
        title="Churn Rate by Geography"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AGE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">👥 Age-wise Churn Analysis</div>',
    unsafe_allow_html=True
)

age_analysis = (
    filtered_df
    .groupby("Age_Group", observed=True)
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

age_analysis["Churn_Rate"] = (
    age_analysis["Churned"]
    /
    age_analysis["Customers"]
) * 100


fig = px.bar(
    age_analysis,
    x="Age_Group",
    y="Churn_Rate",
    text=age_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Age Group"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TENURE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📅 Tenure-wise Churn Analysis</div>',
    unsafe_allow_html=True
)

tenure_analysis = (
    filtered_df
    .groupby("Tenure_Group", observed=True)
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

tenure_analysis["Churn_Rate"] = (
    tenure_analysis["Churned"]
    /
    tenure_analysis["Customers"]
) * 100


fig = px.bar(
    tenure_analysis,
    x="Tenure_Group",
    y="Churn_Rate",
    text=tenure_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Tenure Group"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CREDIT SCORE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">💳 Credit Score Analysis</div>',
    unsafe_allow_html=True
)

credit_analysis = (
    filtered_df
    .groupby("Credit_Score_Band", observed=True)
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

credit_analysis["Churn_Rate"] = (
    credit_analysis["Churned"]
    /
    credit_analysis["Customers"]
) * 100


fig = px.bar(
    credit_analysis,
    x="Credit_Score_Band",
    y="Churn_Rate",
    text=credit_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Credit Score Band"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# BALANCE SEGMENT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">💰 Balance Segment Analysis</div>',
    unsafe_allow_html=True
)

balance_analysis = (
    filtered_df
    .groupby("Balance_Segment", observed=True)
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

balance_analysis["Churn_Rate"] = (
    balance_analysis["Churned"]
    /
    balance_analysis["Customers"]
) * 100


fig = px.bar(
    balance_analysis,
    x="Balance_Segment",
    y="Churn_Rate",
    text=balance_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Balance Segment"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_tickangle=-30
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# GENDER ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">⚥ Gender-wise Churn Analysis</div>',
    unsafe_allow_html=True
)

gender_analysis = (
    filtered_df
    .groupby("Gender")
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

gender_analysis["Churn_Rate"] = (
    gender_analysis["Churned"]
    /
    gender_analysis["Customers"]
) * 100


fig = px.bar(
    gender_analysis,
    x="Gender",
    y="Churn_Rate",
    text=gender_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Gender"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📦 Product Usage & Churn</div>',
    unsafe_allow_html=True
)

product_analysis = (
    filtered_df
    .groupby("NumOfProducts")
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

product_analysis["Churn_Rate"] = (
    product_analysis["Churned"]
    /
    product_analysis["Customers"]
) * 100


fig = px.bar(
    product_analysis,
    x="NumOfProducts",
    y="Churn_Rate",
    text=product_analysis["Churn_Rate"].round(2),
    title="Churn Rate by Number of Products"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CUSTOMER ACTIVITY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Customer Engagement Analysis</div>',
    unsafe_allow_html=True
)

engagement_analysis = (
    filtered_df
    .groupby("Engagement_Status")
    .agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    )
    .reset_index()
)

engagement_analysis["Churn_Rate"] = (
    engagement_analysis["Churned"]
    /
    engagement_analysis["Customers"]
) * 100


fig = px.bar(
    engagement_analysis,
    x="Engagement_Status",
    y="Churn_Rate",
    text=engagement_analysis["Churn_Rate"].round(2),
    title="Churn Rate: Active vs Inactive Customers"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# HIGH-VALUE CUSTOMER ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">⭐ High-Value Customer Churn Analysis</div>',
    unsafe_allow_html=True
)

high_value_df = filtered_df[
    filtered_df["Customer_Value"] == "High Value"
].copy()


if len(high_value_df) > 0:

    high_value_total = len(high_value_df)

    high_value_churned = high_value_df["Exited"].sum()

    high_value_churn_rate = (
        high_value_churned
        /
        high_value_total
    ) * 100

else:

    high_value_total = 0
    high_value_churned = 0
    high_value_churn_rate = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "High-Value Customers",
        f"{high_value_total:,}"
    )


with col2:

    st.metric(
        "High-Value Churned",
        f"{int(high_value_churned):,}"
    )


with col3:

    st.metric(
        "High-Value Churn Rate",
        f"{high_value_churn_rate:.2f}%"
    )


if len(high_value_df) > 0:

    fig = px.scatter(
        high_value_df,
        x="Balance",
        y="EstimatedSalary",
        color="Churn_Status",
        size="CreditScore",
        hover_data=[
            "Geography",
            "Age",
            "Tenure",
            "NumOfProducts",
            "IsActiveMember"
        ],
        title="High-Value Customer Churn Explorer"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No high-value customers match the selected filters."
    )


# ============================================================
# BALANCE VS CHURN
# ============================================================

st.markdown(
    '<div class="section-title">📈 Financial Profile vs Churn</div>',
    unsafe_allow_html=True
)

fig = px.box(
    filtered_df,
    x="Churn_Status",
    y="Balance",
    color="Churn_Status",
    title="Balance Distribution: Churned vs Retained"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AGE VS BALANCE
# ============================================================

fig = px.scatter(
    filtered_df,
    x="Age",
    y="Balance",
    color="Churn_Status",
    size="EstimatedSalary",
    hover_data=[
        "Geography",
        "CreditScore",
        "Tenure",
        "NumOfProducts"
    ],
    title="Age vs Balance by Churn Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHURN HEATMAP DATA
# ============================================================

st.markdown(
    '<div class="section-title">🔥 Geography × Age Churn Analysis</div>',
    unsafe_allow_html=True
)

heatmap_data = (
    filtered_df
    .groupby(
        ["Geography", "Age_Group"],
        observed=True
    )["Exited"]
    .mean()
    .reset_index()
)

heatmap_data["Exited"] = (
    heatmap_data["Exited"] * 100
)


heatmap_pivot = heatmap_data.pivot(
    index="Geography",
    columns="Age_Group",
    values="Exited"
)


fig = px.imshow(
    heatmap_pivot,
    text_auto=".2f",
    aspect="auto",
    title="Churn Rate (%) by Geography and Age Group"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# KPI SUMMARY TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 KPI Summary</div>',
    unsafe_allow_html=True
)

kpi_summary = pd.DataFrame(
    {
        "KPI": [
            "Total Customers",
            "Churned Customers",
            "Retained Customers",
            "Overall Churn Rate",
            "Active Customer Rate",
            "Average Balance",
            "High-Value Customers",
            "High-Value Churned",
            "High-Value Churn Rate"
        ],
        "Value": [
            f"{total_customers:,}",
            f"{int(churned_customers):,}",
            f"{int(retained_customers):,}",
            f"{churn_rate:.2f}%",
            f"{active_rate:.2f}%",
            f"${average_balance:,.2f}",
            f"{high_value_total:,}",
            f"{int(high_value_churned):,}",
            f"{high_value_churn_rate:.2f}%"
        ]
    }
)

st.dataframe(
    kpi_summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Filtered Customer Data</div>',
    unsafe_allow_html=True
)

show_data = st.checkbox(
    "Show filtered customer records"
)

if show_data:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_customer_churn_data.csv",
    mime="text/csv"
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    # Highest geography churn
    highest_geo = (
        geo_analysis
        .sort_values(
            "Churn_Rate",
            ascending=False
        )
        .iloc[0]
    )

    # Highest age churn
    highest_age = (
        age_analysis
        .sort_values(
            "Churn_Rate",
            ascending=False
        )
        .iloc[0]
    )

    # Highest tenure churn
    highest_tenure = (
        tenure_analysis
        .sort_values(
            "Churn_Rate",
            ascending=False
        )
        .iloc[0]
    )

    # Highest credit score churn
    highest_credit = (
        credit_analysis
        .sort_values(
            "Churn_Rate",
            ascending=False
        )
        .iloc[0]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
            **Highest Geographic Churn**

            {highest_geo["Geography"]} shows the highest
            churn rate among the selected geographic segments,
            at approximately {highest_geo["Churn_Rate"]:.2f}%.
            """
        )

        st.info(
            f"""
            **Highest Age-Group Churn**

            The {highest_age["Age_Group"]} age group has the
            highest churn rate, at approximately
            {highest_age["Churn_Rate"]:.2f}%.
            """
        )

    with col2:

        st.info(
            f"""
            **Highest Tenure-Group Churn**

            The {highest_tenure["Tenure_Group"]} segment has
            the highest churn rate, at approximately
            {highest_tenure["Churn_Rate"]:.2f}%.
            """
        )

        st.info(
            f"""
            **Highest Credit-Score-Band Churn**

            The {highest_credit["Credit_Score_Band"]} credit-score
            segment has the highest churn rate among the
            selected segments.
            """
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Strategic Recommendations</div>',
    unsafe_allow_html=True
)

recommendations = [
    "Identify high-risk customer segments and prioritize retention campaigns.",
    "Monitor inactive customers because reduced engagement may be associated with churn.",
    "Develop targeted retention strategies for high-value customers.",
    "Use geography and demographic patterns to personalize customer engagement.",
    "Monitor customers with unusual product usage patterns.",
    "Combine balance, salary, tenure, credit score, and activity indicators for customer risk profiling."
]

for recommendation in recommendations:

    st.write(
        f"• {recommendation}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Customer Segmentation & Churn Pattern Analytics "
    "| European Banking | Data Science Project"
)