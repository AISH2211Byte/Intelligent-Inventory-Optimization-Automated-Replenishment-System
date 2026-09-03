
#sales data

'''
import pandas as pd

# Location of our raw Dataset A
file_path = "data/raw/sales_data.csv"

# Read the CSV
df = pd.read_csv(file_path)

# Basic information
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nUnique Stores:")
print(df["Store ID"].unique())
print("Number of stores:", df["Store ID"].nunique())

print("\nUnique Products:")
print(df["Product ID"].unique())
print("Number of products:", df["Product ID"].nunique())

print("\nDate range:")
print("Start:", df["Date"].min())
print("End:", df["Date"].max())

print("\nDuplicate Date + Store + Product combinations:")
print(
    df.duplicated(
        subset=["Date", "Store ID", "Product ID"]
    ).sum()
)

print("\nPromotion values:")
print(df["Promotion"].unique())

print("\nEpidemic values:")
print(df["Epidemic"].unique())

print("\nInventory Level statistics:")
print(df["Inventory Level"].describe())

print("\nUnits Sold statistics:")
print(df["Units Sold"].describe())

print("\nUnits Ordered statistics:")
print(df["Units Ordered"].describe())

print("\nSample inventory history:")
sample = df[
    (df["Store ID"] == "S001") &
    (df["Product ID"] == "P0001")
].copy()

print(
    sample[
        [
            "Date",
            "Inventory Level",
            "Units Sold",
            "Units Ordered",
            "Demand"
        ]
    ].head(15).to_string(index=False)
)

'''


#supply chain data

'''import pandas as pd

file_path = "data/raw/supply_chain_dataset1.csv"

df = pd.read_csv(file_path)

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())'''


'''import pandas as pd

file_path = "data/raw/supply_chain_dataset1.csv"

df = pd.read_csv(file_path)
print("\nDuplicate rows:", df.duplicated().sum())

print("\nNumber of SKUs:", df["SKU_ID"].nunique())
print("Number of Warehouses:", df["Warehouse_ID"].nunique())
print("Number of Suppliers:", df["Supplier_ID"].nunique())

print("\nDate range:")
print("Start:", df["Date"].min())
print("End:", df["Date"].max())

print("\nStockout values:")
print(df["Stockout_Flag"].unique())

print("\nPromotion values:")
print(df["Promotion_Flag"].unique())'''

'''import pandas as pd

file_path = "data/raw/supply_chain_dataset1.csv"

df = pd.read_csv(file_path)

print("\nSKUs per warehouse:")
print(
    df.groupby("Warehouse_ID")["SKU_ID"]
      .nunique()
)

print("\nSuppliers per SKU:")
print(
    df.groupby("SKU_ID")["Supplier_ID"]
      .nunique()
)

print("\nMultiple suppliers for same SKU:")
print(
    df.groupby("SKU_ID")["Supplier_ID"]
      .nunique()
      .loc[lambda x: x > 1]
)

print("\nDate duplicates within SKU + Warehouse:")
print(
    df.duplicated(
        subset=["Date", "SKU_ID", "Warehouse_ID"]
    ).sum()
)'''

'''import pandas as pd

file_path = "data/raw/supply_chain_dataset1.csv"

df = pd.read_csv(file_path)
print("\nSKU + Warehouse + Date with multiple suppliers:")

print(
    df.groupby(
        ["Date", "SKU_ID", "Warehouse_ID"]
    )["Supplier_ID"]
    .nunique()
    .loc[lambda x: x > 1]
)'''

#dataset c
'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Check the unique values and frequency of important categorical columns

print("Suppliers:")
print(df_c["Supplier"].value_counts())

print("\nItem Categories:")
print(df_c["Item_Category"].value_counts())

print("\nOrder Status:")
print(df_c["Order_Status"].value_counts())

print("\nCompliance:")
print(df_c["Compliance"].value_counts())'''


import pandas as pd

# Load Dataset C
'''df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Check Delivery_Date missing values by Order_Status
delivery_check = (
    df_c.groupby("Order_Status")["Delivery_Date"]
    .apply(lambda x: x.isna().sum())
)

print("Missing Delivery_Date by Order Status:")
print(delivery_check)

# Check Defective_Units missing values by Order_Status
defect_check = (
    df_c.groupby("Order_Status")["Defective_Units"]
    .apply(lambda x: x.isna().sum())
)

print("\nMissing Defective_Units by Order Status:")
print(defect_check)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Find delivered orders where Delivery_Date is missing
delivered_missing_delivery = df_c[
    (df_c["Order_Status"] == "Delivered") &
    (df_c["Delivery_Date"].isna())
]

print("Delivered orders with missing Delivery_Date:")
print(delivered_missing_delivery.head(20))

print(
    "\nNumber of such rows:",
    len(delivered_missing_delivery)
)


# Find delivered orders where Defective_Units is missing
delivered_missing_defects = df_c[
    (df_c["Order_Status"] == "Delivered") &
    (df_c["Defective_Units"].isna())
]

print("\nDelivered orders with missing Defective_Units:")
print(delivered_missing_defects.head(20))

print(
    "\nNumber of such rows:",
    len(delivered_missing_defects)
)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Display all column names
print("Columns in Dataset C:")
print(df_c.columns.tolist())

# Display data types
print("\nData types:")
print(df_c.dtypes)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Convert Order_Date from string to datetime
df_c["Order_Date"] = pd.to_datetime(
    df_c["Order_Date"],
    errors="coerce"
)

# Convert Delivery_Date from string to datetime
df_c["Delivery_Date"] = pd.to_datetime(
    df_c["Delivery_Date"],
    errors="coerce"
)

# Count missing dates after conversion
print("Missing Order_Date:")
print(df_c["Order_Date"].isna().sum())

print("\nMissing Delivery_Date:")
print(df_c["Delivery_Date"].isna().sum())

# Check whether any delivery date occurs before the order date
invalid_delivery_dates = df_c[
    df_c["Delivery_Date"] < df_c["Order_Date"]
]

print("\nDelivery dates before Order dates:")
print(len(invalid_delivery_dates))

# Display the date range
print("\nOrder date range:")
print("Start:", df_c["Order_Date"].min())
print("End:", df_c["Order_Date"].max())

print("\nDelivery date range:")
print("Start:", df_c["Delivery_Date"].min())
print("End:", df_c["Delivery_Date"].max())'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Convert date columns from strings to datetime
df_c["Order_Date"] = pd.to_datetime(
    df_c["Order_Date"],
    errors="coerce"
)

df_c["Delivery_Date"] = pd.to_datetime(
    df_c["Delivery_Date"],
    errors="coerce"
)

# Find records where delivery happened before the order
invalid_dates = df_c[
    df_c["Delivery_Date"] < df_c["Order_Date"]
]

# Display the complete problematic record
print("Invalid delivery-date record:")
print(invalid_dates.to_string(index=False))'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Convert date columns to datetime
df_c["Order_Date"] = pd.to_datetime(
    df_c["Order_Date"],
    errors="coerce"
)

df_c["Delivery_Date"] = pd.to_datetime(
    df_c["Delivery_Date"],
    errors="coerce"
)

# Create a flag for missing Delivery_Date
df_c["Missing_Delivery_Date"] = (
    df_c["Delivery_Date"].isna()
)

# Missing Delivery_Date by Supplier
print("Missing Delivery_Date by Supplier:")
print(
    df_c.groupby("Supplier")["Missing_Delivery_Date"]
    .sum()
)

# Missing Delivery_Date by Item Category
print("\nMissing Delivery_Date by Item Category:")
print(
    df_c.groupby("Item_Category")["Missing_Delivery_Date"]
    .sum()
)

# Missing Delivery_Date by Order Status
print("\nMissing Delivery_Date by Order Status:")
print(
    df_c.groupby("Order_Status")["Missing_Delivery_Date"]
    .sum()
)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Create a flag for missing Defective_Units
df_c["Missing_Defective_Units"] = (
    df_c["Defective_Units"].isna()
)

# Missing Defective_Units by Supplier
print("Missing Defective_Units by Supplier:")
print(
    df_c.groupby("Supplier")["Missing_Defective_Units"]
    .sum()
)

# Missing Defective_Units by Item Category
print("\nMissing Defective_Units by Item Category:")
print(
    df_c.groupby("Item_Category")["Missing_Defective_Units"]
    .sum()
)

# Missing Defective_Units by Order Status
print("\nMissing Defective_Units by Order Status:")
print(
    df_c.groupby("Order_Status")["Missing_Defective_Units"]
    .sum()
)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Check duplicate PO_IDs
duplicate_po_ids = df_c[df_c["PO_ID"].duplicated(keep=False)]

print("Number of duplicate PO_ID rows:")
print(len(duplicate_po_ids))

print("\nDuplicate PO_IDs:")
print(duplicate_po_ids["PO_ID"].value_counts())'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Check for zero or negative quantities
invalid_quantity = df_c[df_c["Quantity"] <= 0]

print("Number of orders with zero or negative Quantity:")
print(len(invalid_quantity))

print("\nOrders with zero or negative Quantity:")
print(invalid_quantity)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Check for zero or negative Unit_Price
invalid_unit_price = df_c[df_c["Unit_Price"] <= 0]

print("Orders with zero or negative Unit_Price:")
print(len(invalid_unit_price))
print(invalid_unit_price)

# Check for zero or negative Negotiated_Price
invalid_negotiated_price = df_c[df_c["Negotiated_Price"] <= 0]

print("\nOrders with zero or negative Negotiated_Price:")
print(len(invalid_negotiated_price))
print(invalid_negotiated_price)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Find orders where negotiated price is higher than unit price
higher_negotiated_price = df_c[
    df_c["Negotiated_Price"] > df_c["Unit_Price"]
]

print("Orders where Negotiated_Price > Unit_Price:")
print(len(higher_negotiated_price))

print("\nThese orders are:")
print(higher_negotiated_price[
    ["PO_ID", "Supplier", "Quantity", "Unit_Price", "Negotiated_Price"]
])'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Check for negative defective units
negative_defects = df_c[
    df_c["Defective_Units"] < 0
]

print("Orders with negative Defective_Units:")
print(len(negative_defects))

print(negative_defects[
    ["PO_ID", "Quantity", "Defective_Units"]
])

# Check if defective units exceed ordered quantity
excessive_defects = df_c[
    df_c["Defective_Units"] > df_c["Quantity"]
]

print("\nOrders where Defective_Units > Quantity:")
print(len(excessive_defects))

print(excessive_defects[
    ["PO_ID", "Quantity", "Defective_Units"]
])'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Create a flag: 1 = Defective_Units is missing, 0 = not missing
df_c["Defective_Units_Missing"] = (
    df_c["Defective_Units"].isna().astype(int)
)

# Count missing defective-unit values by Compliance
defect_missing_by_compliance = df_c.groupby(
    "Compliance"
)["Defective_Units_Missing"].sum()

print("Missing Defective_Units by Compliance:")
print(defect_missing_by_compliance)

# Also calculate the percentage missing within each compliance group
defect_missing_rate_by_compliance = df_c.groupby(
    "Compliance"
)["Defective_Units_Missing"].mean() * 100

print("\nPercentage of Defective_Units missing by Compliance:")
print(defect_missing_rate_by_compliance)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Create missingness indicator
df_c["Defective_Units_Missing"] = (
    df_c["Defective_Units"].isna().astype(int)
)

# Calculate missing count and missing percentage by Order Status
defect_missing_by_status = df_c.groupby(
    "Order_Status"
)["Defective_Units_Missing"].agg(
    ["sum", "count"]
)

defect_missing_by_status["missing_percentage"] = (
    defect_missing_by_status["sum"]
    / defect_missing_by_status["count"]
    * 100
)

print("Defective_Units missingness by Order Status:")
print(defect_missing_by_status)'''

'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")

# Create missingness indicator
df_c["Defective_Units_Missing"] = (df_c["Defective_Units"].isna().astype(int))

duplicate_combinations = df_c[
    df_c.duplicated(
        subset=["Supplier", "Item_Category", "Order_Date"],
        keep=False
    )
].sort_values(
    ["Supplier", "Item_Category", "Order_Date"]
)

print("Duplicate Supplier + Category + Order_Date combinations:")
print(duplicate_combinations)

print(
    "\nNumber of duplicate combinations:",
    len(duplicate_combinations)
)'''


'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv("data/raw/Procurement KPI Analysis Dataset.csv")
categorical_columns = [
    "Supplier",
    "Item_Category",
    "Order_Status",
    "Compliance"
]

for col in categorical_columns:
    print(f"\n{col}:")
    print(df_c[col].value_counts(dropna=False))


    import pandas as pd


# ============================================================
# LOAD DATASET D
# ============================================================

df_d = pd.read_csv(
    "data/raw/online_retail_II.csv"
)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("Dataset D shape:")
print(df_d.shape)


print("\nColumns:")
print(df_d.columns.tolist())


print("\nData types:")
print(df_d.dtypes)


print("\nFirst 5 rows:")
print(df_d.head())'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D2 — MISSING VALUE ANALYSIS
# ============================================================

print("=" * 60)
print("DATASET D — MISSING VALUE ANALYSIS")
print("=" * 60)


# Missing values by column
missing_count = df_d.isnull().sum()

print("\nMissing values by column:")
print(missing_count)


# Missing percentage by column
missing_percentage = (
    df_d.isnull().sum() / len(df_d) * 100
).round(2)

print("\nMissing value percentage:")
print(missing_percentage)


# Total rows containing at least one NULL
rows_with_missing = df_d.isnull().any(axis=1).sum()

print("\nTotal rows with at least one missing value:")
print(rows_with_missing)


# Percentage of rows containing at least one NULL
rows_with_missing_percentage = (
    rows_with_missing / len(df_d) * 100
)

print("\nPercentage of rows with at least one missing value:")
print(round(rows_with_missing_percentage, 2))'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D3 — DUPLICATE ANALYSIS
# ============================================================

print("=" * 60)
print("DATASET D — DUPLICATE ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Exact duplicate rows
# ------------------------------------------------------------

duplicate_rows = df_d.duplicated().sum()

print("\nNumber of exact duplicate rows:")
print(duplicate_rows)


print("\nPercentage of exact duplicate rows:")
print(
    round(
        duplicate_rows / len(df_d) * 100,
        2
    )
)


# ------------------------------------------------------------
# Display duplicate rows
# ------------------------------------------------------------

if duplicate_rows > 0:

    print("\nSample duplicate rows:")

    print(
        df_d[
            df_d.duplicated(keep=False)
        ]
        .sort_values(
            by=[
                "Invoice",
                "StockCode"
            ]
        )
        .head(20)
    )

else:

    print("\nNo exact duplicate rows found.")'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D4 — INVOICE DATE VALIDATION
# ============================================================

print("=" * 60)
print("DATASET D — INVOICE DATE VALIDATION")
print("=" * 60)


# Convert InvoiceDate to datetime
df_d["InvoiceDate_Parsed"] = pd.to_datetime(
    df_d["InvoiceDate"],
    errors="coerce"
)


# ------------------------------------------------------------
# Invalid / unparseable dates
# ------------------------------------------------------------

invalid_dates = df_d["InvoiceDate_Parsed"].isna().sum()

print("\nInvalid / unparseable InvoiceDate values:")
print(invalid_dates)


# ------------------------------------------------------------
# Missing dates
# ------------------------------------------------------------

missing_dates = df_d["InvoiceDate"].isna().sum()

print("\nMissing InvoiceDate values:")
print(missing_dates)


# ------------------------------------------------------------
# Date range
# ------------------------------------------------------------

print("\nInvoiceDate range:")

print(
    "Start:",
    df_d["InvoiceDate_Parsed"].min()
)

print(
    "End:",
    df_d["InvoiceDate_Parsed"].max()
)


# ------------------------------------------------------------
# Future dates
# ------------------------------------------------------------

today = pd.Timestamp.today()

future_dates = (
    df_d["InvoiceDate_Parsed"] > today
).sum()

print("\nFuture InvoiceDate values:")
print(future_dates)


# ------------------------------------------------------------
# Sample dates
# ------------------------------------------------------------

print("\nSample parsed dates:")

print(
    df_d[
        [
            "Invoice",
            "InvoiceDate",
            "InvoiceDate_Parsed"
        ]
    ].head(10)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D5 — QUANTITY & PRICE VALIDATION
# ============================================================

print("=" * 60)
print("DATASET D — QUANTITY & PRICE VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# QUANTITY
# ------------------------------------------------------------

print("\nQuantity statistics:")
print(df_d["Quantity"].describe())


print("\nZero Quantity:")
print(
    (df_d["Quantity"] == 0).sum()
)


print("\nNegative Quantity:")
print(
    (df_d["Quantity"] < 0).sum()
)


# ------------------------------------------------------------
# PRICE
# ------------------------------------------------------------

print("\nPrice statistics:")
print(df_d["Price"].describe())


print("\nZero Price:")
print(
    (df_d["Price"] == 0).sum()
)


print("\nNegative Price:")
print(
    (df_d["Price"] < 0).sum()
)


# ------------------------------------------------------------
# EXTREME VALUES
# ------------------------------------------------------------

print("\nMaximum Quantity:")
print(df_d["Quantity"].max())


print("\nMinimum Quantity:")
print(df_d["Quantity"].min())


print("\nMaximum Price:")
print(df_d["Price"].max())


print("\nMinimum Price:")
print(df_d["Price"].min())'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D6 — NEGATIVE QUANTITY INVESTIGATION
# ============================================================

print("=" * 60)
print("DATASET D — NEGATIVE QUANTITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# Create negative quantity flag
# ------------------------------------------------------------

df_d["Negative_Quantity"] = (
    df_d["Quantity"] < 0
)


# ------------------------------------------------------------
# Count negative quantity records
# ------------------------------------------------------------

print("\nNegative quantity records:")
print(
    df_d["Negative_Quantity"].sum()
)


# ------------------------------------------------------------
# Percentage
# ------------------------------------------------------------

print("\nPercentage of records with negative quantity:")

print(
    round(
        df_d["Negative_Quantity"].mean() * 100,
        2
    )
)


# ------------------------------------------------------------
# Inspect negative quantity transactions
# ------------------------------------------------------------

negative_quantity_df = df_d[
    df_d["Negative_Quantity"]
]

print("\nSample negative quantity transactions:")

print(
    negative_quantity_df[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(20)
)


# ------------------------------------------------------------
# Most common descriptions among negative quantities
# ------------------------------------------------------------

print(
    "\nTop descriptions among negative quantity records:"
)

print(
    negative_quantity_df["Description"]
    .value_counts()
    .head(10)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D7 — INVOICE PREFIX ANALYSIS
# ============================================================

print("=" * 60)
print("DATASET D — INVOICE PREFIX ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Convert Invoice to string
# ------------------------------------------------------------

df_d["Invoice"] = df_d["Invoice"].astype(str)


# ------------------------------------------------------------
# Identify invoices beginning with C
# ------------------------------------------------------------

df_d["Is_C_Invoice"] = df_d["Invoice"].str.startswith("C")


print("\nNumber of C-prefixed transaction rows:")
print(
    df_d["Is_C_Invoice"].sum()
)


print("\nPercentage of transaction rows with C-prefixed Invoice:")
print(
    round(
        df_d["Is_C_Invoice"].mean() * 100,
        2
    )
)


# ------------------------------------------------------------
# Quantity sign by invoice prefix
# ------------------------------------------------------------

print("\nQuantity sign by Invoice prefix:")

print(
    pd.crosstab(
        df_d["Is_C_Invoice"],
        df_d["Quantity"] < 0,
        margins=True
    )
)


# ------------------------------------------------------------
# Negative quantities among C invoices
# ------------------------------------------------------------

c_invoice_rows = df_d[
    df_d["Is_C_Invoice"]
]

negative_c_invoices = c_invoice_rows[
    c_invoice_rows["Quantity"] < 0
]


print("\nNegative quantity rows with C-prefixed Invoice:")
print(
    len(negative_c_invoices)
)


print("\nPercentage of negative quantity rows having C-prefixed Invoice:")

negative_quantity_rows = df_d[
    df_d["Quantity"] < 0
]

print(
    round(
        len(negative_c_invoices)
        / len(negative_quantity_rows)
        * 100,
        2
    )
)


# ------------------------------------------------------------
# Sample C invoices
# ------------------------------------------------------------

print("\nSample C-prefixed transactions:")

print(
    c_invoice_rows[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(20)
)'''


'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D8 — NON-C NEGATIVE QUANTITY INVESTIGATION
# ============================================================

print("=" * 60)
print("DATASET D — NON-C NEGATIVE QUANTITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# Filter negative quantities without C-prefixed invoice
# ------------------------------------------------------------

non_c_negative = df_d[
    (df_d["Quantity"] < 0) &
    (~df_d["Invoice"].astype(str).str.startswith("C"))
].copy()


# ------------------------------------------------------------
# Count
# ------------------------------------------------------------

print("\nNegative quantity rows without C-prefixed Invoice:")
print(len(non_c_negative))


print("\nPercentage of all negative quantity rows:")
print(
    round(
        len(non_c_negative)
        / (df_d["Quantity"] < 0).sum()
        * 100,
        2
    )
)


# ------------------------------------------------------------
# Sample records
# ------------------------------------------------------------

print("\nSample records:")

print(
    non_c_negative[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(30)
)


# ------------------------------------------------------------
# Most common descriptions
# ------------------------------------------------------------

print("\nTop descriptions:")

print(
    non_c_negative["Description"]
    .value_counts()
    .head(20)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D9 — NEGATIVE PRICE INVESTIGATION
# ============================================================

print("=" * 60)
print("DATASET D — NEGATIVE PRICE INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# Find negative-price records
# ------------------------------------------------------------

negative_price_df = df_d[
    df_d["Price"] < 0
].copy()


# ------------------------------------------------------------
# Count
# ------------------------------------------------------------

print("\nNumber of negative-price records:")
print(len(negative_price_df))


# ------------------------------------------------------------
# Display ALL negative-price records
# ------------------------------------------------------------

print("\nAll negative-price records:")

print(
    negative_price_df[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].to_string(index=False)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D10 — ZERO PRICE INVESTIGATION
# ============================================================

print("=" * 60)
print("DATASET D — ZERO PRICE INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# Filter zero-price transactions
# ------------------------------------------------------------

zero_price_df = df_d[
    df_d["Price"] == 0
].copy()


# ------------------------------------------------------------
# Count
# ------------------------------------------------------------

print("\nNumber of zero-price records:")
print(len(zero_price_df))


print("\nPercentage of all records:")
print(
    round(
        len(zero_price_df) / len(df_d) * 100,
        2
    )
)


# ------------------------------------------------------------
# Quantity statistics
# ------------------------------------------------------------

print("\nQuantity statistics for zero-price records:")

print(
    zero_price_df["Quantity"].describe()
)


# ------------------------------------------------------------
# Customer ID availability
# ------------------------------------------------------------

print("\nMissing Customer ID among zero-price records:")

print(
    zero_price_df["Customer ID"].isna().sum()
)


# ------------------------------------------------------------
# Top descriptions
# ------------------------------------------------------------

print("\nTop descriptions among zero-price records:")

print(
    zero_price_df["Description"]
    .value_counts()
    .head(20)
)


# ------------------------------------------------------------
# Sample records
# ------------------------------------------------------------

print("\nSample zero-price records:")

print(
    zero_price_df[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(30)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D11 — CUSTOMER ID MISSINGNESS ANALYSIS
# ============================================================

print("=" * 60)
print("DATASET D — CUSTOMER ID MISSINGNESS ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Create transaction classification flags
# ------------------------------------------------------------

df_d["Is_C_Invoice"] = (
    df_d["Invoice"]
    .astype(str)
    .str.startswith("C")
)

df_d["Negative_Quantity"] = (
    df_d["Quantity"] < 0
)

df_d["Zero_Price"] = (
    df_d["Price"] == 0
)

df_d["Negative_Price"] = (
    df_d["Price"] < 0
)

df_d["Missing_Customer_ID"] = (
    df_d["Customer ID"].isna()
)


# ------------------------------------------------------------
# Overall Customer ID missingness
# ------------------------------------------------------------

print("\nOverall Customer ID missing:")
print(
    df_d["Missing_Customer_ID"].sum()
)

print("\nOverall Customer ID missing percentage:")
print(
    round(
        df_d["Missing_Customer_ID"].mean() * 100,
        2
    )
)


# ------------------------------------------------------------
# Missing Customer ID by C invoice
# ------------------------------------------------------------

print("\nMissing Customer ID by C-prefixed Invoice:")

print(
    pd.crosstab(
        df_d["Is_C_Invoice"],
        df_d["Missing_Customer_ID"],
        margins=True
    )
)


# ------------------------------------------------------------
# Missing Customer ID by negative quantity
# ------------------------------------------------------------

print("\nMissing Customer ID by Negative Quantity:")

print(
    pd.crosstab(
        df_d["Negative_Quantity"],
        df_d["Missing_Customer_ID"],
        margins=True
    )
)


# ------------------------------------------------------------
# Missing Customer ID by zero price
# ------------------------------------------------------------

print("\nMissing Customer ID by Zero Price:")

print(
    pd.crosstab(
        df_d["Zero_Price"],
        df_d["Missing_Customer_ID"],
        margins=True
    )
)


# ------------------------------------------------------------
# Missing Customer ID by negative price
# ------------------------------------------------------------

print("\nMissing Customer ID by Negative Price:")

print(
    pd.crosstab(
        df_d["Negative_Price"],
        df_d["Missing_Customer_ID"],
        margins=True
    )
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D12 — STOCKCODE / DESCRIPTION CONSISTENCY
# ============================================================

print("=" * 60)
print("DATASET D — STOCKCODE / DESCRIPTION CONSISTENCY")
print("=" * 60)


# ------------------------------------------------------------
# Unique counts
# ------------------------------------------------------------

print("\nNumber of unique StockCodes:")
print(df_d["StockCode"].nunique())


print("\nNumber of unique Descriptions:")
print(df_d["Description"].nunique())


# ------------------------------------------------------------
# StockCodes with multiple descriptions
# ------------------------------------------------------------

stockcode_description_counts = (
    df_d.groupby("StockCode")["Description"]
    .nunique(dropna=True)
    .sort_values(ascending=False)
)


multiple_descriptions = (
    stockcode_description_counts[
        stockcode_description_counts > 1
    ]
)


print("\nStockCodes mapped to multiple descriptions:")
print(len(multiple_descriptions))


print("\nTop StockCodes with multiple descriptions:")
print(
    multiple_descriptions.head(20)
)


# ------------------------------------------------------------
# Show examples
# ------------------------------------------------------------

if len(multiple_descriptions) > 0:

    example_stockcodes = (
        multiple_descriptions
        .head(10)
        .index
    )

    print("\nExamples:")

    print(
        df_d[
            df_d["StockCode"].isin(example_stockcodes)
        ][
            [
                "StockCode",
                "Description"
            ]
        ]
        .drop_duplicates()
        .sort_values("StockCode")
        .head(50)
    )


# ------------------------------------------------------------
# Descriptions mapped to multiple StockCodes
# ------------------------------------------------------------

description_stockcode_counts = (
    df_d.groupby("Description")["StockCode"]
    .nunique()
    .sort_values(ascending=False)
)


multiple_stockcodes = (
    description_stockcode_counts[
        description_stockcode_counts > 1
    ]
)


print("\nDescriptions mapped to multiple StockCodes:")
print(len(multiple_stockcodes))


print("\nTop descriptions mapped to multiple StockCodes:")
print(
    multiple_stockcodes.head(20)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D13 — SPECIAL / NON-PRODUCT STOCKCODES
# ============================================================

print("=" * 60)
print("DATASET D — SPECIAL / NON-PRODUCT STOCKCODES")
print("=" * 60)


# ------------------------------------------------------------
# Descriptions that indicate special/operational transactions
# ------------------------------------------------------------

special_keywords = (
    "manual",
    "postage",
    "discount",
    "adjust",
    "adjustment",
    "bad debt",
    "damag",
    "check",
    "missing",
    "found",
    "smashed",
    "crushed",
    "thrown away",
    "unsaleable",
    "wrong",
    "faulty",
    "error",
    "amendment",
    "amazon",
    "dotcom"
)


# ------------------------------------------------------------
# Find records matching special descriptions
# ------------------------------------------------------------

description_text = (
    df_d["Description"]
    .fillna("")
    .astype(str)
    .str.lower()
)


special_mask = description_text.str.contains(
    "|".join(special_keywords),
    regex=True,
    na=False
)


special_df = df_d[special_mask].copy()


# ------------------------------------------------------------
# Count
# ------------------------------------------------------------

print("\nNumber of records matching special/operational keywords:")
print(len(special_df))


print("\nPercentage of Dataset D:")
print(
    round(
        len(special_df) / len(df_d) * 100,
        2
    )
)


# ------------------------------------------------------------
# Unique StockCodes
# ------------------------------------------------------------

print("\nNumber of StockCodes associated with these records:")
print(
    special_df["StockCode"].nunique()
)


# ------------------------------------------------------------
# Most common StockCodes
# ------------------------------------------------------------

print("\nTop StockCodes:")
print(
    special_df["StockCode"]
    .value_counts()
    .head(30)
)


# ------------------------------------------------------------
# Most common descriptions
# ------------------------------------------------------------

print("\nTop descriptions:")
print(
    special_df["Description"]
    .value_counts()
    .head(30)
)'''
'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D14 — INVOICE-LEVEL ANALYSIS
# ============================================================

print("=" * 60)
print("DATASET D — INVOICE-LEVEL ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Unique invoices
# ------------------------------------------------------------

unique_invoices = df_d["Invoice"].nunique()

print("\nNumber of unique invoices:")
print(unique_invoices)


# ------------------------------------------------------------
# Average line items per invoice
# ------------------------------------------------------------

invoice_line_counts = (
    df_d.groupby("Invoice")
    .size()
)


print("\nAverage rows per invoice:")
print(
    round(invoice_line_counts.mean(), 2)
)


print("\nMedian rows per invoice:")
print(
    invoice_line_counts.median()
)


print("\nMaximum rows in a single invoice:")
print(
    invoice_line_counts.max()
)


# ------------------------------------------------------------
# Invoice-level quantity signs
# ------------------------------------------------------------

invoice_signs = (
    df_d.groupby("Invoice")["Quantity"]
    .agg(
        has_positive=lambda x: (x > 0).any(),
        has_negative=lambda x: (x < 0).any()
    )
)


# Invoices containing both positive and negative quantities
mixed_invoices = invoice_signs[
    (invoice_signs["has_positive"]) &
    (invoice_signs["has_negative"])
]


print("\nInvoices containing both positive and negative quantities:")
print(len(mixed_invoices))


# ------------------------------------------------------------
# C-prefixed invoices
# ------------------------------------------------------------

c_invoice_count = (
    df_d["Invoice"]
    .astype(str)
    .str.startswith("C")
    .sum()
)


print("\nC-prefixed transaction rows:")
print(c_invoice_count)


print("\nUnique C-prefixed invoices:")

print(
    df_d[
        df_d["Invoice"]
        .astype(str)
        .str.startswith("C")
    ]["Invoice"].nunique()
)


# ------------------------------------------------------------
# Sample invoice line counts
# ------------------------------------------------------------

print("\nTop 20 invoices by number of line items:")

print(
    invoice_line_counts
    .sort_values(ascending=False)
    .head(20)
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D15 — INVOICE PREFIX vs QUANTITY VALIDATION
# ============================================================

print("=" * 60)
print("DATASET D — INVOICE PREFIX vs QUANTITY VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# Create invoice prefix flag
# ------------------------------------------------------------

df_d["Is_C_Invoice"] = (
    df_d["Invoice"]
    .astype(str)
    .str.startswith("C")
)


# ------------------------------------------------------------
# Quantity sign
# ------------------------------------------------------------

df_d["Quantity_Sign"] = pd.cut(
    df_d["Quantity"],
    bins=[-float("inf"), 0, float("inf")],
    labels=["Negative", "Positive"]
)


# ------------------------------------------------------------
# Cross-tabulation
# ------------------------------------------------------------

print("\nQuantity sign by Invoice prefix:")

print(
    pd.crosstab(
        df_d["Is_C_Invoice"],
        df_d["Quantity_Sign"],
        margins=True
    )
)


# ------------------------------------------------------------
# C-prefixed invoices with positive quantity
# ------------------------------------------------------------

c_positive = df_d[
    (df_d["Is_C_Invoice"]) &
    (df_d["Quantity"] > 0)
]

print("\nC-prefixed rows with positive quantity:")
print(len(c_positive))


if len(c_positive) > 0:
    print("\nC-prefixed positive-quantity records:")
    print(c_positive.head(20))


# ------------------------------------------------------------
# Non-C invoices with negative quantity
# ------------------------------------------------------------

non_c_negative = df_d[
    (~df_d["Is_C_Invoice"]) &
    (df_d["Quantity"] < 0)
]

print("\nNon-C rows with negative quantity:")
print(len(non_c_negative))


# ------------------------------------------------------------
# Percentage
# ------------------------------------------------------------

print(
    "\nPercentage of C-prefixed rows with negative quantity:"
)

print(
    round(
        (
            (
                df_d["Is_C_Invoice"] &
                (df_d["Quantity"] < 0)
            ).sum()
            /
            df_d["Is_C_Invoice"].sum()
        ) * 100,
        2
    )
)


print(
    "\nPercentage of non-C rows with negative quantity:"
)

print(
    round(
        (
            (
                (~df_d["Is_C_Invoice"]) &
                (df_d["Quantity"] < 0)
            ).sum()
            /
            (~df_d["Is_C_Invoice"]).sum()
        ) * 100,
        2
    )
)'''

'''import pandas as pd


# ============================================================
# DATASET D — LOAD DATA
# ============================================================

csv_path = "data/raw/online_retail_II.csv"

df_d = pd.read_csv(csv_path)


# ============================================================
# D16 — TRANSACTION TYPE EXCEPTIONS
# ============================================================

print("=" * 60)
print("DATASET D — TRANSACTION TYPE EXCEPTIONS")
print("=" * 60)


# ------------------------------------------------------------
# C-prefixed positive quantity
# ------------------------------------------------------------

c_positive = df_d[
    df_d["Invoice"]
    .astype(str)
    .str.startswith("C")
    &
    (df_d["Quantity"] > 0)
].copy()


print("\nC-prefixed invoices with positive quantity:")
print(len(c_positive))


print("\nRecords:")

print(
    c_positive[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Non-C negative quantity
# ------------------------------------------------------------

non_c_negative = df_d[
    ~df_d["Invoice"]
    .astype(str)
    .str.startswith("C")
    &
    (df_d["Quantity"] < 0)
].copy()


print("\n\nNon-C invoices with negative quantity:")
print(len(non_c_negative))


# ------------------------------------------------------------
# StockCode distribution
# ------------------------------------------------------------

print("\nTop StockCodes among non-C negative quantities:")

print(
    non_c_negative["StockCode"]
    .value_counts()
    .head(30)
)


# ------------------------------------------------------------
# Description distribution
# ------------------------------------------------------------

print("\nTop descriptions among non-C negative quantities:")

print(
    non_c_negative["Description"]
    .value_counts()
    .head(30)
)


# ------------------------------------------------------------
# Customer ID availability
# ------------------------------------------------------------

print("\nCustomer ID missingness:")

print(
    non_c_negative["Customer ID"]
    .isna()
    .value_counts()
)'''

