import psycopg
import select
import os
from dotenv import load_dotenv

from reorder_engine import calculate_reorder_decision
from procurement_engine import make_procurement_decision
from alert_engine import send_reorder_alert


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


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
# GET ORDER
# ============================================================

def get_order(conn, order_id):

    query = """
        SELECT
            order_id,
            store_id,
            product_id,
            quantity,
            event_time,
            source,
            event_type
        FROM orders
        WHERE order_id = %s;
    """

    with conn.cursor() as cur:

        cur.execute(
            query,
            (order_id,)
        )

        row = cur.fetchone()

    if row is None:
        return None

    return {
        "order_id": row[0],
        "store_id": row[1],
        "product_id": row[2],
        "quantity": row[3],
        "event_time": row[4],
        "source": row[5],
        "event_type": row[6]
    }


# ============================================================
# PROCESS ORDER EVENT
# ============================================================

def process_order(order_id):

    conn = get_connection()

    try:

        order = get_order(
            conn,
            order_id
        )

        if order is None:

            print(
                f"Order {order_id} not found."
            )

            return


        store_id = order["store_id"]
        product_id = order["product_id"]
        quantity = order["quantity"]
        event_type = order["event_type"]


        print()
        print(
            "=" * 60
        )

        print(
            f"PROCESSING ORDER EVENT: {order_id}"
        )

        print(
            "=" * 60
        )

        print(
            f"Store       : {store_id}"
        )

        print(
            f"Product     : {product_id}"
        )

        print(
            f"Event type  : {event_type}"
        )

        print(
            f"Quantity    : {quantity}"
        )


        # ====================================================
        # 1. CHECK CURRENT INVENTORY
        # ====================================================

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT current_stock
                FROM current_inventory
                WHERE store_id = %s
                  AND product_id = %s;
                """,
                (
                    store_id,
                    product_id
                )
            )

            row = cur.fetchone()


        if row is None:

            print(
                "ERROR: Inventory record not found."
            )

            return


        current_stock = int(
            row[0]
        )


        # ====================================================
        # 2. UPDATE INVENTORY
        # ====================================================

        if event_type == "SALE":

            actual_sold = min(
                quantity,
                current_stock
            )

            lost_sale = max(
                0,
                quantity - current_stock
            )

            new_stock = (
                current_stock
                - actual_sold
            )


        elif event_type == "RETURN":

            actual_sold = 0
            lost_sale = 0

            new_stock = (
                current_stock
                + quantity
            )


        else:

            print(
                f"Unknown event type: {event_type}"
            )

            return


        # ====================================================
        # 3. WRITE INVENTORY UPDATE
        # ====================================================

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE current_inventory
                SET
                    current_stock = %s,
                    last_updated = NOW()
                WHERE store_id = %s
                  AND product_id = %s;
                """,
                (
                    new_stock,
                    store_id,
                    product_id
                )
            )

        conn.commit()


        print(
            f"Current stock after event: {new_stock}"
        )


        if lost_sale > 0:

            print(
                f"⚠ Lost sale quantity: {lost_sale}"
            )


        # ====================================================
        # 4. RUN REORDER ENGINE
        # ====================================================

        print()
        print(
            "Running reorder engine..."
        )


        reorder_result = (
            calculate_reorder_decision(
                store_id=store_id,
                product_id=product_id
            )
        )


        print(
            f"Forecast demand : "
            f"{reorder_result['forecast_demand']:.2f}"
        )

        print(
            f"Reorder point   : "
            f"{reorder_result['reorder_point']:.2f}"
        )

        print(
            f"Decision        : "
            f"{reorder_result['decision']}"
        )


        # ====================================================
        # 5. NO REORDER REQUIRED
        # ====================================================

        if reorder_result["decision"] != "ORDER":

            print(
                "No reorder required."
            )

            return


        # ====================================================
        # 6. REORDER REQUIRED
        # ====================================================

        print()
        print(
            "Reorder required!"
        )

        order_quantity = int(
            reorder_result["order_quantity"]
        )

        print(
            f"Order quantity  : {order_quantity}"
        )


        # ====================================================
        # 7. RUN PROCUREMENT ENGINE
        # ====================================================

        print()
        print(
            "Running procurement engine..."
        )


        procurement_result = (
            make_procurement_decision(
                store_id=store_id,
                product_id=product_id,
                order_quantity=order_quantity
            )
        )


        print(
            f"Supplier        : "
            f"{procurement_result['supplier_id']}"
        )

        print(
            f"Supplier rating : "
            f"{procurement_result['supplier_rating']}"
        )

        print(
            f"Recommendation  : "
            f"{procurement_result['recommendation']}"
        )

        print(
            f"Procurement     : "
            f"{procurement_result['procurement_decision']}"
        )


        # ====================================================
        # 8. PROCUREMENT APPROVED
        # ====================================================

        if (
            procurement_result[
                "procurement_decision"
            ]
            in [
                "PROCEED",
                "ORDER_WITH_CAUTION"
            ]
        ):

            print()
            print(
                "✓ Procurement approved."
            )


            # =================================================
            # 9. SEND EMAIL ALERT AUTOMATICALLY
            # =================================================

            print()
            print(
                "Sending automatic reorder alert..."
            )


            # Combine both engine results
            alert_result = {

                **reorder_result,

                **procurement_result,

                "order_id":
                    order_id,

                "event_type":
                    event_type,

                "current_stock":
                    new_stock
            }


            try:

                send_reorder_alert(
                    alert_result
                )

                print(
                    "✓ Reorder email sent."
                )

            except Exception as email_error:

                print()
                print(
                    "⚠ EMAIL ALERT FAILED"
                )

                print(
                    f"Reason: {email_error}"
                )

                print(
                    "Inventory processing "
                    "continues."
                )


            print()
            print(
                "→ Next stage: "
                "create purchase order "
                "and schedule fulfillment."
            )


        else:

            print()
            print(
                "✗ Procurement rejected."
            )

    finally:

        conn.close()


# ============================================================
# LISTENER
# ============================================================

def main():

    print()
    print(
        "=" * 60
    )

    print(
        "              INVENTORY EVENT LISTENER"
    )

    print(
        "=" * 60
    )

    print(
        "Listening for new orders..."
    )

    print(
        "Channel: new_order"
    )

    print(
        "=" * 60
    )


    conn = get_connection()

    conn.autocommit = True


    with conn.cursor() as cur:

        cur.execute(
            "LISTEN new_order;"
        )


    print()
    print(
        "✓ Listener connected."
    )

    print(
        "Waiting for replay events..."
    )


    try:

        for notification in conn.notifies():

            order_id = int(
                notification.payload
            )

            print()
            print(
                f"🔔 New order notification: {order_id}"
            )

            process_order(
                order_id
            )

    except KeyboardInterrupt:

        print()
        print(
            "Listener stopped."
        )

    finally:

        conn.close()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()