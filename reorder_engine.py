import psycopg
import joblib
import pandas as pd
import numpy as np


# ============================================================
# CONFIG
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "inventory_db",
    "user": "postgres",
    "password": "270571"
}

MODEL_PATH = r"D:\Data Analytics\inventory_project\lightgbm_inventory_demand_model.pkl"

# 90% service level
# Z = 1.28
Z_SCORE = 1.28

# Replenishment policy:
# If we reorder, bring stock above the ROP by
# approximately one additional review period of demand.
REVIEW_PERIOD_DAYS = 7


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(**DB_CONFIG)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# GET CURRENT INVENTORY
# ============================================================

def get_current_inventory(store_id, product_id):

    query = """
        SELECT
            store_id,
            product_id,
            current_stock
        FROM current_inventory
        WHERE store_id = %s
          AND product_id = %s;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn,
            params=(store_id, product_id)
        )

    if df.empty:
        raise ValueError(
            f"No inventory found for {store_id} / {product_id}"
        )

    return int(df.iloc[0]["current_stock"])


# ============================================================
# GET BEST SUPPLIER
# ============================================================

def get_supplier(store_id, product_id):

    query = """
        SELECT
            psm.supplier_id,
            sp.avg_lead_time_days,
            sp.lead_time_std_days,
            sp.delivery_rate_pct,
            sp.defect_rate_pct,
            sp.compliance_rate_pct,
            sp.reliability_score
        FROM product_supplier_map psm
        JOIN supplier_profiles sp
            ON psm.supplier_id = sp.supplier_id
        WHERE psm.store_id = %s
          AND psm.product_id = %s
        ORDER BY
            sp.avg_lead_time_days
            * (1 - sp.reliability_score / 100.0) ASC
        LIMIT 1;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn,
            params=(store_id, product_id)
        )

    if df.empty:
        raise ValueError(
            f"No supplier mapping found for {store_id} / {product_id}"
        )

    supplier = df.iloc[0].copy()

    # Lower score = better balance between
    # speed and reliability.
    supplier["supplier_score"] = (
        float(supplier["avg_lead_time_days"])
        * (
            1
            - float(supplier["reliability_score"]) / 100
        )
    )

    return supplier


# ============================================================
# GET LATEST ML FEATURES
# ============================================================

def get_latest_features(store_id, product_id):

    query = """
        SELECT *
        FROM inventory_ml_features
        WHERE store_id = %s
          AND product_id = %s
        ORDER BY date DESC
        LIMIT 1;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn,
            params=(store_id, product_id)
        )

    if df.empty:
        raise ValueError(
            f"No ML features found for {store_id} / {product_id}"
        )

    return df


# ============================================================
# FORECAST DEMAND
# ============================================================

def get_demand_forecast(store_id, product_id):

    df = get_latest_features(
        store_id,
        product_id
    )

    feature_columns = [
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

    X = df[feature_columns].copy()

    # Handle missing values.
    X = X.fillna(0)

    prediction = model.predict(X)[0]

    # Demand cannot be negative.
    prediction = max(
        0,
        float(prediction)
    )

    return prediction, df.iloc[0]


# ============================================================
# SUPPLIER RATING
# ============================================================

def evaluate_supplier(reliability_score):

    reliability_score = float(reliability_score)

    if reliability_score >= 85:
        return "EXCELLENT"

    elif reliability_score >= 75:
        return "GOOD"

    elif reliability_score >= 65:
        return "FAIR"

    else:
        return "POOR"


# ============================================================
# REORDER DECISION
# ============================================================

def calculate_reorder_decision(
    store_id,
    product_id
):

    # --------------------------------------------------------
    # 1. CURRENT INVENTORY
    # --------------------------------------------------------

    current_stock = get_current_inventory(
        store_id,
        product_id
    )

    # --------------------------------------------------------
    # 2. DEMAND FORECAST
    # --------------------------------------------------------

    forecast, feature_row = get_demand_forecast(
        store_id,
        product_id
    )

    # --------------------------------------------------------
    # 3. SUPPLIER SELECTION
    # --------------------------------------------------------

    supplier = get_supplier(
        store_id,
        product_id
    )

    supplier_id = supplier["supplier_id"]

    lead_time = float(
        supplier["avg_lead_time_days"]
    )

    lead_time_std = float(
        supplier["lead_time_std_days"]
    )

    # --------------------------------------------------------
    # 4. DEMAND VARIABILITY
    # --------------------------------------------------------

    # Prefer 30-day variability because it gives
    # a more stable estimate.

    demand_std = feature_row["rolling_30d_std"]

    if pd.isna(demand_std):

        demand_std = feature_row["rolling_14d_std"]

    if pd.isna(demand_std):

        demand_std = feature_row["rolling_7d_std"]

    if pd.isna(demand_std):

        demand_std = 0

    demand_std = float(demand_std)

    # Prevent negative/invalid variability.
    demand_std = max(
        0,
        demand_std
    )

    # --------------------------------------------------------
    # 5. SAFETY STOCK
    # --------------------------------------------------------

    # Accounts for BOTH:
    #
    # A. Demand uncertainty
    # B. Lead-time uncertainty
    #
    # SS = Z × sqrt(
    #          L × demand_std²
    #          +
    #          forecast² × lead_time_std²
    #      )

    safety_stock = (
        Z_SCORE
        * np.sqrt(
            (
                lead_time
                * demand_std ** 2
            )
            +
            (
                forecast ** 2
                * lead_time_std ** 2
            )
        )
    )

    # --------------------------------------------------------
    # 6. LEAD-TIME DEMAND
    # --------------------------------------------------------

    lead_time_demand = (
        forecast
        * lead_time
    )

    # --------------------------------------------------------
    # 7. REORDER POINT
    # --------------------------------------------------------

    reorder_point = (
        lead_time_demand
        + safety_stock
    )

    # --------------------------------------------------------
    # 8. ORDER-UP-TO LEVEL
    # --------------------------------------------------------

    # Instead of ordering only up to the ROP,
    # maintain an additional review-period demand buffer.

    review_period_demand = (
        forecast
        * REVIEW_PERIOD_DAYS
    )

    target_stock = (
        reorder_point
        + review_period_demand
    )

    # --------------------------------------------------------
    # 9. DECISION
    # --------------------------------------------------------

    if current_stock <= reorder_point:

        decision = "ORDER"

        order_quantity = max(
            0,
            int(
                np.ceil(
                    target_stock
                    - current_stock
                )
            )
        )

    else:

        decision = "NO_ORDER"

        order_quantity = 0

    # --------------------------------------------------------
    # 10. SUPPLIER RATING
    # --------------------------------------------------------

    reliability_score = float(
        supplier["reliability_score"]
    )

    supplier_rating = evaluate_supplier(
        reliability_score
    )

    # --------------------------------------------------------
    # 11. RETURN COMPLETE DECISION
    # --------------------------------------------------------

    return {

        "store_id":
            store_id,

        "product_id":
            product_id,

        "supplier_id":
            supplier_id,

        "current_stock":
            current_stock,

        "forecast_demand":
            round(
                forecast,
                2
            ),

        "lead_time_days":
            round(
                lead_time,
                2
            ),

        "lead_time_std_days":
            round(
                lead_time_std,
                2
            ),

        "demand_std":
            round(
                demand_std,
                2
            ),

        "safety_stock":
            round(
                safety_stock,
                2
            ),

        "lead_time_demand":
            round(
                lead_time_demand,
                2
            ),

        "reorder_point":
            round(
                reorder_point,
                2
            ),

        "review_period_days":
            REVIEW_PERIOD_DAYS,

        "review_period_demand":
            round(
                review_period_demand,
                2
            ),

        "target_stock":
            round(
                target_stock,
                2
            ),

        "order_quantity":
            order_quantity,

        "decision":
            decision,

        "delivery_rate_pct":
            round(
                float(
                    supplier["delivery_rate_pct"]
                ),
                2
            ),

        "defect_rate_pct":
            round(
                float(
                    supplier["defect_rate_pct"]
                ),
                2
            ),

        "compliance_rate_pct":
            round(
                float(
                    supplier["compliance_rate_pct"]
                ),
                2
            ),

        "reliability_score":
            round(
                reliability_score,
                2
            ),

        "supplier_rating":
            supplier_rating,

        "supplier_score":
            round(
                float(
                    supplier["supplier_score"]
                ),
                4
            )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = calculate_reorder_decision(
        store_id="S001",
        product_id="P0001"
    )

    print(
        "\n========== REORDER DECISION =========="
    )

    for key, value in result.items():

        print(
            f"{key:25}: {value}"
        )