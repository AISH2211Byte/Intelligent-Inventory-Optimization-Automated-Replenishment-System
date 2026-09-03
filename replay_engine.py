import time
import random
import numpy as np
import pandas as pd
import psycopg


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


# ------------------------------------------------------------
# Replay settings
# ------------------------------------------------------------

# Online Retail II observed return rate:
# 22,950 negative-quantity transactions / 1,067,371 total
RETURN_RATE = 22950 / 1067371

# Compress real-world invoice gaps for demonstration.
#
# Example:
# Real gap = 60 seconds
# compress_factor = 0.15
# Replay gap = 9 seconds
COMPRESS_FACTOR = 0.15

# Prevent extremely long silent periods.
GAP_CAP_PERCENTILE = 95

# Number of historical days used when sampling quantities.
RECENT_DAYS = 30

# Number of events to generate.
#
# Set to None for continuous replay.
MAX_EVENTS = 50


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg.connect(**DB_CONFIG)


# ============================================================
# 1. LOAD ONLINE RETAIL II TIMING
# ============================================================

def load_timing_pattern():

    print("\nLoading Online Retail II timing pattern...")

    query = """
        SELECT
            invoice,
            invoice_date
        FROM retail_transactions
        WHERE invoice IS NOT NULL
          AND invoice_date IS NOT NULL
        ORDER BY invoice_date;
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    if df.empty:
        raise ValueError(
            "No transaction data found in retail_transactions."
        )

    # --------------------------------------------------------
    # One event = one invoice
    # Multiple rows can belong to the same invoice.
    # --------------------------------------------------------

    times = (
        df.drop_duplicates("invoice")["invoice_date"]
        .sort_values()
    )

    # Calculate time between consecutive invoices
    gaps = (
        times.diff()
        .dropna()
        .dt.total_seconds()
    )

    # Remove invalid negative gaps
    gaps = gaps[gaps >= 0]

    if gaps.empty:
        raise ValueError(
            "Could not calculate invoice inter-arrival times."
        )

    # --------------------------------------------------------
    # Cap extreme gaps
    # --------------------------------------------------------

    cap = np.percentile(
        gaps,
        GAP_CAP_PERCENTILE
    )

    gaps = gaps.clip(upper=cap)

    # --------------------------------------------------------
    # Zero-second gaps are valid in the real dataset
    # because multiple invoices can have identical timestamps.
    #
    # We replace them with 1 second so the replay engine
    # doesn't repeatedly fire at exactly the same instant.
    # --------------------------------------------------------

    gaps = gaps.replace(0, 1)

    # --------------------------------------------------------
    # Compress for demo
    # --------------------------------------------------------

    compressed_gaps = (
        gaps * COMPRESS_FACTOR
    )

    # Never allow a zero sleep
    compressed_gaps = np.maximum(
        compressed_gaps,
        0.1
    )

    print(
        f"Timing pattern loaded: {len(compressed_gaps)} gaps"
    )

    print(
        f"95th percentile real gap: "
        f"{cap:.2f} seconds"
    )

    print(
        f"Median replay gap: "
        f"{np.median(compressed_gaps):.2f} seconds"
    )

    return compressed_gaps


# ============================================================
# 2. LOAD DATASET A DEMAND PROFILES
# ============================================================

def load_demand_profiles():

    print("\nLoading Dataset A demand profiles...")

    query = """
        SELECT
            store_id,
            product_id,
            date,
            demand
        FROM historical_inventory
        WHERE demand IS NOT NULL
          AND demand >= 0
        ORDER BY date;
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    if df.empty:
        raise ValueError(
            "No demand data found in historical_inventory."
        )

    df["date"] = pd.to_datetime(df["date"])

    # --------------------------------------------------------
    # Keep only recent history for each store-product.
    # --------------------------------------------------------

    profiles = {}

    for (store_id, product_id), group in df.groupby(
        ["store_id", "product_id"]
    ):

        group = group.sort_values("date")

        recent = group.tail(RECENT_DAYS)

        demand_values = (
            recent["demand"]
            .dropna()
            .astype(int)
            .values
        )

        if len(demand_values) == 0:
            continue

        # ----------------------------------------------------
        # Weight each store-product according to average
        # historical demand.
        #
        # Higher-demand products get selected more frequently.
        # ----------------------------------------------------

        avg_demand = float(
            recent["demand"].mean()
        )

        profiles[(store_id, product_id)] = {
            "quantities": demand_values,
            "avg_demand": max(avg_demand, 0)
        }

    if not profiles:
        raise ValueError(
            "Could not construct any demand profiles."
        )

    print(
        f"Loaded {len(profiles)} store-product profiles."
    )

    return profiles


# ============================================================
# 3. BUILD WEIGHTED STORE-PRODUCT SELECTION
# ============================================================

def build_selection_distribution(profiles):

    keys = list(profiles.keys())

    weights = np.array(
        [
            profiles[key]["avg_demand"]
            for key in keys
        ],
        dtype=float
    )

    # --------------------------------------------------------
    # If every product somehow has zero demand,
    # fall back to uniform selection.
    # --------------------------------------------------------

    if weights.sum() <= 0:

        probabilities = np.ones(
            len(keys)
        ) / len(keys)

    else:

        probabilities = (
            weights / weights.sum()
        )

    return keys, probabilities


# ============================================================
# 4. GENERATE EVENT QUANTITY
# ============================================================

def generate_quantity(quantity_history):

    # --------------------------------------------------------
    # Pick a historical daily demand value.
    # --------------------------------------------------------

    historical_demand = int(
        random.choice(quantity_history)
    )

    if historical_demand <= 0:
        return 1

    # --------------------------------------------------------
    # A historical daily demand is NOT one customer order.
    #
    # Split it into a smaller event quantity.
    # --------------------------------------------------------

    split_factor = random.randint(1, 5)

    quantity = max(
        1,
        int(round(
            historical_demand / split_factor
        ))
    )

    return quantity


# ============================================================
# 5. GENERATE SALE OR RETURN
# ============================================================

def generate_transaction(quantity):

    is_return = (
        random.random() < RETURN_RATE
    )

    if is_return:

        return -quantity, True

    return quantity, False


# ============================================================
# 6. INSERT ORDER EVENT
# ============================================================

def insert_order(
    conn,
    store_id,
    product_id,
    quantity
):

    query = """
        INSERT INTO orders (
            store_id,
            product_id,
            quantity,
            event_time,
            source
        )
        VALUES (
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP,
            'replay'
        )
        RETURNING order_id, event_time;
    """

    with conn.cursor() as cur:

        cur.execute(
            query,
            (
                store_id,
                product_id,
                quantity
            )
        )

        result = cur.fetchone()

    conn.commit()

    return result


# ============================================================
# 7. RUN REPLAY
# ============================================================

def run_replay(
    timing_gaps,
    profiles,
    max_events=None
):

    keys, probabilities = (
        build_selection_distribution(
            profiles
        )
    )

    print("\n========================================")
    print("        REPLAY ENGINE STARTED")
    print("========================================")

    print(
        f"Return rate: "
        f"{RETURN_RATE * 100:.2f}%"
    )

    print(
        f"Compression factor: "
        f"{COMPRESS_FACTOR}"
    )

    print(
        f"Maximum events: "
        f"{max_events if max_events else 'CONTINUOUS'}"
    )

    print("========================================\n")

    conn = get_connection()

    event_count = 0

    try:

        while True:

            # ------------------------------------------------
            # Stop condition
            # ------------------------------------------------

            if (
                max_events is not None
                and event_count >= max_events
            ):
                break

            # ------------------------------------------------
            # Select store-product according to demand weight
            # ------------------------------------------------

            index = np.random.choice(
                len(keys),
                p=probabilities
            )

            store_id, product_id = keys[index]

            profile = profiles[
                (store_id, product_id)
            ]

            # ------------------------------------------------
            # Generate quantity
            # ------------------------------------------------

            quantity = generate_quantity(
                profile["quantities"]
            )

            # ------------------------------------------------
            # Sale or return
            # ------------------------------------------------

            quantity, is_return = (
                generate_transaction(
                    quantity
                )
            )

            # ------------------------------------------------
            # Insert into orders
            # ------------------------------------------------

            order_id, event_time = insert_order(
                conn,
                store_id,
                product_id,
                quantity
            )

            event_count += 1

            event_type = (
                "RETURN"
                if is_return
                else "SALE"
            )

            print(
                f"[replay] "
                f"event={event_count:03d} | "
                f"order={order_id} | "
                f"{event_type:6s} | "
                f"{store_id}/{product_id} | "
                f"qty={quantity:+d} | "
                f"time={event_time}"
            )

            # ------------------------------------------------
            # Wait before next event
            # ------------------------------------------------

            gap = float(
                random.choice(timing_gaps.to_numpy())
            )

            time.sleep(gap)

    except KeyboardInterrupt:

        print(
            "\n\nReplay stopped manually."
        )

    finally:

        conn.close()

    print(
        f"\nReplay completed. "
        f"Events generated: {event_count}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("         INVENTORY REPLAY ENGINE")
    print("========================================")

    timing_gaps = load_timing_pattern()

    demand_profiles = load_demand_profiles()

    run_replay(
        timing_gaps,
        demand_profiles,
        MAX_EVENTS
    )