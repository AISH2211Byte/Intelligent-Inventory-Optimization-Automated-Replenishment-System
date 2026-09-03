'''import pandas as pd
from sqlalchemy import create_engine
# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)'''

# ==============================
# ML DATA QUALITY AUDIT
# ==============================


'''import pandas as pd
from sqlalchemy import create_engine
# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""
df = pd.read_sql(query, engine)


print("\n========== BASIC INFO ==========")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()
print(missing[missing > 0])


print("\n========== TARGET ==========")

print("Missing target:", df["target_next_day"].isnull().sum())
print("Available target:", df["target_next_day"].notnull().sum())

print("\nTarget statistics:")
print(df["target_next_day"].describe())


print("\n========== DUPLICATES ==========")

print(
    "Duplicate stock_code + demand_date:",
    df.duplicated(
        subset=["stock_code", "demand_date"]
    ).sum()
)


print("\n========== DATE ==========")

df["demand_date"] = pd.to_datetime(df["demand_date"])

print("Minimum date:", df["demand_date"].min())
print("Maximum date:", df["demand_date"].max())


print("\n========== NEGATIVE VALUES ==========")

print(
    "Negative daily quantity:",
    (df["daily_quantity"] < 0).sum()
)

print(
    "Negative target:",
    (df["target_next_day"] < 0).sum()
)'''

'''import pandas as pd
from sqlalchemy import create_engine
# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""
df = pd.read_sql(query, engine)


print("\n========== FEATURE AVAILABILITY ==========")

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
]

for col in feature_cols:
    print(
        f"{col:20s} "
        f"available = {df[col].notna().sum():,} | "
        f"missing = {df[col].isna().sum():,}"
    )


print("\n========== ZERO ROLLING DEMAND ==========")

print(
    "Rows with rolling_30d_avg = 0:",
    (df["rolling_30d_avg"] == 0).sum()
)

print(
    "Rows with rolling_30d_avg = 0 AND rolling_30d_std = 0:",
    (
        (df["rolling_30d_avg"] == 0) &
        (df["rolling_30d_std"] == 0)
    ).sum()
)

print(
    "Rows with rolling_30d_cv NULL:",
    df["rolling_30d_cv"].isna().sum()
)'''




'''import pandas as pd
from sqlalchemy import create_engine
# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""
df = pd.read_sql(query, engine)
# ==========================================
# CREATE ML-READY DATASET
# ==========================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

id_cols = [
    "stock_code",
    "demand_date"
]

ml_df = df[id_cols + feature_cols + [target_col]].copy()

print("\n========== ML DATASET ==========")

print("Original rows:", len(df))
print("ML rows before cleaning:", len(ml_df))

print("\nColumns:")
print(ml_df.columns.tolist())

ml_df = ml_df.dropna(subset=["target_next_day"])'''


'''import pandas as pd
from sqlalchemy import create_engine
# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""
df = pd.read_sql(query, engine)
# ==========================================
# CREATE ML-READY DATASET
# ==========================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

id_cols = [
    "stock_code",
    "demand_date"
]

ml_df = df[id_cols + feature_cols + [target_col]].copy()
ml_df = ml_df.dropna(subset=["target_next_day"])

print("Shape after removing missing targets:", ml_df.shape)
print(ml_df.shape)'''


'''import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

id_cols = [
    "stock_code",
    "demand_date"
]

ml_df = df[id_cols + feature_cols + [target_col]].copy()

# Remove rows where tomorrow's actual demand is unavailable
ml_df = ml_df.dropna(subset=["target_next_day"])

print("ML dataframe shape:", ml_df.shape)

print("\nMissing values in selected ML features:")
print(ml_df[feature_cols].isnull().sum())

print("\nRows with ANY missing selected feature:")
print(ml_df[feature_cols].isnull().any(axis=1).sum())

print("\nRows with NO missing selected features:")
print(ml_df[feature_cols].notnull().all(axis=1).sum())'''


'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# Load the ML feature table
query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

# Convert date
df["demand_date"] = pd.to_datetime(df["demand_date"])

# Same feature definition
feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

# Create ML dataframe
ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    ["target_next_day"]
].copy()

# Remove rows with unavailable target
ml_df = ml_df.dropna(subset=["target_next_day"])

# Find rows where lag_14 is missing
lag14_missing = ml_df[ml_df["lag_14"].isna()].copy()

print("Rows with missing lag_14:", len(lag14_missing))

print("\nFirst 10 rows with missing lag_14:")
print(
    lag14_missing[
        ["stock_code", "demand_date", "lag_1", "lag_7", "lag_14"]
    ].head(10)
)

print("\nNumber of unique products affected:")
print(lag14_missing["stock_code"].nunique())

print("\nEarliest date for affected rows:")
print(lag14_missing["demand_date"].min())

print("\nLatest date for affected rows:")
print(lag14_missing["demand_date"].max())'''


'''import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT
    stock_code,
    demand_date,
    daily_quantity,
    lag_1,
    lag_7,
    lag_14
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# Products with missing lag_14
missing_lag14 = df[df["lag_14"].isna()].copy()

# For every product, find the first date where lag_14 is NOT missing
first_valid_lag14 = (
    df[df["lag_14"].notna()]
    .groupby("stock_code")["demand_date"]
    .min()
    .reset_index(name="first_valid_lag14_date")
)

# Compare
missing_lag14 = missing_lag14.merge(
    first_valid_lag14,
    on="stock_code",
    how="left"
)

print("========== LAG_14 INVESTIGATION ==========")

print("\nTotal missing lag_14 rows:", len(missing_lag14))

print(
    "\nProducts whose lag_14 NEVER becomes available:"
)
print(
    missing_lag14[
        missing_lag14["first_valid_lag14_date"].isna()
    ]["stock_code"].nunique()
)

print(
    "\nMissing lag_14 rows occurring AFTER lag_14 became valid:"
)

late_missing = missing_lag14[
    missing_lag14["first_valid_lag14_date"].notna()
    &
    (
        missing_lag14["demand_date"]
        >= missing_lag14["first_valid_lag14_date"]
    )
]

print(len(late_missing))

print("\nFirst 20 late-missing examples:")
print(
    late_missing[
        [
            "stock_code",
            "demand_date",
            "first_valid_lag14_date",
            "lag_1",
            "lag_7",
            "lag_14"
        ]
    ].head(20)
)'''

'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

# Create the same ML feature set
feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    ["target_next_day"]
].copy()

# Remove rows with missing target
ml_df = ml_df.dropna(subset=["target_next_day"])

print("========== NULL FEATURE INVESTIGATION ==========")

for col in feature_cols:
    missing = ml_df[ml_df[col].isna()]

    if len(missing) > 0:
        print(f"\n{col}")
        print("Missing rows:", len(missing))
        print("Unique products:", missing["stock_code"].nunique())
        print("Earliest missing date:", missing["demand_date"].min())
        print("Latest missing date:", missing["demand_date"].max())'''


'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# Load feature table
query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

# Convert date
df["demand_date"] = pd.to_datetime(df["demand_date"])

# Model features
feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# Create ML dataframe
ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    [target_col]
].copy()

# Step 1: target must exist
ml_df = ml_df.dropna(subset=[target_col])

# Step 2: every model feature must exist
ml_df = ml_df.dropna(subset=feature_cols)

print("========== FINAL ML DATASET ==========")
print("Shape:", ml_df.shape)

print("\nRemaining missing values:")
print(ml_df[feature_cols + [target_col]].isna().sum().sum())

print("\nDate range:")
print("Start:", ml_df["demand_date"].min())
print("End:", ml_df["demand_date"].max())

print("\nUnique products:", ml_df["stock_code"].nunique())'''

'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# Load data
query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# Same model features
feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# Recreate clean ML dataset
ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    [target_col]
].copy()

ml_df = ml_df.dropna(subset=[target_col])
ml_df = ml_df.dropna(subset=feature_cols)

# Check how many observations we have by year
print("========== OBSERVATIONS BY YEAR ==========")
print(ml_df["demand_date"].dt.year.value_counts().sort_index())

print("\n========== OBSERVATIONS BY MONTH ==========")
print(
    ml_df.groupby(
        ml_df["demand_date"].dt.to_period("M")
    ).size().tail(15)
)

print("\n========== DATE RANGE ==========")
print("Start:", ml_df["demand_date"].min())
print("End:", ml_df["demand_date"].max())'''


'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# Load data
query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# Model features
feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# Build clean ML dataset
ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    [target_col]
].copy()

ml_df = ml_df.dropna(subset=[target_col])
ml_df = ml_df.dropna(subset=feature_cols)

# Proposed chronological split
train = ml_df[
    ml_df["demand_date"] <= "2010-12-31"
]

validation = ml_df[
    (ml_df["demand_date"] >= "2011-01-01") &
    (ml_df["demand_date"] <= "2011-09-30")
]

test = ml_df[
    (ml_df["demand_date"] >= "2011-10-01") &
    (ml_df["demand_date"] <= "2011-12-08")
]

print("========== SPLIT CHECK ==========")

for name, data in [
    ("TRAIN", train),
    ("VALIDATION", validation),
    ("TEST", test)
]:
    print(f"\n{name}")
    print("Rows:", len(data))
    print("Unique products:", data["stock_code"].nunique())
    print("Start:", data["demand_date"].min())
    print("End:", data["demand_date"].max())'''


'''import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# Load required columns
query = """
SELECT
    stock_code,
    demand_date,
    daily_quantity,
    target_next_day,
    lag_1,
    lag_7,
    lag_14
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# Check target relationship
df["next_date"] = (
    df.groupby("stock_code")["demand_date"]
      .shift(-1)
)

df["actual_next_demand"] = (
    df.groupby("stock_code")["daily_quantity"]
      .shift(-1)
)

# Compare target_next_day against actual next-day demand
comparison = df[
    df["target_next_day"].notna() &
    df["actual_next_demand"].notna()
].copy()

comparison["target_matches_actual"] = (
    comparison["target_next_day"] ==
    comparison["actual_next_demand"]
)

print("========== TARGET SANITY CHECK ==========")

print(
    "\nTarget matches actual next demand:",
    comparison["target_matches_actual"].sum()
)

print(
    "Target does NOT match:",
    (~comparison["target_matches_actual"]).sum()
)

print(
    "\nMatch percentage:",
    comparison["target_matches_actual"].mean() * 100
)

print("\nSample:")
print(
    comparison[
        [
            "stock_code",
            "demand_date",
            "daily_quantity",
            "next_date",
            "target_next_day",
            "actual_next_demand"
        ]
    ].head(10)
)'''

'''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. PostgreSQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD DATA
# ============================================================

query = """
SELECT *
FROM product_ml_features
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# ============================================================
# 3. DEFINE FEATURES
# ============================================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# ============================================================
# 4. CREATE CLEAN ML DATASET
# ============================================================

ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    [target_col]
].copy()

# Target must exist
ml_df = ml_df.dropna(subset=[target_col])

# All selected model features must exist
ml_df = ml_df.dropna(subset=feature_cols)

# ============================================================
# 5. TEST PERIOD
# ============================================================

test = ml_df[
    (ml_df["demand_date"] >= "2011-10-01") &
    (ml_df["demand_date"] <= "2011-12-08")
].copy()

# ============================================================
# 6. NAIVE BASELINE
# ============================================================
# Predict tomorrow's demand using today's demand.
#
# lag_1 = demand on the previous day

y_actual = test[target_col]
y_pred = test["lag_1"]

# ============================================================
# 7. EVALUATE
# ============================================================

mae = mean_absolute_error(y_actual, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_actual, y_pred)
)

r2 = r2_score(y_actual, y_pred)

print("========== NAIVE BASELINE ==========")
print("Prediction rule: Tomorrow's demand = Today's demand")

print("\nTest rows:", len(test))

print("\nMAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)'''


'''import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD ONLY REQUIRED COLUMNS
# ============================================================

query = """
SELECT
    stock_code,
    demand_date,
    lag_1,
    lag_7,
    lag_14,
    rolling_7d_avg,
    rolling_14d_avg,
    rolling_30d_avg,
    rolling_7d_std,
    rolling_14d_std,
    rolling_30d_std,
    demand_trend_7d,
    demand_trend_30d,
    day_of_week,
    day_of_month,
    month,
    week_of_year,
    is_weekend,
    target_next_day
FROM product_ml_features
WHERE target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# ============================================================
# 3. MODEL FEATURES
# ============================================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# ============================================================
# 4. REMOVE ROWS WITH MISSING MODEL FEATURES
# ============================================================

df = df.dropna(subset=feature_cols)

# ============================================================
# 5. CHRONOLOGICAL SPLIT
# ============================================================

train = df[
    df["demand_date"] <= "2010-12-31"
].copy()

validation = df[
    (df["demand_date"] >= "2011-01-01") &
    (df["demand_date"] <= "2011-09-30")
].copy()

# TEST IS NOT USED HERE
# It remains locked for final evaluation.

X_train = train[feature_cols]
y_train = train[target_col]

X_val = validation[feature_cols]
y_val = validation[target_col]

# ============================================================
# 6. TRAIN LIGHTGBM
# ============================================================

model = LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    max_depth=-1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

# ============================================================
# 7. VALIDATION PREDICTIONS
# ============================================================

y_val_pred = model.predict(X_val)

# ============================================================
# 8. VALIDATION METRICS
# ============================================================

mae = mean_absolute_error(y_val, y_val_pred)

rmse = np.sqrt(
    mean_squared_error(y_val, y_val_pred)
)

r2 = r2_score(y_val, y_val_pred)

print("========== LIGHTGBM VALIDATION ==========")

print("\nTraining rows:", len(train))
print("Validation rows:", len(validation))

print("\nMAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)'''


'''import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD VALIDATION DATA ONLY
# ============================================================

query = """
SELECT
    stock_code,
    demand_date,
    daily_quantity,
    target_next_day
FROM product_ml_features
WHERE demand_date >= '2011-01-01'
  AND demand_date <= '2011-09-30'
  AND target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

validation = pd.read_sql(query, engine)

validation["demand_date"] = pd.to_datetime(
    validation["demand_date"]
)

# ============================================================
# 3. REMOVE ROWS WHERE TODAY'S DEMAND IS UNAVAILABLE
# ============================================================

validation = validation.dropna(
    subset=["daily_quantity"]
)

# ============================================================
# 4. NAIVE BASELINE
# ============================================================
# Prediction:
# Tomorrow's demand = today's demand

y_actual = validation["target_next_day"]

y_pred = validation["daily_quantity"]

# ============================================================
# 5. EVALUATE
# ============================================================

mae = mean_absolute_error(
    y_actual,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_actual,
        y_pred
    )
)

r2 = r2_score(
    y_actual,
    y_pred
)

# ============================================================
# 6. RESULTS
# ============================================================

print("========== NAIVE BASELINE — VALIDATION ==========")

print("\nValidation rows:", len(validation))

print("\nPrediction rule:")
print("Tomorrow's demand = Today's demand")

print("\nMAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)'''

'''import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD VALIDATION DATA
# ============================================================

query = """
SELECT
    stock_code,
    demand_date,
    lag_1,
    lag_7,
    lag_14,
    rolling_7d_avg,
    rolling_14d_avg,
    rolling_30d_avg,
    rolling_7d_std,
    rolling_14d_std,
    rolling_30d_std,
    demand_trend_7d,
    demand_trend_30d,
    day_of_week,
    day_of_month,
    month,
    week_of_year,
    is_weekend,
    target_next_day,
    daily_quantity
FROM product_ml_features
WHERE demand_date >= '2011-01-01'
  AND demand_date <= '2011-09-30'
  AND target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

validation = pd.read_sql(query, engine)

validation["demand_date"] = pd.to_datetime(
    validation["demand_date"]
)

# ============================================================
# 3. SAME FEATURE COLUMNS USED BY LIGHTGBM
# ============================================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

# ============================================================
# 4. APPLY THE EXACT SAME CLEANING AS LIGHTGBM
# ============================================================

validation = validation.dropna(
    subset=feature_cols + ["target_next_day"]
)

# ============================================================
# 5. NAIVE BASELINE
# ============================================================
# Tomorrow's demand = today's demand

y_actual = validation["target_next_day"]

y_pred = validation["daily_quantity"]

# ============================================================
# 6. EVALUATE
# ============================================================

mae = mean_absolute_error(
    y_actual,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_actual,
        y_pred
    )
)

r2 = r2_score(
    y_actual,
    y_pred
)

# ============================================================
# 7. RESULTS
# ============================================================

print("========== FAIR NAIVE BASELINE — VALIDATION ==========")

print("\nValidation rows:", len(validation))

print("\nPrediction rule:")
print("Tomorrow's demand = Today's demand")

print("\nMAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)'''


'''import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD TRAIN + VALIDATION DATA
# ============================================================

query = """
SELECT
    stock_code,
    demand_date,
    lag_1,
    lag_7,
    lag_14,
    rolling_7d_avg,
    rolling_14d_avg,
    rolling_30d_avg,
    rolling_7d_std,
    rolling_14d_std,
    rolling_30d_std,
    demand_trend_7d,
    demand_trend_30d,
    day_of_week,
    day_of_month,
    month,
    week_of_year,
    is_weekend,
    target_next_day
FROM product_ml_features
WHERE target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

# ============================================================
# 3. FEATURES
# ============================================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

# ============================================================
# 4. SAME CLEANING USED BEFORE
# ============================================================

df = df.dropna(
    subset=feature_cols + [target_col]
)

# ============================================================
# 5. CHRONOLOGICAL TRAIN / VALIDATION SPLIT
# ============================================================

train = df[
    df["demand_date"] <= "2010-12-31"
].copy()

validation = df[
    (df["demand_date"] >= "2011-01-01") &
    (df["demand_date"] <= "2011-09-30")
].copy()

X_train = train[feature_cols]
y_train = train[target_col]

X_val = validation[feature_cols]
y_val = validation[target_col]

# ============================================================
# 6. TRAIN LIGHTGBM
# ============================================================

model = LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    max_depth=-1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    verbosity=-1
)

model.fit(
    X_train,
    y_train
)

# ============================================================
# 7. PREDICTIONS
# ============================================================

validation["predicted_demand"] = model.predict(X_val)

validation["prediction_error"] = (
    validation["target_next_day"]
    - validation["predicted_demand"]
)

validation["absolute_error"] = (
    validation["prediction_error"]
    .abs()
)

# ============================================================
# 8. OVERALL PERFORMANCE
# ============================================================

mae = mean_absolute_error(
    validation["target_next_day"],
    validation["predicted_demand"]
)

rmse = np.sqrt(
    mean_squared_error(
        validation["target_next_day"],
        validation["predicted_demand"]
    )
)

r2 = r2_score(
    validation["target_next_day"],
    validation["predicted_demand"]
)

print("========== OVERALL VALIDATION PERFORMANCE ==========")

print("\nRows:", len(validation))
print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)

# ============================================================
# 9. ZERO-DEMAND ANALYSIS
# ============================================================

zero_demand = validation[
    validation["target_next_day"] == 0
]

print("\n========== ZERO-DEMAND ANALYSIS ==========")

print("Zero-demand rows:", len(zero_demand))

if len(zero_demand) > 0:
    print(
        "MAE:",
        mean_absolute_error(
            zero_demand["target_next_day"],
            zero_demand["predicted_demand"]
        )
    )

# ============================================================
# 10. HIGH-DEMAND ANALYSIS
# ============================================================

high_demand = validation[
    validation["target_next_day"] >= 100
]

print("\n========== HIGH-DEMAND ANALYSIS ==========")

print("Demand >= 100 rows:", len(high_demand))

if len(high_demand) > 0:
    print(
        "MAE:",
        mean_absolute_error(
            high_demand["target_next_day"],
            high_demand["predicted_demand"]
        )
    )

    print(
        "RMSE:",
        np.sqrt(
            mean_squared_error(
                high_demand["target_next_day"],
                high_demand["predicted_demand"]
            )
        )
    )

# ============================================================
# 11. BIGGEST PREDICTION ERRORS
# ============================================================

print("\n========== TOP 10 LARGEST ERRORS ==========")

top_errors = validation.sort_values(
    "absolute_error",
    ascending=False
)[
    [
        "stock_code",
        "demand_date",
        "target_next_day",
        "predicted_demand",
        "absolute_error"
    ]
].head(10)

print(top_errors.to_string(index=False))

# ============================================================
# 12. SAMPLE PREDICTIONS
# ============================================================

print("\n========== SAMPLE PREDICTIONS ==========")

sample = validation[
    [
        "stock_code",
        "demand_date",
        "target_next_day",
        "predicted_demand",
        "prediction_error"
    ]
].head(10)

print(sample.to_string(index=False))'''



'''import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. PRODUCTS WITH BIGGEST MODEL ERRORS
# ============================================================

spike_cases = [
    ("22197", "2011-05-26"),
    ("22053", "2011-02-21"),
    ("84879", "2011-08-03"),
    ("18007", "2011-07-18"),
    ("21108", "2011-01-10"),
    ("21108", "2011-04-17"),
    ("85123A", "2011-01-10"),
    ("84568", "2011-07-30"),
    ("21977", "2011-05-22"),
    ("84077", "2011-02-02")
]

# ============================================================
# 3. LOOK AT PREVIOUS 30 DAYS
# ============================================================

for stock_code, spike_date in spike_cases:

    spike_date = pd.Timestamp(spike_date)

    query = """
    SELECT
        stock_code,
        demand_date,
        daily_quantity
    FROM product_daily_calendar
    WHERE stock_code = %(stock_code)s
      AND demand_date BETWEEN %(start_date)s AND %(end_date)s
    ORDER BY demand_date;
    """

    history = pd.read_sql(
        query,
        engine,
        params={
            "stock_code": stock_code,
            "start_date": spike_date - pd.Timedelta(days=30),
            "end_date": spike_date
        }
    )
    history["demand_date"] = pd.to_datetime(
        history["demand_date"]
    )

    spike_row = history[
        history["demand_date"] == spike_date
    ]


    print("\n" + "=" * 70)
    print("PRODUCT:", stock_code)
    print("SPIKE DATE:", spike_date.date())
    print("=" * 70)

    print(history.to_string(index=False))

    if len(spike_row) > 0:

        actual = spike_row["daily_quantity"].iloc[0]

        print("ACTUAL DEMAND ON DATE:", actual)

        previous = history[
            history["demand_date"] < spike_date
        ]

        print(
            "MAX DEMAND IN PREVIOUS 30 DAYS:",
            previous["daily_quantity"].max()
        )

        print(
            "AVERAGE DEMAND IN PREVIOUS 30 DAYS:",
            round(previous["daily_quantity"].mean(), 2)
        )

    else:

        print("No row found for this product/date.")

    print("\nLast 10 days before date:")

    print(
        history[
            history["demand_date"] < spike_date
        ].tail(10).to_string(index=False)
    )'''

'''import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD ONLY WHAT WE NEED
# ============================================================

query = """
SELECT
    stock_code,
    demand_date,
    target_next_day
FROM product_ml_features
WHERE target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

# ============================================================
# 3. CONVERT DATE
# ============================================================

df["demand_date"] = pd.to_datetime(df["demand_date"])

# ============================================================
# 4. DEMAND DISTRIBUTION
# ============================================================

df["demand_category"] = pd.cut(
    df["target_next_day"],
    bins=[-1, 0, 10, 50, 100, 500, 1000, float("inf")],
    labels=[
        "0",
        "1-10",
        "11-50",
        "51-100",
        "101-500",
        "501-1000",
        ">1000"
    ]
)

distribution = (
    df["demand_category"]
    .value_counts()
    .sort_index()
)

percentage = (
    distribution / len(df) * 100
).round(2)

result = pd.DataFrame({
    "Rows": distribution,
    "Percentage": percentage
})

# ============================================================
# 5. PRINT RESULTS
# ============================================================

print("=" * 60)
print("DEMAND DISTRIBUTION")
print("=" * 60)

print(result)

print("\nTotal observations:", len(df))

print("\nZero-demand observations:",
      (df["target_next_day"] == 0).sum())

print(
    "Zero-demand percentage:",
    round((df["target_next_day"] == 0).mean() * 100, 2),
    "%"
)

print("\nMaximum demand:",
      df["target_next_day"].max())

print("\nMedian demand:",
      df["target_next_day"].median())

print("\nMean demand:",
      round(df["target_next_day"].mean(), 2))'''


'''import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# ============================================================
# 1. POSTGRESQL CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg://postgres:270571@localhost:5432/inventory_db"
)

# ============================================================
# 2. LOAD ONLY REQUIRED COLUMNS
# ============================================================

feature_cols = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7d_avg",
    "rolling_14d_avg",
    "rolling_30d_avg",
    "rolling_7d_std",
    "rolling_14d_std",
    "rolling_30d_std",
    "demand_trend_7d",
    "demand_trend_30d",
    "day_of_week",
    "day_of_month",
    "month",
    "week_of_year",
    "is_weekend"
]

target_col = "target_next_day"

query = f"""
SELECT
    stock_code,
    demand_date,
    {", ".join(feature_cols)},
    {target_col}
FROM product_ml_features
WHERE target_next_day IS NOT NULL
ORDER BY stock_code, demand_date;
"""

df = pd.read_sql(query, engine)

df["demand_date"] = pd.to_datetime(df["demand_date"])

print("Loaded rows:", len(df))

# ============================================================
# 3. CLEAN ML DATASET
# ============================================================

ml_df = df[
    ["stock_code", "demand_date"] +
    feature_cols +
    [target_col]
].copy()

ml_df = ml_df.dropna(subset=feature_cols + [target_col])

print("Clean ML rows:", len(ml_df))

# ============================================================
# 4. TIME-BASED TRAIN / VALIDATION SPLIT
# ============================================================

train = ml_df[
    ml_df["demand_date"] <= "2010-12-31"
].copy()

validation = ml_df[
    (ml_df["demand_date"] >= "2011-01-01") &
    (ml_df["demand_date"] <= "2011-09-30")
].copy()

print("\n========== DATA SPLIT ==========")
print("Training rows:", len(train))
print("Validation rows:", len(validation))

# ============================================================
# 5. CREATE X AND y
# ============================================================

X_train = train[feature_cols]
y_train = train[target_col]

X_val = validation[feature_cols]
y_val = validation[target_col]

# ============================================================
# 6. LIGHTGBM MODEL
# ============================================================

model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    max_depth=-1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

# ============================================================
# 7. TRAIN
# ============================================================

print("\n========== TRAINING LIGHTGBM ==========")

model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[
        lgb.early_stopping(
            stopping_rounds=50,
            verbose=True
        )
    ]
)

# ============================================================
# 8. VALIDATION PREDICTIONS
# ============================================================

y_pred = model.predict(X_val)

# Demand cannot be negative
y_pred = np.maximum(y_pred, 0)

# ============================================================
# 9. EVALUATION
# ============================================================

mae = mean_absolute_error(y_val, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_val, y_pred)
)

r2 = r2_score(y_val, y_pred)

print("\n========== FINAL MODEL VALIDATION ==========")

print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)

# ============================================================
# 10. SAVE MODEL
# ============================================================

model_path = "lightgbm_demand_model.pkl"

joblib.dump(model, model_path)

print("\n========== MODEL SAVED ==========")
print("Path:", os.path.abspath(model_path))

print("\nBest iteration:", model.best_iteration_)'''

