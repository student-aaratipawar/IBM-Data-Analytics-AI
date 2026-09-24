from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IBM Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # Get the main project folder
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Build correct dataset path
    DATA_FILE = BASE_DIR / "data" / "clean_sales.csv"

    # Check whether file exists
    if not DATA_FILE.exists():
        st.error(f"Dataset not found: {DATA_FILE}")
        st.stop()

    df = pd.read_csv(DATA_FILE)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df


df = load_data()

# ============================================================
# TITLE
# ============================================================

st.title("📊 Sales Analytics & AI Business Intelligence Dashboard")

st.markdown(
    """
    **IBM SkillsBuild – Data Analytics with AI**

    Analyze sales performance, profitability, customers, products,
    risks, opportunities and recommended business actions.
    """
)

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")

# Date filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region
regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

# Category
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

# Segment
segments = ["All"] + sorted(df["Segment"].dropna().unique().tolist())

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segments
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date)
        &
        (filtered_df["Order Date"] <= end_date)
    ]

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_segment != "All":

    filtered_df = filtered_df[
        filtered_df["Segment"] == selected_segment
    ]

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Sales"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()

total_profit = filtered_df["Profit"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)

# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Executive KPIs")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "💰 Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col4.metric(
    "🧾 Avg Order Value",
    f"${average_order_value:,.2f}"
)

col5.metric(
    "💵 Profit",
    f"${total_profit:,.0f}"
)

col6.metric(
    "📈 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# ============================================================
# PAGE TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Executive Overview",
        "📦 Sales & Product Analysis",
        "⚠️ Customer & Risk Analysis"
    ]
)

# ============================================================
# TAB 1 – EXECUTIVE OVERVIEW
# ============================================================

with tab1:

    st.subheader("📈 Revenue & Profit Trends")

    trend_df = (
        filtered_df
        .set_index("Order Date")
        .resample("ME")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_sales = px.line(
            trend_df,
            x="Order Date",
            y="Sales",
            markers=True,
            title="Monthly Revenue Trend"
        )

        fig_sales.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )

    with col2:

        fig_profit = px.line(
            trend_df,
            x="Order Date",
            y="Profit",
            markers=True,
            title="Monthly Profit Trend"
        )

        fig_profit.update_layout(
            xaxis_title="Month",
            yaxis_title="Profit"
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )

    # --------------------------------------------------------
    # CATEGORY AND REGION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    category_data = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    region_data = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    with col1:

        fig_category = px.bar(
            category_data,
            x="Category",
            y="Sales",
            title="Sales by Category",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    with col2:

        fig_region = px.bar(
            region_data,
            x="Region",
            y="Sales",
            title="Sales by Region",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    # --------------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------------

    st.subheader("💡 Key Business Findings")

    if not category_data.empty:

        top_category = category_data.iloc[0]

        st.info(
            f"**Top Category:** {top_category['Category']} "
            f"generated ${top_category['Sales']:,.2f} in sales."
        )

    if not region_data.empty:

        top_region = region_data.iloc[0]

        st.success(
            f"**Top Region:** {top_region['Region']} "
            f"generated ${top_region['Sales']:,.2f} in sales."
        )


# ============================================================
# TAB 2 – SALES & PRODUCT ANALYSIS
# ============================================================

with tab2:

    st.subheader("📦 Sales & Product Performance")

    # Category performance

    category_profit = (
        filtered_df
        .groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    category_profit["Profit Margin %"] = (
        category_profit["Profit"]
        /
        category_profit["Sales"]
        * 100
    )

    st.dataframe(
        category_profit.style.format(
            {
                "Sales": "${:,.2f}",
                "Profit": "${:,.2f}",
                "Profit Margin %": "{:.2f}%"
            }
        ),
        use_container_width=True
    )

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    product_data = (
        filtered_df
        .groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top 10 Products")

        top_products = product_data.head(10)

        fig_top = px.bar(
            top_products.sort_values("Sales"),
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top Products by Revenue"
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    with col2:

        st.subheader("📉 Bottom 10 Products")

        bottom_products = product_data.tail(10)

        fig_bottom = px.bar(
            bottom_products.sort_values("Sales"),
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Lowest Revenue Products"
        )

        st.plotly_chart(
            fig_bottom,
            use_container_width=True
        )

    # --------------------------------------------------------
    # REGION PROFITABILITY
    # --------------------------------------------------------

    region_profit = (
        filtered_df
        .groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    fig_region_profit = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_region_profit,
        use_container_width=True
    )


# ============================================================
# TAB 3 – CUSTOMER & RISK ANALYSIS
# ============================================================

with tab3:

    st.subheader("⚠️ Customer & Risk Analysis")

    # Customer analysis

    customer_data = (
        filtered_df
        .groupby("Customer ID")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        f"{len(customer_data):,}"
    )

    col2.metric(
        "Profitable Customers",
        f"{(customer_data['Profit'] > 0).sum():,}"
    )

    col3.metric(
        "Customers with Loss",
        f"{(customer_data['Profit'] < 0).sum():,}"
    )

    # --------------------------------------------------------
    # CUSTOMER SALES
    # --------------------------------------------------------

    st.subheader("👥 Top Customers")

    top_customers = customer_data.head(10)

    fig_customers = px.bar(
        top_customers.sort_values("Sales"),
        x="Sales",
        y="Customer ID",
        orientation="h",
        title="Top 10 Customers by Revenue"
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )

    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    st.subheader("🚨 Business Risks")

    negative_products = product_data[
        product_data["Profit"] < 0
    ]

    negative_product_count = len(negative_products)

    low_profit_categories = category_profit[
        category_profit["Profit"] < 0
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Loss-Making Products",
        f"{negative_product_count:,}"
    )

    col2.metric(
        "Loss-Making Categories",
        f"{len(low_profit_categories):,}"
    )

    col3.metric(
        "Total Loss",
        f"${abs(filtered_df[filtered_df['Profit'] < 0]['Profit'].sum()):,.0f}"
    )

    if negative_product_count > 0:

        st.warning(
            f"There are **{negative_product_count} products** "
            "with negative total profit. These products should "
            "be reviewed for pricing, discount and cost issues."
        )

    else:

        st.success(
            "No loss-making products were detected in the "
            "selected filters."
        )

    # --------------------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------------------

    st.subheader("🚀 Business Opportunities")

    st.markdown(
        """
        **1. Improve high-sales / low-profit products**

        Identify products generating strong revenue but weak
        profitability and review their pricing and discount strategy.

        **2. Expand high-performing categories**

        Focus marketing and inventory planning on categories
        producing strong sales and profitability.

        **3. Improve regional performance**

        Investigate lower-performing regions and identify
        opportunities for better customer acquisition and retention.
        """
    )

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    st.subheader("🎯 Recommended Actions")

    st.markdown(
        """
        | Priority Area | Recommended Action |
        |---|---|
        | Product Profitability | Review discounts and pricing |
        | Inventory | Use monthly sales trends for planning |
        | Regions | Investigate low-profit regions |
        | Customers | Focus on high-value customer segments |
        | Product Mix | Reduce exposure to consistently loss-making products |
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "IBM SkillsBuild – Data Analytics with AI | "
    "Sales Analytics & Business Intelligence Project"
)