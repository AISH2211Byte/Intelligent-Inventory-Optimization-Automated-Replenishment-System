import psycopg
from datetime import datetime, timedelta


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
# CREATE PURCHASE ORDER
# ============================================================

def create_purchase_order(
    store_id,
    product_id,
    supplier_id,
    quantity,
    lead_time_days
):
    """
    Creates a purchase order after procurement approval.

    The PO remains PENDING until its expected arrival time.
    """

    if quantity <= 0:
        raise ValueError("Order quantity must be greater than zero.")

    if lead_time_days < 0:
        raise ValueError("Lead time cannot be negative.")

    created_at = datetime.now()

    expected_arrival = (
        created_at
        + timedelta(days=lead_time_days)
    )

    query = """
        INSERT INTO purchase_orders (
            store_id,
            product_id,
            supplier_id,
            quantity,
            created_at,
            expected_arrival,
            status
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, 'PENDING'
        )
        RETURNING po_id;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (
                    store_id,
                    product_id,
                    supplier_id,
                    int(quantity),
                    created_at,
                    expected_arrival
                )
            )

            po_id = cur.fetchone()[0]

        conn.commit()

    return {
        "po_id": po_id,
        "store_id": store_id,
        "product_id": product_id,
        "supplier_id": supplier_id,
        "quantity": int(quantity),
        "created_at": created_at,
        "expected_arrival": expected_arrival,
        "status": "PENDING"
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = create_purchase_order(
        store_id="S001",
        product_id="P0008",
        supplier_id="SUP_9",
        quantity=1832,
        lead_time_days=8.19
    )

    print("\n============================================================")
    print("             PURCHASE ORDER CREATED")
    print("============================================================")

    for key, value in result.items():
        print(f"{key:20}: {value}")