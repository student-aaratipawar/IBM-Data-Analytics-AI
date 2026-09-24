import pandas as pd
import os

# ============================================================
# BUSINESS INSIGHTS ANALYSIS
# IBM DATA ANALYTICS WITH AI PROJECT
# ============================================================

INPUT_FILE = "data/clean_sales.csv"
OUTPUT_FILE = "data/business_insights.csv"

print("=" * 70)
print("              BUSINESS INSIGHTS ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["Order Date"] = pd.to_datetime(df["Order Date"])

print(f"\nDataset loaded successfully")
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# ------------------------------------------------------------
# 2. CATEGORY ANALYSIS
# ------------------------------------------------------------

category_analysis = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

category_analysis["Profit Margin %"] = (
    category_analysis["Profit"] /
    category_analysis["Sales"] * 100
)

category_analysis = category_analysis.sort_values(
    "Sales", ascending=False
)


# ------------------------------------------------------------
# 3. REGION ANALYSIS
# ------------------------------------------------------------

region_analysis = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Customers=("Customer ID", "nunique")
    )
    .reset_index()
)

region_analysis["Profit Margin %"] = (
    region_analysis["Profit"] /
    region_analysis["Sales"] * 100
)

region_analysis = region_analysis.sort_values(
    "Sales", ascending=False
)


# ------------------------------------------------------------
# 4. PRODUCT ANALYSIS
# ------------------------------------------------------------

product_analysis = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

product_analysis["Profit Margin %"] = (
    product_analysis["Profit"] /
    product_analysis["Sales"] * 100
)

top_products = product_analysis.sort_values(
    "Sales", ascending=False
).head(10)

bottom_products = product_analysis.sort_values(
    "Sales", ascending=True
).head(10)


# ------------------------------------------------------------
# 5. YEARLY TREND
# ------------------------------------------------------------

df["Year"] = df["Order Date"].dt.year

yearly_sales = (
    df.groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

yearly_profit = (
    df.groupby("Year")["Profit"]
    .sum()
    .reset_index()
)


# ------------------------------------------------------------
# 6. MONTHLY TREND
# ------------------------------------------------------------

df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

monthly_profit = (
    df.groupby("Month")["Profit"]
    .sum()
    .reset_index()
)


# ============================================================
# BUSINESS FINDINGS
# ============================================================

print("\n")
print("=" * 70)
print("                    KEY FINDINGS")
print("=" * 70)


# Finding 1
top_category = category_analysis.iloc[0]

print("\n1. TOP CATEGORY")
print(
    f"{top_category['Category']} generated the highest sales "
    f"of ${top_category['Sales']:,.2f}."
)


# Finding 2
top_region = region_analysis.iloc[0]

print("\n2. TOP REGION")
print(
    f"{top_region['Region']} generated the highest sales "
    f"of ${top_region['Sales']:,.2f}."
)


# Finding 3
most_profitable_category = category_analysis.sort_values(
    "Profit", ascending=False
).iloc[0]

print("\n3. MOST PROFITABLE CATEGORY")
print(
    f"{most_profitable_category['Category']} generated the highest "
    f"profit of ${most_profitable_category['Profit']:,.2f}."
)


# Finding 4
lowest_profit_category = category_analysis.sort_values(
    "Profit", ascending=True
).iloc[0]

print("\n4. LOWEST PROFIT CATEGORY")
print(
    f"{lowest_profit_category['Category']} generated the lowest "
    f"profit of ${lowest_profit_category['Profit']:,.2f}."
)


# Finding 5
top_product = product_analysis.iloc[
    product_analysis["Sales"].idxmax()
]

print("\n5. TOP PRODUCT")
print(
    f"{top_product['Product Name']} generated sales of "
    f"${top_product['Sales']:,.2f}."
)


# ============================================================
# RISKS
# ============================================================

print("\n")
print("=" * 70)
print("                         RISKS")
print("=" * 70)

print("\nRisk 1:")
print(
    f"{lowest_profit_category['Category']} has the lowest total "
    f"profit among the categories."
)

lowest_profit_region = region_analysis.sort_values(
    "Profit", ascending=True
).iloc[0]

print("\nRisk 2:")
print(
    f"{lowest_profit_region['Region']} has the lowest regional "
    f"profit of ${lowest_profit_region['Profit']:,.2f}."
)

negative_products = product_analysis[
    product_analysis["Profit"] < 0
]

print("\nRisk 3:")
print(
    f"{len(negative_products)} products have negative total profit."
)


# ============================================================
# OPPORTUNITIES
# ============================================================

print("\n")
print("=" * 70)
print("                     OPPORTUNITIES")
print("=" * 70)

print("\nOpportunity 1:")
print(
    f"Focus on the {top_category['Category']} category because "
    f"it generates the highest sales."
)

highest_margin_category = category_analysis.sort_values(
    "Profit Margin %", ascending=False
).iloc[0]

print("\nOpportunity 2:")
print(
    f"{highest_margin_category['Category']} has the highest "
    f"profit margin of "
    f"{highest_margin_category['Profit Margin %']:.2f}%."
)

print("\nOpportunity 3:")
print(
    f"Improve performance of low-profit products and categories "
    f"through pricing, discounts, and product mix optimization."
)


# ============================================================
# ACTIONS
# ============================================================

print("\n")
print("=" * 70)
print("                 RECOMMENDED ACTIONS")
print("=" * 70)

print("\nAction 1:")
print(
    "Increase focus on high-performing categories and products."
)

print("\nAction 2:")
print(
    "Review pricing and discount strategies for low-profit products."
)

print("\nAction 3:")
print(
    "Investigate regions with lower profitability and identify "
    "the factors affecting their margins."
)

print("\nAction 4:")
print(
    "Monitor products generating negative profit."
)

print("\nAction 5:")
print(
    "Use monthly sales trends to support inventory and sales planning."
)


# ============================================================
# SAVE INSIGHTS
# ============================================================

insights = []

for _, row in category_analysis.iterrows():

    insights.append({
        "Type": "Category",
        "Entity": row["Category"],
        "Sales": row["Sales"],
        "Profit": row["Profit"],
        "Profit Margin %": row["Profit Margin %"]
    })


for _, row in region_analysis.iterrows():

    insights.append({
        "Type": "Region",
        "Entity": row["Region"],
        "Sales": row["Sales"],
        "Profit": row["Profit"],
        "Profit Margin %": row["Profit Margin %"]
    })


insights_df = pd.DataFrame(insights)

insights_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n")
print("=" * 70)
print("             BUSINESS INSIGHTS COMPLETED")
print("=" * 70)

print(f"\nInsights saved successfully!")
print(f"Location: {os.path.abspath(OUTPUT_FILE)}")

print("\nNext Step: STREAMLIT DASHBOARD")
print("=" * 70)