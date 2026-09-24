import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# IBM DATA ANALYTICS WITH AI
# EXPLORATORY DATA ANALYSIS
# ============================================================

input_file = "data/clean_sales.csv"
output_folder = "images"

print("=" * 70)
print("          IBM DATA ANALYTICS WITH AI PROJECT")
print("             EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# ============================================================
# 1. CHECK FILE
# ============================================================

if not os.path.exists(input_file):

    print("\nERROR: Clean dataset not found!")

    print(
        "Expected:",
        os.path.abspath(input_file)
    )

    exit()


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(input_file)

print("\nClean dataset loaded successfully.")

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# ============================================================
# 3. CONVERT DATE
# ============================================================

if "Order Date" in df.columns:

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )


# ============================================================
# 4. BASIC BUSINESS KPIs
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC BUSINESS KPIs")
print("=" * 70)

if "Sales" in df.columns:

    total_sales = df["Sales"].sum()

    print(
        f"\nTotal Sales: ${total_sales:,.2f}"
    )


if "Profit" in df.columns:

    total_profit = df["Profit"].sum()

    print(
        f"Total Profit: ${total_profit:,.2f}"
    )


if "Order ID" in df.columns:

    total_orders = df["Order ID"].nunique()

    print(
        f"Total Orders: {total_orders:,}"
    )


if "Customer ID" in df.columns:

    total_customers = df["Customer ID"].nunique()

    print(
        f"Total Customers: {total_customers:,}"
    )


if (
    "Sales" in df.columns
    and "Order ID" in df.columns
):

    average_order_value = (
        total_sales / total_orders
    )

    print(
        f"Average Order Value: "
        f"${average_order_value:,.2f}"
    )


# ============================================================
# 5. SALES BY CATEGORY
# ============================================================

if (
    "Category" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("2. SALES BY CATEGORY")
    print("=" * 70)

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        category_sales.to_string()
    )


# ============================================================
# 6. PROFIT BY CATEGORY
# ============================================================

if (
    "Category" in df.columns
    and "Profit" in df.columns
):

    print("\n" + "=" * 70)
    print("3. PROFIT BY CATEGORY")
    print("=" * 70)

    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        category_profit.to_string()
    )


# ============================================================
# 7. SALES BY REGION
# ============================================================

if (
    "Region" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("4. SALES BY REGION")
    print("=" * 70)

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        region_sales.to_string()
    )


# ============================================================
# 8. PROFIT BY REGION
# ============================================================

if (
    "Region" in df.columns
    and "Profit" in df.columns
):

    print("\n" + "=" * 70)
    print("5. PROFIT BY REGION")
    print("=" * 70)

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        region_profit.to_string()
    )


# ============================================================
# 9. SALES BY SEGMENT
# ============================================================

if (
    "Segment" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("6. SALES BY CUSTOMER SEGMENT")
    print("=" * 70)

    segment_sales = (
        df.groupby("Segment")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        segment_sales.to_string()
    )


# ============================================================
# 10. TOP 10 PRODUCTS
# ============================================================

if (
    "Product Name" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("7. TOP 10 PRODUCTS BY SALES")
    print("=" * 70)

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print(
        top_products.to_string()
    )


# ============================================================
# 11. BOTTOM 10 PRODUCTS
# ============================================================

if (
    "Product Name" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("8. BOTTOM 10 PRODUCTS BY SALES")
    print("=" * 70)

    bottom_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(
            ascending=True
        )
        .head(10)
    )

    print(
        bottom_products.to_string()
    )


# ============================================================
# 12. MONTHLY SALES
# ============================================================

if (
    "Order Date" in df.columns
    and "Sales" in df.columns
):

    print("\n" + "=" * 70)
    print("9. MONTHLY SALES")
    print("=" * 70)

    monthly_sales = (
        df.set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
    )

    print(
        monthly_sales.to_string()
    )


# ============================================================
# 13. MONTHLY PROFIT
# ============================================================

if (
    "Order Date" in df.columns
    and "Profit" in df.columns
):

    print("\n" + "=" * 70)
    print("10. MONTHLY PROFIT")
    print("=" * 70)

    monthly_profit = (
        df.set_index("Order Date")
        .resample("ME")["Profit"]
        .sum()
    )

    print(
        monthly_profit.to_string()
    )


# ============================================================
# 14. CREATE CHART FOLDER
# ============================================================

os.makedirs(
    output_folder,
    exist_ok=True
)


# ============================================================
# 15. SALES BY CATEGORY CHART
# ============================================================

if (
    "Category" in df.columns
    and "Sales" in df.columns
):

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=category_sales.index,
        y=category_sales.values
    )

    plt.title(
        "Sales by Category"
    )

    plt.xlabel("Category")

    plt.ylabel("Sales")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        f"{output_folder}/sales_by_category.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 16. SALES BY REGION CHART
# ============================================================

if (
    "Region" in df.columns
    and "Sales" in df.columns
):

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=region_sales.index,
        y=region_sales.values
    )

    plt.title(
        "Sales by Region"
    )

    plt.xlabel("Region")

    plt.ylabel("Sales")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        f"{output_folder}/sales_by_region.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 17. MONTHLY SALES CHART
# ============================================================

if (
    "Order Date" in df.columns
    and "Sales" in df.columns
):

    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_sales.index,
        monthly_sales.values,
        marker="o"
    )

    plt.title(
        "Monthly Sales Trend"
    )

    plt.xlabel("Date")

    plt.ylabel("Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        f"{output_folder}/monthly_sales.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 18. MONTHLY PROFIT CHART
# ============================================================

if (
    "Order Date" in df.columns
    and "Profit" in df.columns
):

    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_profit.index,
        monthly_profit.values,
        marker="o"
    )

    plt.title(
        "Monthly Profit Trend"
    )

    plt.xlabel("Date")

    plt.ylabel("Profit")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        f"{output_folder}/monthly_profit.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 19. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("              EDA COMPLETED")
print("=" * 70)

print("\nCharts saved in:")
print(
    os.path.abspath(output_folder)
)

print("\nNext Step:")
print("KPI CALCULATION + BUSINESS INSIGHTS")

print("=" * 70)