select * from historical_inventory;
select count(*) from historical_inventory;
CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(20) PRIMARY KEY,
    region VARCHAR(50)
);
INSERT INTO stores (store_id, region)
SELECT DISTINCT store_id, region
FROM historical_inventory;
select * from stores;
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50)
);
/*old table*/
INSERT INTO products (product_id, category)
SELECT DISTINCT product_id, category
FROM historical_inventory;
DROP TABLE products;
/*new table*/
CREATE TABLE products (
    store_id VARCHAR(20) REFERENCES stores(store_id),
    product_id VARCHAR(20),
    category VARCHAR(50),
    PRIMARY KEY (store_id, product_id)
);
INSERT INTO products (store_id, product_id, category)

SELECT COUNT(*) FROM products;
SELECT * FROM products
ORDER BY store_id, product_id;
/*checking*/
SELECT DISTINCT
    store_id,
    product_id,
    category
FROM historical_inventory;
SELECT * FROM products
ORDER BY store_id,product_id;

SELECT product_id, COUNT(DISTINCT category) AS category_count
FROM historical_inventory
GROUP BY product_id
HAVING COUNT(DISTINCT category) > 1;

SELECT DISTINCT product_id, category
FROM historical_inventory
WHERE product_id = 'P0003'
ORDER BY category;

SELECT
    store_id,
    product_id,
    COUNT(DISTINCT category) AS category_count
FROM historical_inventory
GROUP BY store_id, product_id
HAVING COUNT(DISTINCT category) > 1;


CREATE TABLE IF NOT EXISTS current_inventory (
    store_id VARCHAR(20),
    product_id VARCHAR(20),
    current_stock INT NOT NULL,
    last_updated TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (store_id, product_id),

    FOREIGN KEY (store_id, product_id)
        REFERENCES products(store_id, product_id)
);

INSERT INTO current_inventory (
    store_id,
    product_id,
    current_stock
)
SELECT DISTINCT ON (store_id, product_id)
    store_id,
    product_id,
    inventory_level
FROM historical_inventory
ORDER BY store_id, product_id, date DESC;

SELECT COUNT(*) FROM current_inventory;

SELECT *
FROM current_inventory
ORDER BY store_id, product_id;

select * from supply_chain_history;
select count(*) from supply_chain_history;
SELECT
    date,
    sku_id,
    warehouse_id,
    COUNT(*) AS count
FROM supply_chain_history
GROUP BY
    date,
    sku_id,
    warehouse_id
HAVING COUNT(*) > 1;
SELECT
    sku_id,
    COUNT(DISTINCT warehouse_id) AS number_of_warehouses
FROM supply_chain_history
GROUP BY sku_id
ORDER BY sku_id;

SELECT
    sku_id,
    COUNT(DISTINCT supplier_id) AS number_of_suppliers
FROM supply_chain_history
GROUP BY sku_id
ORDER BY sku_id;

SELECT
    supplier_id,
    COUNT(DISTINCT sku_id) AS number_of_skus
FROM supply_chain_history
GROUP BY supplier_id
ORDER BY supplier_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT supplier_id) AS number_of_suppliers
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT supplier_id) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    warehouse_id,
    COUNT(DISTINCT region) AS number_of_regions
FROM supply_chain_history
GROUP BY warehouse_id
ORDER BY warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT supplier_id) AS number_of_suppliers
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
ORDER BY
    sku_id,
    warehouse_id;


SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT supplier_id) AS number_of_suppliers
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT supplier_id) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT region) AS number_of_regions
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT region) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT supplier_lead_time_days) AS number_of_lead_times
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT supplier_lead_time_days) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT reorder_point) AS number_of_reorder_points
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT reorder_point) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT unit_cost) AS number_of_unit_costs
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT unit_cost) > 1
ORDER BY
    sku_id,
    warehouse_id;

SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT unit_price) AS number_of_unit_prices
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT unit_price) > 1
ORDER BY
    sku_id,
    warehouse_id;


SELECT
    sku_id,
    warehouse_id,
    COUNT(DISTINCT order_quantity) AS number_of_order_quantities
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id
HAVING COUNT(DISTINCT order_quantity) > 1
ORDER BY
    sku_id,
    warehouse_id;

CREATE TABLE sku_warehouse (
    sku_id VARCHAR(20),
    warehouse_id VARCHAR(20),
    supplier_id VARCHAR(20),
    supplier_lead_time_days INT,
    reorder_point INT,
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),

    PRIMARY KEY (sku_id, warehouse_id)
);
INSERT INTO sku_warehouse (
    sku_id,
    warehouse_id,
    supplier_id,
    supplier_lead_time_days,
    reorder_point,
    unit_cost,
    unit_price
)
SELECT
    sku_id,
    warehouse_id,
    MIN(supplier_id) AS supplier_id,
    MIN(supplier_lead_time_days) AS supplier_lead_time_days,
    MIN(reorder_point) AS reorder_point,
    MIN(unit_cost) AS unit_cost,
    MIN(unit_price) AS unit_price
FROM supply_chain_history
GROUP BY
    sku_id,
    warehouse_id;

select * from sku_warehouse order by sku_id,warehouse_id;
select count(*) from sku_warehouse;

SELECT COUNT(*)
FROM supply_chain_history h
LEFT JOIN sku_warehouse sw
    ON h.sku_id = sw.sku_id
    AND h.warehouse_id = sw.warehouse_id
WHERE sw.sku_id IS NULL;


select * from procurement_orders;
drop table procurement_orders;
CREATE TABLE procurement_orders (
    po_id VARCHAR(20) PRIMARY KEY,
    supplier VARCHAR(50),
    order_date DATE,
    delivery_date DATE,
    item_category VARCHAR(50),
    order_status VARCHAR(30),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    negotiated_price NUMERIC(10,2),
    defective_units NUMERIC(10,2),
    compliance VARCHAR(10)
);
select count(*) from procurement_orders;

DROP TABLE IF EXISTS retail_transactions;

CREATE TABLE retail_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,

    invoice VARCHAR(20),
    stock_code VARCHAR(30),
    description TEXT,

    quantity INTEGER,
    invoice_date TIMESTAMP,

    price NUMERIC(12,2),
    customer_id NUMERIC(12,0),

    country VARCHAR(50)
);
TRUNCATE TABLE retail_transactions;
select * from retail_transactions;
select count(*) from retail_transactions;
SELECT 
    MIN(invoice_date) AS start_date,
    MAX(invoice_date) AS end_date,
    COUNT(DISTINCT invoice) AS unique_invoices
FROM retail_transactions;
CREATE OR REPLACE VIEW clean_retail_transactions AS
SELECT
    transaction_id,
    invoice,
    stock_code,
    description,
    quantity,
    invoice_date,
    price,
    customer_id,
    country,

    quantity * price AS transaction_value,

    CASE
        WHEN invoice LIKE 'C%' THEN 'RETURN'
        WHEN quantity < 0 THEN 'NEGATIVE_ADJUSTMENT'
        WHEN price < 0 THEN 'FINANCIAL_ADJUSTMENT'
        WHEN quantity > 0 AND price > 0 THEN 'SALE'
        WHEN price = 0 THEN 'ZERO_PRICE'
        ELSE 'OTHER'
    END AS transaction_type

FROM retail_transactions;

SELECT
    transaction_type,
    COUNT(*) AS transaction_count
FROM clean_retail_transactions
GROUP BY transaction_type
ORDER BY transaction_count DESC;
SELECT *
FROM clean_retail_transactions
LIMIT 20;

SELECT
    COUNT(*) AS sale_rows,
    COUNT(DISTINCT stock_code) AS unique_stockcodes,
    SUM(quantity) AS total_units,
    SUM(transaction_value) AS total_sales_value
FROM clean_retail_transactions
WHERE transaction_type = 'SALE';

SELECT
    stock_code,
    description,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(transaction_value) AS total_value
FROM clean_retail_transactions
WHERE transaction_type = 'SALE'
GROUP BY stock_code, description
ORDER BY total_quantity DESC
LIMIT 30;

SELECT
    invoice,
    stock_code,
    description,
    quantity,
    price,
    transaction_value,
    invoice_date
FROM clean_retail_transactions
WHERE transaction_type = 'SALE'
ORDER BY quantity DESC
LIMIT 30;

CREATE TABLE product_daily_demand AS
SELECT
    stock_code,
    DATE(invoice_date) AS demand_date,

    SUM(quantity) AS units_sold,

    SUM(transaction_value) AS sales_value,

    COUNT(*) AS transaction_count,

    COUNT(DISTINCT invoice) AS invoice_count

FROM clean_retail_transactions

WHERE transaction_type = 'SALE'
  AND quantity > 0
  AND price > 0

GROUP BY
    stock_code,
    DATE(invoice_date);

SELECT COUNT(*)
FROM product_daily_demand;

SELECT *
FROM product_daily_demand
ORDER BY demand_date, stock_code
LIMIT 20;

SELECT
    MIN(demand_date) AS start_date,
    MAX(demand_date) AS end_date,
    COUNT(DISTINCT stock_code) AS products,
    SUM(units_sold) AS total_units,
    SUM(sales_value) AS total_sales
FROM product_daily_demand;

SELECT
    stock_code,
    COUNT(*) AS active_days,
    MIN(demand_date) AS first_sale_date,
    MAX(demand_date) AS last_sale_date,
    SUM(units_sold) AS total_units_sold,
    AVG(units_sold) AS avg_daily_units
FROM product_daily_demand
GROUP BY stock_code
ORDER BY total_units_sold DESC
LIMIT 20;

DROP TABLE IF EXISTS product_daily_demand;

CREATE TABLE product_daily_demand AS

WITH date_range AS (
    SELECT
        MIN(invoice_date)::date AS min_date,
        MAX(invoice_date)::date AS max_date
    FROM clean_retail_transactions
),

products AS (
    SELECT DISTINCT stock_code
    FROM clean_retail_transactions
),

calendar AS (
    SELECT
        generate_series(
            (SELECT min_date FROM date_range),
            (SELECT max_date FROM date_range),
            INTERVAL '1 day'
        )::date AS demand_date
)

SELECT
    p.stock_code,
    c.demand_date,

    COALESCE(SUM(
        CASE
            WHEN crt.quantity > 0
            THEN crt.quantity
            ELSE 0
        END
    ), 0) AS units_sold,

    COALESCE(SUM(
        CASE
            WHEN crt.quantity > 0
            THEN crt.quantity * crt.price
            ELSE 0
        END
    ), 0) AS sales_value,

    COUNT(
        CASE
            WHEN crt.quantity > 0
            THEN 1
        END
    ) AS transaction_count,

    COUNT(DISTINCT
        CASE
            WHEN crt.quantity > 0
            THEN crt.invoice
        END
    ) AS invoice_count

FROM products p
CROSS JOIN calendar c

LEFT JOIN clean_retail_transactions crt
    ON crt.stock_code = p.stock_code
    AND crt.invoice_date::date = c.demand_date

GROUP BY
    p.stock_code,
    c.demand_date;

SELECT *
FROM product_daily_demand
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 20;


ALTER TABLE product_daily_demand
ADD COLUMN lag_1 INTEGER,
ADD COLUMN lag_7 INTEGER,
ADD COLUMN lag_14 INTEGER,
ADD COLUMN lag_28 INTEGER;


WITH lagged AS (
    SELECT
        stock_code,
        demand_date,

        LAG(units_sold, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS l1,

        LAG(units_sold, 7) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS l7,

        LAG(units_sold, 14) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS l14,

        LAG(units_sold, 28) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS l28

    FROM product_daily_demand
)

UPDATE product_daily_demand p
SET
    lag_1 = l.l1,
    lag_7 = l.l7,
    lag_14 = l.l14,
    lag_28 = l.l28
FROM lagged l
WHERE p.stock_code = l.stock_code
  AND p.demand_date = l.demand_date;

 SELECT *
FROM product_daily_demand
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 35;

ALTER TABLE product_daily_demand
ADD COLUMN rolling_7d_avg NUMERIC(12,2),
ADD COLUMN rolling_30d_avg NUMERIC(12,2);


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'product_daily_demand'
ORDER BY ordinal_position;

WITH rolling_features AS (
    SELECT
        stock_code,
        demand_date,

        AVG(units_sold) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS r7,

        AVG(units_sold) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS r30

    FROM product_daily_demand
)

UPDATE product_daily_demand p
SET
    rolling_7d_avg = rf.r7,
    rolling_30d_avg = rf.r30
FROM rolling_features rf
WHERE p.stock_code = rf.stock_code
  AND p.demand_date = rf.demand_date;

SELECT
    stock_code,
    demand_date,
    units_sold,
    lag_1,
    lag_7,
    lag_14,
    lag_28,
    rolling_7d_avg,
    rolling_30d_avg
FROM product_daily_demand
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 40;

ALTER TABLE product_daily_demand
ADD COLUMN day_of_week INTEGER,
ADD COLUMN month INTEGER,
ADD COLUMN quarter INTEGER,
ADD COLUMN is_weekend BOOLEAN;

UPDATE product_daily_demand
SET
    day_of_week = EXTRACT(ISODOW FROM demand_date)::INTEGER,
    month = EXTRACT(MONTH FROM demand_date)::INTEGER,
    quarter = EXTRACT(QUARTER FROM demand_date)::INTEGER,
    is_weekend = EXTRACT(ISODOW FROM demand_date) IN (6, 7);

	SELECT
    stock_code,
    demand_date,
    units_sold,
    day_of_week,
    month,
    quarter,
    is_weekend
FROM product_daily_demand
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 15;

ALTER TABLE product_daily_demand
ADD COLUMN rolling_7d_std NUMERIC(12,2),
ADD COLUMN rolling_30d_std NUMERIC(12,2);

WITH volatility_features AS (
    SELECT
        stock_code,
        demand_date,

        STDDEV_SAMP(units_sold) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS std_7,

        STDDEV_SAMP(units_sold) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS std_30

    FROM product_daily_demand
)

UPDATE product_daily_demand p
SET
    rolling_7d_std = vf.std_7,
    rolling_30d_std = vf.std_30
FROM volatility_features vf
WHERE p.stock_code = vf.stock_code
  AND p.demand_date = vf.demand_date;

SELECT
    stock_code,
    demand_date,
    units_sold,
    rolling_7d_avg,
    rolling_30d_avg,
    rolling_7d_std,
    rolling_30d_std
FROM product_daily_demand
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 20;


WITH daily_demand AS (
    SELECT
        stock_code,
        invoice_date::date AS demand_date,
        SUM(quantity) AS daily_quantity
    FROM retail_transactions
    WHERE quantity > 0
      AND price > 0
    GROUP BY stock_code, invoice_date::date
),

features AS (
    SELECT
        stock_code,
        demand_date,
        daily_quantity,

        LAG(daily_quantity, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_1,

        LAG(daily_quantity, 7) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_7,

        LAG(daily_quantity, 14) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_14,

        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_avg,

        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS rolling_14d_avg,

        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_30d_avg,

        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_std,

        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS rolling_14d_std,

        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_30d_std

    FROM daily_demand
)

SELECT
    *,
    
    CASE
        WHEN rolling_30d_avg > 0
        THEN rolling_30d_std / rolling_30d_avg
        ELSE NULL
    END AS rolling_30d_cv,

    rolling_7d_avg - rolling_14d_avg AS demand_trend_7d,

    rolling_14d_avg - rolling_30d_avg AS demand_trend_30d

FROM features
ORDER BY stock_code, demand_date;


DROP TABLE IF EXISTS daily_product_demand;

CREATE TABLE daily_product_demand AS
SELECT
    stock_code,
    DATE(invoice_date) AS demand_date,

    SUM(
        CASE
            WHEN invoice NOT LIKE 'C%'
                 AND quantity > 0
                 AND price > 0
            THEN quantity
            ELSE 0
        END
    ) AS daily_quantity,

    SUM(
        CASE
            WHEN invoice NOT LIKE 'C%'
                 AND quantity > 0
                 AND price > 0
            THEN quantity * price
            ELSE 0
        END
    ) AS daily_revenue,

    COUNT(
        CASE
            WHEN invoice NOT LIKE 'C%'
                 AND quantity > 0
                 AND price > 0
            THEN 1
        END
    ) AS transaction_count,

    COUNT(DISTINCT
        CASE
            WHEN invoice NOT LIKE 'C%'
                 AND quantity > 0
                 AND price > 0
            THEN customer_id
        END
    ) AS customer_count

FROM retail_transactions
GROUP BY
    stock_code,
    DATE(invoice_date);


SELECT *
FROM daily_product_demand
ORDER BY stock_code, demand_date
LIMIT 20;


DROP TABLE IF EXISTS daily_product_demand;

CREATE TABLE daily_product_demand AS
SELECT
    p.stock_code,
    d.demand_date,
    COALESCE(dp.daily_quantity, 0) AS daily_quantity,
    COALESCE(dp.daily_revenue, 0) AS daily_revenue,
    COALESCE(dp.transaction_count, 0) AS transaction_count,
    COALESCE(dp.customer_count, 0) AS customer_count
FROM
(
    SELECT
        stock_code,
        MIN(demand_date) AS min_date,
        MAX(demand_date) AS max_date
    FROM
        (
            SELECT
                stock_code,
                DATE(invoice_date) AS demand_date,
                SUM(
                    CASE
                        WHEN invoice NOT LIKE 'C%'
                             AND quantity > 0
                             AND price > 0
                        THEN quantity
                        ELSE 0
                    END
                ) AS daily_quantity,
                SUM(
                    CASE
                        WHEN invoice NOT LIKE 'C%'
                             AND quantity > 0
                             AND price > 0
                        THEN quantity * price
                        ELSE 0
                    END
                ) AS daily_revenue,
                COUNT(
                    CASE
                        WHEN invoice NOT LIKE 'C%'
                             AND quantity > 0
                             AND price > 0
                        THEN 1
                    END
                ) AS transaction_count,
                COUNT(DISTINCT
                    CASE
                        WHEN invoice NOT LIKE 'C%'
                             AND quantity > 0
                             AND price > 0
                        THEN customer_id
                    END
                ) AS customer_count
            FROM retail_transactions
            GROUP BY stock_code, DATE(invoice_date)
        ) x
    GROUP BY stock_code
) p
CROSS JOIN LATERAL
(
    SELECT generate_series(
        p.min_date,
        p.max_date,
        INTERVAL '1 day'
    )::date AS demand_date
) d
LEFT JOIN
(
    SELECT
        stock_code,
        DATE(invoice_date) AS demand_date,
        SUM(
            CASE
                WHEN invoice NOT LIKE 'C%'
                     AND quantity > 0
                     AND price > 0
                THEN quantity
                ELSE 0
            END
        ) AS daily_quantity,
        SUM(
            CASE
                WHEN invoice NOT LIKE 'C%'
                     AND quantity > 0
                     AND price > 0
                THEN quantity * price
                ELSE 0
            END
        ) AS daily_revenue,
        COUNT(
            CASE
                WHEN invoice NOT LIKE 'C%'
                     AND quantity > 0
                     AND price > 0
                THEN 1
            END
        ) AS transaction_count,
        COUNT(DISTINCT
            CASE
                WHEN invoice NOT LIKE 'C%'
                     AND quantity > 0
                     AND price > 0
                THEN customer_id
            END
        ) AS customer_count
    FROM retail_transactions
    GROUP BY stock_code, DATE(invoice_date)
) dp
ON dp.stock_code = p.stock_code
AND dp.demand_date = d.demand_date;

DROP TABLE IF EXISTS product_daily_calendar;

CREATE TABLE product_daily_calendar AS
SELECT
    p.stock_code,
    d.demand_date,
    COALESCE(dp.daily_quantity, 0) AS daily_quantity,
    COALESCE(dp.daily_revenue, 0) AS daily_revenue,
    COALESCE(dp.transaction_count, 0) AS transaction_count,
    COALESCE(dp.customer_count, 0) AS customer_count
FROM (
    SELECT
        stock_code,
        MIN(demand_date) AS min_date,
        MAX(demand_date) AS max_date
    FROM daily_product_demand
    GROUP BY stock_code
) p
CROSS JOIN LATERAL (
    SELECT generate_series(
        p.min_date,
        p.max_date,
        INTERVAL '1 day'
    )::date AS demand_date
) d
LEFT JOIN daily_product_demand dp
    ON dp.stock_code = p.stock_code
    AND dp.demand_date = d.demand_date;

DROP TABLE IF EXISTS product_ml_features;

CREATE TABLE product_ml_features AS
WITH base AS (
    SELECT
        stock_code,
        demand_date,
        daily_quantity,
        daily_revenue,
        transaction_count,
        customer_count,

        -- Lag features
        LAG(daily_quantity, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_1,

        LAG(daily_quantity, 7) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_7,

        LAG(daily_quantity, 14) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_14,

        -- Rolling averages
        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_avg,

        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS rolling_14d_avg,

        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_30d_avg,

        -- Rolling volatility
        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_std,

        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS rolling_14d_std,

        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_30d_std,

        -- Target: tomorrow's demand
        LEAD(daily_quantity, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS target_next_day

    FROM product_daily_calendar
)

SELECT
    *,

    -- Coefficient of variation
    CASE
        WHEN rolling_30d_avg > 0
        THEN rolling_30d_std / rolling_30d_avg
        ELSE NULL
    END AS rolling_30d_cv,

    -- Demand trends
    rolling_7d_avg - rolling_14d_avg AS demand_trend_7d,

    rolling_14d_avg - rolling_30d_avg AS demand_trend_30d,

    -- Calendar features
    EXTRACT(DOW FROM demand_date)::integer AS day_of_week,

    EXTRACT(DAY FROM demand_date)::integer AS day_of_month,

    EXTRACT(MONTH FROM demand_date)::integer AS month,

    EXTRACT(WEEK FROM demand_date)::integer AS week_of_year,

    CASE
        WHEN EXTRACT(DOW FROM demand_date) IN (0, 6)
        THEN 1
        ELSE 0
    END AS is_weekend

FROM base;


SELECT *
FROM product_ml_features
WHERE stock_code = '84077'
ORDER BY demand_date
LIMIT 20;


DROP TABLE IF EXISTS product_ml_features;

CREATE TABLE product_ml_features AS
WITH features AS (
    SELECT
        stock_code,
        demand_date,
        daily_quantity,
        daily_revenue,
        transaction_count,
        customer_count,

        -- Previous demand
        LAG(daily_quantity, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_1,

        LAG(daily_quantity, 7) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_7,

        LAG(daily_quantity, 14) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS lag_14,

        -- Previous 7 days (excluding today)
        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS rolling_7d_avg,

        -- Previous 14 days (excluding today)
        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ) AS rolling_14d_avg,

        -- Previous 30 days (excluding today)
        AVG(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS rolling_30d_avg,

        -- Previous 7-day volatility
        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS rolling_7d_std,

        -- Previous 14-day volatility
        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ) AS rolling_14d_std,

        -- Previous 30-day volatility
        STDDEV(daily_quantity) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS rolling_30d_std,

        -- Tomorrow's actual demand = ML target
        LEAD(daily_quantity, 1) OVER (
            PARTITION BY stock_code
            ORDER BY demand_date
        ) AS target_next_day,

        -- Calendar features
        EXTRACT(DOW FROM demand_date)::integer AS day_of_week,
        EXTRACT(DAY FROM demand_date)::integer AS day_of_month,
        EXTRACT(MONTH FROM demand_date)::integer AS month,
        EXTRACT(WEEK FROM demand_date)::integer AS week_of_year,

        CASE
            WHEN EXTRACT(DOW FROM demand_date) IN (0, 6)
            THEN 1
            ELSE 0
        END AS is_weekend

    FROM product_daily_calendar
)

SELECT
    *,

    -- Volatility relative to average demand
    CASE
        WHEN rolling_30d_avg > 0
        THEN rolling_30d_std / rolling_30d_avg
        ELSE NULL
    END AS rolling_30d_cv,

    -- Short-term trend
    CASE
        WHEN rolling_14d_avg IS NOT NULL
        THEN rolling_7d_avg - rolling_14d_avg
        ELSE NULL
    END AS demand_trend_7d,

    -- Longer-term trend
    CASE
        WHEN rolling_30d_avg IS NOT NULL
        THEN rolling_14d_avg - rolling_30d_avg
        ELSE NULL
    END AS demand_trend_30d

FROM features;



SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE rolling_7d_avg IS NULL
    ) AS no_7d_history,

    COUNT(*) FILTER (
        WHERE rolling_14d_avg IS NULL
    ) AS no_14d_history,

    COUNT(*) FILTER (
        WHERE rolling_30d_avg IS NULL
    ) AS no_30d_history,

    COUNT(*) FILTER (
        WHERE lag_14 IS NULL
    ) AS no_lag14,

    COUNT(*) FILTER (
        WHERE target_next_day IS NULL
    ) AS no_target

FROM product_ml_features;


select * FROM product_daily_calendar


SELECT *
FROM current_inventory
LIMIT 10;

SELECT *
FROM products
LIMIT 10;

SELECT *
FROM product_daily_calendar
LIMIT 10;

SELECT *
FROM current_inventory
LIMIT 10;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'current_inventory'
ORDER BY ordinal_position;

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT store_id) AS stores,
       COUNT(DISTINCT product_id) AS products
FROM current_inventory;


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'products'
ORDER BY ordinal_position;

SELECT *
FROM historical_inventory
LIMIT 20;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'historical_inventory'
ORDER BY ordinal_position;


SELECT
    MIN(date) AS min_date,
    MAX(date) AS max_date,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT store_id) AS stores,
    COUNT(DISTINCT product_id) AS products,
    COUNT(DISTINCT (store_id, product_id)) AS store_product_pairs
FROM historical_inventory;

SELECT
    store_id,
    product_id,
    COUNT(*) AS days,
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM historical_inventory
GROUP BY store_id, product_id
ORDER BY days
LIMIT 20;




DROP TABLE IF EXISTS inventory_ml_features;

CREATE TABLE inventory_ml_features AS

WITH base AS (

    SELECT
        store_id,
        product_id,
        date,

        -- Original Dataset A variables
        demand,
        units_sold,
        units_ordered,
        inventory_level,
        price,
        discount,
        promotion,
        competitor_pricing,
        weather_condition,
        seasonality,
        epidemic,

        -- ====================================================
        -- LAG FEATURES
        -- ====================================================

        LAG(demand, 1) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
        ) AS lag_1,

        LAG(demand, 7) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
        ) AS lag_7,

        LAG(demand, 14) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
        ) AS lag_14,

        -- ====================================================
        -- ROLLING DEMAND FEATURES
        -- Previous completed days ONLY
        -- ====================================================

        AVG(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS rolling_7d_avg,

        AVG(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ) AS rolling_14d_avg,

        AVG(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS rolling_30d_avg,

        -- ====================================================
        -- ROLLING DEMAND VOLATILITY
        -- ====================================================

        STDDEV(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS rolling_7d_std,

        STDDEV(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 14 PRECEDING AND 1 PRECEDING
        ) AS rolling_14d_std,

        STDDEV(demand) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS rolling_30d_std,

        -- ====================================================
        -- TARGET
        -- Tomorrow's demand
        -- ====================================================

        LEAD(demand, 1) OVER (
            PARTITION BY store_id, product_id
            ORDER BY date
        ) AS target_next_day

    FROM historical_inventory
)

SELECT
    base.*,

    -- ========================================================
    -- CALENDAR FEATURES
    -- ========================================================

    EXTRACT(DOW FROM date)::integer AS day_of_week,

    EXTRACT(DAY FROM date)::integer AS day_of_month,

    EXTRACT(MONTH FROM date)::integer AS month,

    EXTRACT(WEEK FROM date)::integer AS week_of_year,

    CASE
        WHEN EXTRACT(DOW FROM date) IN (0, 6)
        THEN 1
        ELSE 0
    END AS is_weekend,

    -- ========================================================
    -- DEMAND TREND FEATURES
    -- ========================================================

    rolling_7d_avg - rolling_14d_avg
        AS demand_trend_7d,

    rolling_14d_avg - rolling_30d_avg
        AS demand_trend_30d

FROM base;

SELECT *
FROM inventory_ml_features
LIMIT 10;

SELECT
    COUNT(*) AS total_rows,
    COUNT(target_next_day) AS rows_with_target,
    COUNT(lag_1) AS rows_with_lag1,
    COUNT(lag_7) AS rows_with_lag7,
    COUNT(lag_14) AS rows_with_lag14
FROM inventory_ml_features;



SELECT COUNT(*) AS rows
FROM inventory_ml_features;

SELECT
    COUNT(*) AS total_rows,

    COUNT(DISTINCT lag_1) AS lag_1_values,
    COUNT(DISTINCT lag_7) AS lag_7_values,
    COUNT(DISTINCT lag_14) AS lag_14_values,

    COUNT(DISTINCT rolling_7d_avg) AS rolling_7d_avg_values,
    COUNT(DISTINCT rolling_14d_avg) AS rolling_14d_avg_values,
    COUNT(DISTINCT rolling_30d_avg) AS rolling_30d_avg_values,

    COUNT(DISTINCT rolling_7d_std) AS rolling_7d_std_values,
    COUNT(DISTINCT rolling_14d_std) AS rolling_14d_std_values,
    COUNT(DISTINCT rolling_30d_std) AS rolling_30d_std_values,

    COUNT(DISTINCT demand_trend_7d) AS trend_7d_values,
    COUNT(DISTINCT demand_trend_30d) AS trend_30d_values,

    COUNT(DISTINCT day_of_week) AS day_of_week_values,
    COUNT(DISTINCT day_of_month) AS day_of_month_values,
    COUNT(DISTINCT month) AS month_values,
    COUNT(DISTINCT week_of_year) AS week_values,
    COUNT(DISTINCT is_weekend) AS weekend_values

FROM inventory_ml_features;


SELECT *
FROM supply_chain_history
LIMIT 10;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'supply_chain_history'
ORDER BY ordinal_position;

SELECT *
FROM sku_warehouse
LIMIT 20;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'sku_warehouse'
ORDER BY ordinal_position;

SELECT *
FROM procurement_orders
LIMIT 20;


SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'procurement_orders'
ORDER BY ordinal_position;


SELECT
    supplier_id,
    COUNT(*) AS observations,
    ROUND(AVG(supplier_lead_time_days), 2) AS avg_lead_time,
    ROUND(STDDEV(supplier_lead_time_days), 2) AS lead_time_std,
    MIN(supplier_lead_time_days) AS min_lead_time,
    MAX(supplier_lead_time_days) AS max_lead_time
FROM supply_chain_history
GROUP BY supplier_id
ORDER BY supplier_id;

SELECT
    MIN(supplier_lead_time_days) AS min_lead_time,
    MAX(supplier_lead_time_days) AS max_lead_time,
    ROUND(AVG(supplier_lead_time_days), 2) AS avg_lead_time,
    ROUND(STDDEV(supplier_lead_time_days), 2) AS std_lead_time
FROM supply_chain_history;


SELECT
    supplier,
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE order_status = 'Delivered'
    ) AS delivered_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_status = 'Delivered'
        ) / COUNT(*),
        2
    ) AS delivery_rate,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN defective_units IS NULL THEN 0
                ELSE defective_units::numeric / NULLIF(quantity, 0)
            END
        ),
        2
    ) AS defect_rate_pct,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN compliance = 'Yes' THEN 1
                ELSE 0
            END
        ),
        2
    ) AS compliance_rate
FROM procurement_orders
GROUP BY supplier
ORDER BY supplier;

CREATE TABLE supplier_profiles AS

WITH lead_time AS (
    SELECT
        supplier_id,
        COUNT(*) AS lead_time_observations,
        ROUND(AVG(supplier_lead_time_days), 2) AS avg_lead_time_days,
        ROUND(STDDEV(supplier_lead_time_days), 2) AS lead_time_std_days,
        MIN(supplier_lead_time_days) AS min_lead_time_days,
        MAX(supplier_lead_time_days) AS max_lead_time_days
    FROM supply_chain_history
    GROUP BY supplier_id
),

procurement AS (
    SELECT
        supplier,
        ROUND(
            100.0 * COUNT(*) FILTER (
                WHERE order_status = 'Delivered'
            ) / COUNT(*),
            2
        ) AS delivery_rate_pct,

        ROUND(
            100.0 * AVG(
                CASE
                    WHEN defective_units IS NULL THEN 0
                    ELSE defective_units::numeric / NULLIF(quantity, 0)
                END
            ),
            2
        ) AS defect_rate_pct,

        ROUND(
            100.0 * AVG(
                CASE
                    WHEN compliance = 'Yes' THEN 1
                    ELSE 0
                END
            ),
            2
        ) AS compliance_rate_pct

    FROM procurement_orders
    GROUP BY supplier
),

-- Assign the 5 real procurement profiles
-- cyclically to our 10 internal suppliers.
-- This is a calibration, NOT an identity mapping.
assigned_profiles AS (
    SELECT
        'SUP_' || gs AS supplier_id,
        p.supplier AS source_procurement_profile
    FROM generate_series(1, 10) AS gs
    JOIN (
        SELECT
            supplier,
            ROW_NUMBER() OVER (ORDER BY supplier) AS rn
        FROM procurement
    ) p
    ON ((gs - 1) % 5) + 1 = p.rn
)

SELECT
    lt.supplier_id,

    lt.lead_time_observations,
    lt.avg_lead_time_days,
    lt.lead_time_std_days,
    lt.min_lead_time_days,
    lt.max_lead_time_days,

    pr.delivery_rate_pct,
    pr.defect_rate_pct,
    pr.compliance_rate_pct,

    ROUND(
        (
            0.50 * pr.delivery_rate_pct
            + 0.30 * pr.compliance_rate_pct
            + 0.20 * (100 - pr.defect_rate_pct)
        ),
        2
    ) AS reliability_score,

    ap.source_procurement_profile

FROM lead_time lt

JOIN assigned_profiles ap
    ON lt.supplier_id = ap.supplier_id

JOIN procurement pr
    ON ap.source_procurement_profile = pr.supplier;
SELECT *
FROM supplier_profiles
ORDER BY supplier_id;


SELECT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_name = 'product_supplier_map'
);


SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'supplier_profiles';

SELECT supplier_id, COUNT(*)
FROM supplier_profiles
GROUP BY supplier_id
HAVING COUNT(*) > 1;

ALTER TABLE supplier_profiles
ADD PRIMARY KEY (supplier_id);

CREATE TABLE product_supplier_map (
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (store_id, product_id),
    FOREIGN KEY (supplier_id)
        REFERENCES supplier_profiles(supplier_id)
);

SELECT *
FROM product_supplier_map;

INSERT INTO product_supplier_map (
    store_id,
    product_id,
    supplier_id
)
SELECT
    store_id,
    product_id,
    'SUP_' || (
        ROW_NUMBER() OVER (
            ORDER BY store_id, product_id
        ) % 10 + 1
    )::text
FROM current_inventory;


SELECT *
FROM retail_transactions LIMIT 10;


SELECT *
FROM daily_product_demand
LIMIT 10;

SELECT *
FROM product_daily_calendar
LIMIT 10;

SELECT *
FROM product_daily_demand
LIMIT 10;


SELECT *
FROM product_ml_features
LIMIT 10;


SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name IN (
    'store_id',
    'product_id',
    'lag_1',
    'lag_7',
    'lag_14'
)
ORDER BY table_name, ordinal_position;


SELECT *
FROM inventory_ml_features
LIMIT 10;

SELECT *
FROM current_inventory
LIMIT 10;


SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'supplier_profiles'
ORDER BY ordinal_position;


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'retail_transactions'
ORDER BY ordinal_position;

SELECT
    MIN(invoice_date) AS first_date,
    MAX(invoice_date) AS last_date,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT stock_code) AS unique_products,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT country) AS unique_countries
FROM retail_transactions;

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE quantity > 0) AS positive_quantity,
    COUNT(*) FILTER (WHERE quantity < 0) AS negative_quantity,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer
FROM retail_transactions;

SELECT
    country,
    COUNT(*) AS transactions
FROM retail_transactions
GROUP BY country
ORDER BY transactions DESC
LIMIT 10;


SELECT
    supplier_id,
    avg_lead_time_days,
    lead_time_std_days,
    delivery_rate_pct,
    defect_rate_pct,
    compliance_rate_pct,
    reliability_score
FROM supplier_profiles
ORDER BY reliability_score;

SELECT
    store_id,
    product_id,
    current_stock
FROM current_inventory
ORDER BY store_id, product_id
LIMIT 20;


SELECT
    psm.supplier_id,
    sp.avg_lead_time_days,
    sp.lead_time_std_days,
    sp.reliability_score,
    ROUND(
        sp.avg_lead_time_days *
        (1 - sp.reliability_score / 100.0),
        4
    ) AS supplier_score
FROM product_supplier_map psm
JOIN supplier_profiles sp
    ON psm.supplier_id = sp.supplier_id
WHERE psm.store_id = 'S001'
  AND psm.product_id = 'P0001'
ORDER BY supplier_score ASC;


CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(20) DEFAULT 'replay'
);

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;


SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'product_daily_demand'
ORDER BY ordinal_position;


SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE column_name IN (
    'store_id',
    'product_id',
    'date',
    'demand',
    'units_sold'
)
ORDER BY table_name, ordinal_position;


SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;

select * from orders;

-- 1. Orders structure
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;

-- 2. Current inventory structure
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'current_inventory'
ORDER BY ordinal_position;

SELECT *
FROM orders
ORDER BY event_time DESC
LIMIT 10;

ALTER TABLE orders
ADD COLUMN event_type VARCHAR(10) DEFAULT 'SALE';

SELECT *
FROM orders
ORDER BY order_id DESC
LIMIT 10;

CREATE OR REPLACE FUNCTION notify_new_order()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify(
        'new_order',
        NEW.order_id::text
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS orders_insert_notify ON orders;

CREATE TRIGGER orders_insert_notify
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION notify_new_order();


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;


CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id BIGSERIAL PRIMARY KEY,

    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,

    quantity INTEGER NOT NULL CHECK (quantity > 0),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expected_arrival TIMESTAMP NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',

    CONSTRAINT purchase_order_status_check
        CHECK (status IN ('PENDING', 'ARRIVED', 'CANCELLED'))
);


SELECT *
FROM purchase_orders;

SELECT *
FROM purchase_orders
ORDER BY po_id DESC;


SELECT *
FROM current_inventory
WHERE store_id = 'S001'
  AND product_id = 'P0008';

SELECT *
FROM current_inventory
ORDER BY last_updated DESC;

SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;



SELECT COUNT(*)
FROM public.clean_retail_transactions;
