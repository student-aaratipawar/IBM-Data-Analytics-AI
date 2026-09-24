import pandas as pd
import os

# ============================================================
# IBM DATA ANALYTICS WITH AI
# DATASET CHECK
# ============================================================

file_path = "data/sales.xlsx"

print("=" * 70)
print("          IBM DATA ANALYTICS WITH AI PROJECT")
print("                DATASET CHECK")
print("=" * 70)


# ============================================================
# 1. CHECK FILE
# ============================================================

if not os.path.exists(file_path):
    print("\nERROR: Dataset file not found!")
    print("Expected location:")
    print(os.path.abspath(file_path))
    exit()

print("\nDataset file found successfully!")
print("File:", os.path.abspath(file_path))


# ============================================================
# 2. READ EXCEL FILE
# ============================================================

try:
    excel_file = pd.ExcelFile(file_path)

    print("\nAVAILABLE SHEETS")
    print("-" * 40)

    for sheet in excel_file.sheet_names:
        print("-", sheet)

except Exception as e:
    print("\nERROR while opening Excel file:")
    print(e)
    exit()


# ============================================================
# 3. READ FIRST SHEET
# ============================================================

sheet_name = excel_file.sheet_names[0]

print("\nReading sheet:", sheet_name)

try:
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

except Exception as e:
    print("\nERROR while reading Excel data:")
    print(e)
    exit()


# ============================================================
# 4. SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 70)


# ============================================================
# 5. DATASET SHAPE
# ============================================================

print("\n1. DATASET SHAPE")
print("-" * 40)

print("Number of Rows    :", df.shape[0])
print("Number of Columns :", df.shape[1])


# ============================================================
# 6. COLUMN NAMES
# ============================================================

print("\n2. COLUMN NAMES")
print("-" * 40)

for number, column in enumerate(df.columns, start=1):
    print(f"{number}. {column}")


# ============================================================
# 7. FIRST 5 ROWS
# ============================================================

print("\n3. FIRST 5 ROWS")
print("-" * 40)

print(df.head().to_string())


# ============================================================
# 8. DATA TYPES
# ============================================================

print("\n4. DATA TYPES")
print("-" * 40)

print(df.dtypes.to_string())


# ============================================================
# 9. MISSING VALUES
# ============================================================

print("\n5. MISSING VALUES")
print("-" * 40)

print(df.isnull().sum().to_string())


# ============================================================
# 10. DUPLICATE ROWS
# ============================================================

print("\n6. DUPLICATE ROWS")
print("-" * 40)

print("Number of duplicate rows:", df.duplicated().sum())


# ============================================================
# 11. NUMERICAL STATISTICS
# ============================================================

print("\n7. NUMERICAL STATISTICS")
print("-" * 40)

numeric_columns = df.select_dtypes(include="number").columns

if len(numeric_columns) > 0:
    print(
        df[numeric_columns]
        .describe()
        .transpose()
        .to_string()
    )
else:
    print("No numerical columns found.")


# ============================================================
# 12. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("              DATASET CHECK COMPLETED")
print("=" * 70)

print("\nRows       :", df.shape[0])
print("Columns    :", df.shape[1])
print("Duplicates :", df.duplicated().sum())
print("Missing    :", df.isnull().sum().sum())

print("\nNext Step: DATA CLEANING")
print("=" * 70)