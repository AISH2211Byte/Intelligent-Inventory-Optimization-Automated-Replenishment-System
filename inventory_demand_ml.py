import pandas as pd
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
# 2. FEATURES FROM DATASET A
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
    store_id,
    product_id,
    date,
    {", ".join(feature_cols)},
    {target_col}
FROM inventory_ml_features
WHERE target_next_day IS NOT NULL
ORDER BY store_id, product_id, date;
"""

df = pd.read_sql(query, engine)

df["date"] = pd.to_datetime(df["date"])

print("Loaded rows:", len(df))

# ============================================================
# 3. CLEAN ML DATASET
# ============================================================

ml_df = df[
    ["store_id", "product_id", "date"] +
    feature_cols +
    [target_col]
].copy()

ml_df = ml_df.dropna(
    subset=feature_cols + [target_col]
)

print("Clean ML rows:", len(ml_df))

# ============================================================
# 4. TIME-BASED TRAIN / VALIDATION SPLIT
# ============================================================

train = ml_df[
    ml_df["date"] <= "2023-06-30"
].copy()

validation = ml_df[
    (ml_df["date"] >= "2023-07-01") &
    (ml_df["date"] <= "2024-01-30")
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
# 6. LIGHTGBM
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
# 8. PREDICTIONS
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

model_path = "lightgbm_inventory_demand_model.pkl"

joblib.dump(model, model_path)

print("\n========== MODEL SAVED ==========")
print("Path:", os.path.abspath(model_path))

print("\nBest iteration:", model.best_iteration_)