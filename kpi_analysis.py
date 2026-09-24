import pandas as pd
import os

# ============================================================
# IBM DATA ANALYTICS WITH AI
# KPI CALCULATION
# ============================================================

input_file = "data/clean_sales.csv"
output_file = "data/kpi_summary.csv"

print("=" * 70)
print("          IBM DATA ANALYTICS WITH AI PROJECT")
print("                 KPI ANALYSIS")
print("=" * 70)

# ============================================================
# 1. LOAD DATA
# ============================================================

if not os.path.exists(input_file):
    print("\nERROR: Clean dataset not found!")
    exit()

df = pd.read_csv(input_file)

# Convert date
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

print("\nDataset loaded successfully.")
print("Rows:", len(df))


# ============================================================
# 2. KPI CALCULATIONS
# ============================================================

# Revenue
total_revenue = df["Sales"].sum()

# Orders
total_orders = df["Order ID"].nunique()

# Customers
total_customers = df["Customer ID"].nunique()

# Profit
total_profit = df["Profit"].sum()

# Average Order Value
average_order_value = (
    total_revenue / total_orders
)

# Profit Margin
profit_margin = (
    total_profit / total_revenue
) * 100


# ============================================================
# 3. GROWTH CALCULATION
# ============================================================

df["Order Year"] = df["Order Date"].dt.year

yearly_sales = (
    df.groupby("Order Year")["Sales"]
    .sum()
    .sort_index()
)

if len(yearly_sales) >= 2:

    current_year_sales = yearly_sales.iloc[-1]
    previous_year_sales = yearly_sales.iloc[-2]

    growth_percentage = (
        (current_year_sales - previous_year_sales)
        / previous_year_sales
    ) * 100

else:

    growth_percentage = 0


# ============================================================
# 4. DISPLAY KPIs
# ============================================================

print("\n" + "=" * 70)
print("                    EXECUTIVE KPIs")
print("=" * 70)

print(f"\nTotal Revenue      : ${total_revenue:,.2f}")
print(f"Total Orders       : {total_orders:,}")
print(f"Total Customers    : {total_customers:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")
print(f"Total Profit       : ${total_profit:,.2f}")
print(f"Profit Margin      : {profit_margin:.2f}%")
print(f"Year-over-Year Growth: {growth_percentage:.2f}%")


# ============================================================
# 5. TOP CATEGORY
# ============================================================

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_sales.index[0]
top_category_sales = category_sales.iloc[0]

print("\n" + "=" * 70)
print("                    TOP CATEGORY")
print("=" * 70)

print(
    f"\nTop Category: {top_category}"
)

print(
    f"Sales: ${top_category_sales:,.2f}"
)


# ============================================================
# 6. TOP REGION
# ============================================================

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

top_region = region_sales.index[0]
top_region_sales = region_sales.iloc[0]

print("\n" + "=" * 70)
print("                    TOP REGION")
print("=" * 70)

print(
    f"\nTop Region: {top_region}"
)

print(
    f"Sales: ${top_region_sales:,.2f}"
)


# ============================================================
# 7. MOST PROFITABLE CATEGORY
# ============================================================

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

top_profit_category = category_profit.index[0]

print("\n" + "=" * 70)
print("                MOST PROFITABLE CATEGORY")
print("=" * 70)

print(
    f"\nCategory: {top_profit_category}"
)

print(
    f"Profit: ${category_profit.iloc[0]:,.2f}"
)


# ============================================================
# 8. LEAST PROFITABLE CATEGORY
# ============================================================

lowest_profit_category = category_profit.index[-1]

print("\n" + "=" * 70)
print("                LOWEST PROFIT CATEGORY")
print("=" * 70)

print(
    f"\nCategory: {lowest_profit_category}"
)

print(
    f"Profit: ${category_profit.iloc[-1]:,.2f}"
)


# ============================================================
# 9. TOP 10 PRODUCTS
# ============================================================

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 70)
print("                 TOP 10 PRODUCTS")
print("=" * 70)

print(top_products.to_string())


# ============================================================
# 10. YEARLY SALES
# ============================================================

print("\n" + "=" * 70)
print("                    YEARLY SALES")
print("=" * 70)

print(yearly_sales.to_string())


# ============================================================
# 11. SAVE KPI SUMMARY
# ============================================================

kpi_data = {
    "KPI": [
        "Total Revenue",
        "Total Orders",
        "Total Customers",
        "Average Order Value",
        "Total Profit",
        "Profit Margin",
        "Growth Percentage",
        "Top Category",
        "Top Region",
        "Most Profitable Category",
        "Lowest Profit Category"
    ],

    "Value": [
        total_revenue,
        total_orders,
        total_customers,
        average_order_value,
        total_profit,
        profit_margin,
        growth_percentage,
        top_category,
        top_region,
        top_profit_category,
        lowest_profit_category
    ]
}

kpi_df = pd.DataFrame(kpi_data)

kpi_df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("KPI SUMMARY SAVED")
print("=" * 70)

print(
    "Location:",
    os.path.abspath(output_file)
)

print("\nNext Step: BUSINESS INSIGHTS")

print("=" * 70)