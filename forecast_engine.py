import os
import joblib
import pandas as pd
import psycopg


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "dbname": "inventory_db",
    "user": "postgres",
    "password": "270571",
    "port": 5432
}

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "lightgbm_inventory_demand_model.pkl"
)

# ============================================================
# MODEL FEATURES
# Must match training order exactly
# ============================================================

FEATURE_COLUMNS = [
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
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(**DB_CONFIG)


# ============================================================
# GET LATEST FEATURES
# ============================================================

def get_latest_features(store_id, product_id):

    query = """
        SELECT
            date,
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
            is_weekend
        FROM inventory_ml_features
        WHERE store_id = %s
          AND product_id = %s
        ORDER BY date DESC
        LIMIT 1;
    """

    conn = get_connection()

    try:
        df = pd.read_sql_query(
            query,
            conn,
            params=(store_id, product_id)
        )
    finally:
        conn.close()

    if df.empty:
        raise ValueError(
            f"No ML features found for {store_id} / {product_id}"
        )

    return df


# ============================================================
# FORECAST DEMAND
# ============================================================

def get_demand_forecast(store_id, product_id):

    df = get_latest_features(store_id, product_id)

    feature_row = df[FEATURE_COLUMNS]

    # Check for missing features
    if feature_row.isnull().any().any():
        missing = feature_row.columns[
            feature_row.isnull().any()
        ].tolist()

        raise ValueError(
            f"Missing features for {store_id}/{product_id}: {missing}"
        )

    predicted_demand = model.predict(feature_row)[0]

    # Demand cannot be negative
    predicted_demand = max(0, predicted_demand)

    return {
        "store_id": store_id,
        "product_id": product_id,
        "feature_date": df.iloc[0]["date"],
        "predicted_demand": round(float(predicted_demand), 2)
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = get_demand_forecast(
        "S001",
        "P0001"
    )

    print("\n========== DEMAND FORECAST ==========")
    print(f"Store           : {result['store_id']}")
    print(f"Product         : {result['product_id']}")
    print(f"Feature date    : {result['feature_date']}")
    print(f"Predicted demand: {result['predicted_demand']}")