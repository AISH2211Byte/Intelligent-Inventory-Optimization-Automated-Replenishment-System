import psycopg
from datetime import datetime


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
# FULFILL PENDING PURCHASE ORDERS
# ============================================================

def fulfill_pending_orders():

    query = """
        SELECT
            po_id,
            store_id,
            product_id,
            supplier_id,
            quantity,
            expected_arrival
        FROM purchase_orders
        WHERE status = 'PENDING'
          AND expected_arrival <= CURRENT_TIMESTAMP
        ORDER BY expected_arrival;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(query)

            pending_orders = cur.fetchall()

            if not pending_orders:
                return []

            fulfilled = []

            for row in pending_orders:

                (
                    po_id,
                    store_id,
                    product_id,
                    supplier_id,
                    quantity,
                    expected_arrival
                ) = row

                # ------------------------------------------------
                # Add received stock to current inventory
                # ------------------------------------------------

                inventory_query = """
                    UPDATE current_inventory
                    SET
                        current_stock = current_stock + %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE store_id = %s
                      AND product_id = %s;
                """

                cur.execute(
                    inventory_query,
                    (
                        quantity,
                        store_id,
                        product_id
                    )
                )

                if cur.rowcount == 0:
                    raise ValueError(
                        f"No inventory record found for "
                        f"{store_id} / {product_id}"
                    )

                # ------------------------------------------------
                # Mark PO as ARRIVED
                # ------------------------------------------------

                update_po_query = """
                    UPDATE purchase_orders
                    SET status = 'ARRIVED'
                    WHERE po_id = %s;
                """

                cur.execute(
                    update_po_query,
                    (po_id,)
                )

                fulfilled.append({
                    "po_id": po_id,
                    "store_id": store_id,
                    "product_id": product_id,
                    "supplier_id": supplier_id,
                    "quantity": quantity,
                    "expected_arrival": expected_arrival
                })

            conn.commit()

    return fulfilled


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n============================================================")
    print("              INVENTORY FULFILLMENT ENGINE")
    print("============================================================")

    print("Checking for arrived purchase orders...")

    results = fulfill_pending_orders()

    if not results:

        print("\nNo purchase orders are currently ready for fulfillment.")

    else:

        print(
            f"\nFulfilled {len(results)} purchase order(s):"
        )

        for po in results:

            print("\n----------------------------------------")

            print(
                f"PO ID          : {po['po_id']}"
            )

            print(
                f"Store          : {po['store_id']}"
            )

            print(
                f"Product        : {po['product_id']}"
            )

            print(
                f"Supplier       : {po['supplier_id']}"
            )

            print(
                f"Quantity       : {po['quantity']}"
            )

            print(
                f"Expected arrival: "
                f"{po['expected_arrival']}"
            )

            print(
                "Status         : ARRIVED"
            )