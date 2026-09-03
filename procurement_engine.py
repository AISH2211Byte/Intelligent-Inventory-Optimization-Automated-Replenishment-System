import psycopg
import pandas as pd


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


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(**DB_CONFIG)


# ============================================================
# GET SUPPLIER PROFILE
# ============================================================

def get_supplier_profile(store_id, product_id):

    query = """
        SELECT
            psm.store_id,
            psm.product_id,
            sp.supplier_id,
            sp.avg_lead_time_days,
            sp.lead_time_std_days,
            sp.delivery_rate_pct,
            sp.defect_rate_pct,
            sp.compliance_rate_pct,
            sp.reliability_score,
            sp.source_procurement_profile
        FROM product_supplier_map psm
        JOIN supplier_profiles sp
            ON psm.supplier_id = sp.supplier_id
        WHERE psm.store_id = %s
          AND psm.product_id = %s;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn,
            params=(store_id, product_id)
        )

    if df.empty:
        raise ValueError(
            f"No supplier profile found for "
            f"{store_id} / {product_id}"
        )

    return df.iloc[0]


# ============================================================
# SUPPLIER EVALUATION
# ============================================================

def evaluate_supplier(supplier):

    reliability = float(
        supplier["reliability_score"]
    )

    delivery_rate = float(
        supplier["delivery_rate_pct"]
    )

    defect_rate = float(
        supplier["defect_rate_pct"]
    )

    compliance_rate = float(
        supplier["compliance_rate_pct"]
    )

    lead_time = float(
        supplier["avg_lead_time_days"]
    )

    # --------------------------------------------------------
    # Reliability classification
    # --------------------------------------------------------

    if reliability >= 85:

        supplier_rating = "EXCELLENT"

    elif reliability >= 75:

        supplier_rating = "GOOD"

    elif reliability >= 65:

        supplier_rating = "MODERATE"

    else:

        supplier_rating = "POOR"

    # --------------------------------------------------------
    # Procurement recommendation
    # --------------------------------------------------------

    if (
        reliability >= 85
        and defect_rate <= 5
        and compliance_rate >= 90
    ):

        recommendation = "PREFERRED"

    elif (
        reliability >= 75
        and defect_rate <= 10
    ):

        recommendation = "ACCEPTABLE"

    else:

        recommendation = "RISKY"

    return {
        "supplier_rating": supplier_rating,
        "recommendation": recommendation,
        "reliability_score": reliability,
        "delivery_rate_pct": delivery_rate,
        "defect_rate_pct": defect_rate,
        "compliance_rate_pct": compliance_rate,
        "lead_time_days": lead_time
    }


# ============================================================
# PROCUREMENT DECISION
# ============================================================

def make_procurement_decision(
    store_id,
    product_id,
    order_quantity
):

    # --------------------------------------------------------
    # 1. Get supplier
    # --------------------------------------------------------

    supplier = get_supplier_profile(
        store_id,
        product_id
    )

    # --------------------------------------------------------
    # 2. Evaluate supplier
    # --------------------------------------------------------

    evaluation = evaluate_supplier(
        supplier
    )

    # --------------------------------------------------------
    # 3. Procurement decision
    # --------------------------------------------------------

    supplier_id = supplier["supplier_id"]

    if evaluation["recommendation"] == "RISKY":

        procurement_decision = (
            "ORDER_WITH_CAUTION"
        )

    else:

        procurement_decision = "PROCEED"

    # --------------------------------------------------------
    # 4. Return complete result
    # --------------------------------------------------------

    return {

        "store_id": store_id,

        "product_id": product_id,

        "supplier_id": supplier_id,

        "order_quantity": int(
            order_quantity
        ),

        "procurement_decision":
            procurement_decision,

        "supplier_rating":
            evaluation["supplier_rating"],

        "recommendation":
            evaluation["recommendation"],

        "lead_time_days":
            round(
                evaluation["lead_time_days"],
                2
            ),

        "delivery_rate_pct":
            round(
                evaluation["delivery_rate_pct"],
                2
            ),

        "defect_rate_pct":
            round(
                evaluation["defect_rate_pct"],
                2
            ),

        "compliance_rate_pct":
            round(
                evaluation["compliance_rate_pct"],
                2
            ),

        "reliability_score":
            round(
                evaluation["reliability_score"],
                2
            ),

        "supplier_source":
            supplier[
                "source_procurement_profile"
            ]
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = make_procurement_decision(
        store_id="S001",
        product_id="P0001",
        order_quantity=616
    )

    print(
        "\n========== PROCUREMENT DECISION =========="
    )

    for key, value in result.items():

        print(
            f"{key:25}: {value}"
        )