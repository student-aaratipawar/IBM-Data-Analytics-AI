import pandas as pd
import os

# ============================================================
# IBM DATA ANALYTICS WITH AI
# DATA CLEANING
# ============================================================

input_file = "data/sales.xlsx"
output_file = "data/clean_sales.csv"

print("=" * 70)
print("          IBM DATA ANALYTICS WITH AI PROJECT")
print("                    DATA CLEANING")
print("=" * 70)


# ============================================================
# 1. CHECK INPUT FILE
# ============================================================

if not os.path.exists(input_file):

    print("\nERROR: Dataset not found!")
    print("Expected location:")
    print(os.path.abspath(input_file))
    exit()

print("\nOriginal dataset found:")
print(os.path.abspath(input_file))


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_excel(input_file)

print("\nDataset loaded successfully.")

print("\nOriginal dataset shape:")
print(df.shape)


# ============================================================
# 3. DISPLAY COLUMN NAMES
# ============================================================

print("\nOriginal columns:")

for column in df.columns:
    print("-", column)


# ============================================================
# 4. REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

if duplicate_count > 0:

    df = df.drop_duplicates()

    print(
        "Duplicate rows removed:",
        duplicate_count
    )

else:

    print("No duplicate rows found.")


# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

print("\nMissing values BEFORE cleaning:")

missing_before = df.isnull().sum()

print(
    missing_before[
        missing_before > 0
    ].to_string()
)


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

# For numeric columns:
# Replace missing values with median.

numeric_columns = df.select_dtypes(
    include="number"
).columns

for column in numeric_columns:

    if df[column].isnull().sum() > 0:

        median_value = df[column].median()

        df[column] = df[column].fillna(
            median_value
        )

        print(
            f"\nMissing numeric values in "
            f"'{column}' replaced with median:"
            f" {median_value}"
        )


# For text/categorical columns:
# Replace missing values with "Unknown".

categorical_columns = df.select_dtypes(
    include="object"
).columns

for column in categorical_columns:

    if df[column].isnull().sum() > 0:

        df[column] = df[column].fillna(
            "Unknown"
        )

        print(
            f"\nMissing categorical values in "
            f"'{column}' replaced with 'Unknown'."
        )


# ============================================================
# 7. CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "Order Date",
    "Ship Date"
]

for column in date_columns:

    if column in df.columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        print(
            f"\nConverted '{column}' to datetime."
        )


# ============================================================
# 8. CHECK INVALID NUMERIC VALUES
# ============================================================

print("\nChecking numeric columns for invalid values...")

for column in numeric_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    print(
        f"{column}: "
        f"{negative_count} negative values"
    )


# ============================================================
# 9. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
)

print("\nColumn names standardized.")


# ============================================================
# 10. CREATE USEFUL DATE FEATURES
# ============================================================

if "Order Date" in df.columns:

    df["Order Year"] = (
        df["Order Date"].dt.year
    )

    df["Order Month"] = (
        df["Order Date"].dt.month
    )

    df["Order Month Name"] = (
        df["Order Date"].dt.month_name()
    )

    df["Order Quarter"] = (
        "Q"
        + df["Order Date"]
        .dt.quarter
        .astype(str)
    )

    print(
        "\nCreated date analysis columns:"
    )

    print("- Order Year")
    print("- Order Month")
    print("- Order Month Name")
    print("- Order Quarter")


# ============================================================
# 11. CREATE PROFIT MARGIN
# ============================================================

if "Sales" in df.columns and "Profit" in df.columns:

    df["Profit Margin"] = (
        df["Profit"]
        / df["Sales"]
        * 100
    )

    # Avoid infinite values
    df["Profit Margin"] = (
        df["Profit Margin"]
        .replace(
            [float("inf"), -float("inf")],
            0
        )
    )

    print(
        "\nCreated 'Profit Margin' column."
    )


# ============================================================
# 12. CHECK MISSING VALUES AFTER CLEANING
# ============================================================

print("\nMissing values AFTER cleaning:")

missing_after = df.isnull().sum()

remaining_missing = (
    missing_after[
        missing_after > 0
    ]
)

if len(remaining_missing) > 0:

    print(
        remaining_missing.to_string()
    )

else:

    print("No missing values remaining.")


# ============================================================
# 13. FINAL DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET INFORMATION")
print("=" * 70)

print("\nRows       :", df.shape[0])
print("Columns    :", df.shape[1])
print(
    "Duplicates :",
    df.duplicated().sum()
)
print(
    "Missing    :",
    df.isnull().sum().sum()
)


# ============================================================
# 14. SAVE CLEAN DATASET
# ============================================================

df.to_csv(
    output_file,
    index=False
)

print("\nClean dataset saved successfully!")

print(
    "Location:",
    os.path.abspath(output_file)
)


# ============================================================
# 15. COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("              DATA CLEANING COMPLETED")
print("=" * 70)

print("\nNext Step: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 70)