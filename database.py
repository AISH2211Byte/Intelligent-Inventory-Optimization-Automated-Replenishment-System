#dataset a
'''import pandas as pd

file_path = "data/raw/sales_data.csv"

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

print("Data types:")
print(df.dtypes)
print("\nFINAL DATE TYPE:")
print(df["Date"].dtype)

import psycopg

# PostgreSQL connection details
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="inventory_db",
    user="postgres",
    password="270571"
)

print("Connected to PostgreSQL successfully!")


# Create the historical inventory table

create_table_query = """
CREATE TABLE IF NOT EXISTS historical_inventory (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    category VARCHAR(50),
    region VARCHAR(50),
    inventory_level INT NOT NULL,
    units_sold INT NOT NULL,
    units_ordered INT,
    price NUMERIC(10,2),
    discount NUMERIC(5,2),
    weather_condition VARCHAR(30),
    promotion INT,
    competitor_pricing NUMERIC(10,2),
    seasonality VARCHAR(20),
    epidemic INT,
    demand INT
);
"""
import psycopg
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="inventory_db",
    user="postgres",
    password="270571"
)

with conn.cursor() as cur:
    cur.execute(create_table_query)

conn.commit()

print("historical_inventory table created successfully!")


# -----------------------------
# 3. Load data
# -----------------------------

insert_query = """
INSERT INTO historical_inventory (
    date,
    store_id,
    product_id,
    category,
    region,
    inventory_level,
    units_sold,
    units_ordered,
    price,
    discount,
    weather_condition,
    promotion,
    competitor_pricing,
    seasonality,
    epidemic,
    demand
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

with conn.cursor() as cur:
    for row in df.itertuples(index=False):
        cur.execute(
            insert_query,
            (
                row.Date,
                row[1],   # Store ID
                row[2],   # Product ID
                row[3],   # Category
                row[4],   # Region
                row[5],   # Inventory Level
                row[6],   # Units Sold
                row[7],   # Units Ordered
                row[8],   # Price
                row[9],   # Discount
                row[10],  # Weather Condition
                row[11],  # Promotion
                row[12],  # Competitor Pricing
                row[13],  # Seasonality
                row[14],  # Epidemic
                row[15]   # Demand
            )
        )

conn.commit()

print("Dataset A loaded successfully!")

conn.close()'''

#dataset b 
'''import pandas as pd
df_b = pd.read_csv("data/raw/supply_chain_dataset1.csv")

df_b["Date"] = pd.to_datetime(
    df_b["Date"],
    format="%d-%m-%Y"
)
import psycopg
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="inventory_db",
    user="postgres",
    password="270571"
)
with conn.cursor() as cur:

    cur.execute("""
        CREATE TABLE IF NOT EXISTS supply_chain_history (
            date DATE,
            sku_id VARCHAR(20),
            warehouse_id VARCHAR(20),
            supplier_id VARCHAR(20),
            region VARCHAR(20),
            units_sold INT,
            inventory_level INT,
            supplier_lead_time_days INT,
            reorder_point INT,
            order_quantity INT,
            unit_cost DECIMAL(10,2),
            unit_price DECIMAL(10,2),
            promotion_flag INT,
            stockout_flag INT,
            demand_forecast DECIMAL(10,2),

            PRIMARY KEY (date, sku_id, warehouse_id)
        );
    """)

conn.commit()

print("supply_chain_history table created successfully!")'''


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

'''import pandas as pd
# pandas → used to read and work with the CSV dataset

import psycopg
# psycopg → used to connect Python to PostgreSQL


# ============================================================
# 2. LOAD DATASET B
# ============================================================

file_path = "data/raw/supply_chain_dataset1.csv"
# file_path → location of our Dataset B CSV file

df_b = pd.read_csv(file_path)
# df_b → Pandas DataFrame containing Dataset B
# pd.read_csv() → reads the CSV file into the DataFrame


# ============================================================
# 3. CONVERT DATE
# ============================================================

df_b["Date"] = pd.to_datetime(
    df_b["Date"],
    format="%d-%m-%Y"
)
# Converts Date from string format into a real datetime value.


# ============================================================
# 4. CONNECT TO POSTGRESQL
# ============================================================

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="inventory_db",
    user="postgres",
    password="270571"
)
# conn → connection between Python and our PostgreSQL database


# ============================================================
# 5. PREPARE DATA FOR INSERTION
# ============================================================

records = df_b.where(
    pd.notnull(df_b),
    None
).values.tolist()

# records → Python list containing all rows from df_b
#
# pd.notnull() → checks for missing values
# None → converts missing values into SQL NULL
# .values → gets the actual values from the DataFrame
# .tolist() → converts them into a Python list
#
# Dataset B contains 91,250 rows,
# so records contains 91,250 rows.


# ============================================================
# 6. INSERT DATA INTO POSTGRESQL
# ============================================================

with conn.cursor() as cur:
    # cur → cursor used to send SQL commands to PostgreSQL

    cur.executemany("""
        INSERT INTO supply_chain_history (
            date,
            sku_id,
            warehouse_id,
            supplier_id,
            region,
            units_sold,
            inventory_level,
            supplier_lead_time_days,
            reorder_point,
            order_quantity,
            unit_cost,
            unit_price,
            promotion_flag,
            stockout_flag,
            demand_forecast
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        );
    """, records)

# executemany() → executes the INSERT statement for
# every row in records.
#
# %s → placeholders for the values in each row.


# ============================================================
# 7. SAVE THE INSERTION
# ============================================================

conn.commit()
# commit() → permanently saves the inserted rows
# in PostgreSQL.


# ============================================================
# 8. CONFIRM INSERTION
# ============================================================

print("Dataset B inserted successfully!")
print("Rows inserted:", len(records))


# ============================================================
# 9. CLOSE DATABASE CONNECTION
# ============================================================

conn.close()
# close() → closes the connection to PostgreSQL
'''


#dataset c
import pandas as pd
import psycopg


# ============================================================
# POSTGRESQL CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="inventory_db",
        user="postgres",
        password="270571",
        port="5432"
    )


# ============================================================
# CREATE PROCUREMENT ORDERS TABLE
# ============================================================

def create_procurement_orders_table():

    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS procurement_orders (
        po_id VARCHAR(20) PRIMARY KEY,
        supplier VARCHAR(50),
        order_date DATE,
        delivery_date DATE,
        item_category VARCHAR(50),
        order_status VARCHAR(30),
        quantity INT,
        unit_price NUMERIC(10,2),
        negotiated_price NUMERIC(10,2),
        defective_units INT,
        compliance VARCHAR(10)
    );
    """

    '''cursor.execute(create_table_query)

    conn.commit()

    cursor.close()
    conn.close()

    print("procurement_orders table created successfully.")


# ============================================================
# LOAD DATASET C
# ============================================================

def load_procurement_orders_data(csv_path):

    # --------------------------------------------------------
    # Read Procurement KPI Analysis Dataset
    # --------------------------------------------------------

    df = pd.read_csv(csv_path)

    print(f"Dataset C loaded: {len(df)} rows")


    # --------------------------------------------------------
    # Convert date columns
    #
    # CSV:
    # Order_Date / Delivery_Date → strings
    #
    # Python:
    # strings → datetime
    #
    # PostgreSQL:
    # datetime → DATE
    # --------------------------------------------------------

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df["Delivery_Date"] = pd.to_datetime(
        df["Delivery_Date"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Convert pandas missing values to Python None
    #
    # NaN / NaT → None
    # PostgreSQL → NULL
    # --------------------------------------------------------

    df = df.where(pd.notnull(df), None)


    # --------------------------------------------------------
    # Connect to PostgreSQL
    # --------------------------------------------------------

    conn = get_connection()
    cursor = conn.cursor()


    # --------------------------------------------------------
    # INSERT QUERY
    # --------------------------------------------------------

    insert_query = """
    INSERT INTO procurement_orders (
        po_id,
        supplier,
        order_date,
        delivery_date,
        item_category,
        order_status,
        quantity,
        unit_price,
        negotiated_price,
        defective_units,
        compliance
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (po_id) DO NOTHING;
    """


    # --------------------------------------------------------
    # Insert Dataset C rows
    # --------------------------------------------------------

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                row["PO_ID"],
                row["Supplier"],
                row["Order_Date"],
                row["Delivery_Date"],
                row["Item_Category"],
                row["Order_Status"],
                row["Quantity"],
                row["Unit_Price"],
                row["Negotiated_Price"],
                row["Defective_Units"],
                row["Compliance"]
            )
        )


    conn.commit()

    print(f"{len(df)} Dataset C rows processed.")

    cursor.close()
    conn.close()


# ============================================================
# VERIFY PROCUREMENT ORDERS TABLE
# ============================================================

def verify_procurement_orders_table():

    conn = get_connection()
    cursor = conn.cursor()


    # --------------------------------------------------------
    # Count rows
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM procurement_orders;
    """)

    count = cursor.fetchone()[0]

    print(f"Rows currently in procurement_orders: {count}")


    # --------------------------------------------------------
    # Preview first 5 rows
    # --------------------------------------------------------

    cursor.execute("""
        SELECT *
        FROM procurement_orders
        ORDER BY po_id
        LIMIT 5;
    """)

    rows = cursor.fetchall()

    print("\nFirst 5 rows:")

    for row in rows:
        print(row)


    cursor.close()
    conn.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Dataset C path
    # --------------------------------------------------------

    csv_path = "data/raw/Procurement KPI Analysis Dataset.csv"


    # --------------------------------------------------------
    # 1. Create PostgreSQL table
    # --------------------------------------------------------

    create_procurement_orders_table()


    # --------------------------------------------------------
    # 2. Load Dataset C
    # --------------------------------------------------------

    load_procurement_orders_data(csv_path)


    # --------------------------------------------------------
    # 3. Verify table
    # --------------------------------------------------------

    verify_procurement_orders_table()

'''
'''import pandas as pd

# Load Dataset C
df_c = pd.read_csv(
    "data/raw/Procurement KPI Analysis Dataset.csv"
)

# Convert date columns
df_c["Order_Date"] = pd.to_datetime(
    df_c["Order_Date"],
    errors="coerce"
)

df_c["Delivery_Date"] = pd.to_datetime(
    df_c["Delivery_Date"],
    errors="coerce"
)

# Check maximum values
print("\nMaximum values:")

print("Quantity max:", df_c["Quantity"].max())
print("Unit_Price max:", df_c["Unit_Price"].max())
print("Negotiated_Price max:", df_c["Negotiated_Price"].max())
print("Defective_Units max:", df_c["Defective_Units"].max())'''

'''import psycopg


# PostgreSQL connection
conn = psycopg.connect(
    host="localhost",
    dbname="inventory_db",
    user="postgres",
    password="270571",
    port=5432
)

cursor = conn.cursor()


# Check number of rows
cursor.execute("""
    SELECT COUNT(*)
    FROM procurement_orders;
""")

count = cursor.fetchone()[0]

print("Rows in procurement_orders:", count)


# Close connection
cursor.close()
conn.close()'''

import psycopg


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="inventory_db",
        user="postgres",
        password="270571",
        port=5432
    )


# ============================================================
# DATASET D — BULK LOAD USING POSTGRESQL COPY
# ============================================================

def load_retail_transactions(csv_path):

    print("Starting Dataset D bulk load...")

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            with open(
                csv_path,
                "r",
                encoding="utf-8-sig"
            ) as file:

                with cursor.copy(
                    """
                    COPY retail_transactions (
                        invoice,
                        stock_code,
                        description,
                        quantity,
                        invoice_date,
                        price,
                        customer_id,
                        country
                    )
                    FROM STDIN
                    WITH (
                        FORMAT CSV,
                        HEADER TRUE,
                        DELIMITER ',',
                        QUOTE '"'
                    )
                    """
                ) as copy:

                    while True:

                        data = file.read(1024 * 1024)

                        if not data:
                            break

                        copy.write(data)

        conn.commit()

        print("Dataset D inserted successfully.")


    except Exception as e:

        conn.rollback()

        print("Dataset D loading failed.")
        print("Error:", e)

        raise


    finally:

        conn.close()


# ============================================================
# RUN DATASET D LOAD
# ============================================================

if __name__ == "__main__":

    load_retail_transactions(
        "data/raw/online_retail_II.csv"
    )

