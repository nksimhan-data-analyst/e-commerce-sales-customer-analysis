-- ============================================================
-- E-COMMERCE SALES & CUSTOMER ANALYSIS
-- SQL BUSINESS ANALYSIS
-- DuckDB + CSV files
-- ============================================================


-- ============================================================
-- 1. CORE BUSINESS KPIs
-- ============================================================

-- 1.1 Raw order rows
SELECT
    COUNT(*) AS total_orders
FROM 'data/raw/orders.csv';


-- 1.2 Unique orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM 'data/raw/orders.csv';


-- 1.3 Total recorded revenue
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM 'data/raw/order_items.csv';


-- 1.4 Final KPI reconciliation
SELECT
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS ordering_customers,
    ROUND(
        SUM(oi.revenue) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id;


-- ============================================================
-- 2. CUSTOMER SEGMENT ANALYSIS
-- ============================================================

-- 2.1 Revenue and profit by customer segment
WITH customer_segments AS (
    SELECT
        customer_id,
        CASE
            WHEN LOWER(customer_segment) = 'regular' THEN 'Regular'
            WHEN LOWER(customer_segment) = 'new' THEN 'New'
            WHEN LOWER(customer_segment) = 'loyal' THEN 'Loyal'
            WHEN LOWER(customer_segment) = 'premium' THEN 'Premium'
            ELSE 'Missing'
        END AS customer_segment
    FROM 'data/raw/customers.csv'
),
unique_orders AS (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
)
SELECT
    cs.customer_segment,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT uo.customer_id) AS customer_count,
    COUNT(DISTINCT uo.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN unique_orders AS uo
    ON oi.order_id = uo.order_id
JOIN customer_segments AS cs
    ON uo.customer_id = cs.customer_id
GROUP BY cs.customer_segment
ORDER BY total_revenue DESC;


-- 2.2 Revenue and profit per customer by segment
WITH customer_segments AS (
    SELECT
        customer_id,
        CASE
            WHEN LOWER(customer_segment) = 'regular' THEN 'Regular'
            WHEN LOWER(customer_segment) = 'new' THEN 'New'
            WHEN LOWER(customer_segment) = 'loyal' THEN 'Loyal'
            WHEN LOWER(customer_segment) = 'premium' THEN 'Premium'
            ELSE 'Missing'
        END AS customer_segment
    FROM 'data/raw/customers.csv'
),
customer_value AS (
    SELECT
        o.customer_id,
        SUM(oi.revenue) AS total_revenue,
        SUM(oi.profit) AS total_profit
    FROM 'data/raw/order_items.csv' AS oi
    JOIN (
        SELECT DISTINCT
            order_id,
            customer_id
        FROM 'data/raw/orders.csv'
    ) AS o
        ON oi.order_id = o.order_id
    GROUP BY o.customer_id
)
SELECT
    cs.customer_segment,
    ROUND(AVG(cv.total_revenue), 2) AS revenue_per_customer,
    ROUND(AVG(cv.total_profit), 2) AS profit_per_customer
FROM customer_value AS cv
JOIN customer_segments AS cs
    ON cv.customer_id = cs.customer_id
GROUP BY cs.customer_segment
ORDER BY revenue_per_customer DESC;


-- 2.3 Customers without orders
SELECT
    COUNT(*) AS customers_without_orders
FROM 'data/raw/customers.csv' AS c
LEFT JOIN (
    SELECT DISTINCT
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;


-- ============================================================
-- 3. PRODUCT & CATEGORY ANALYSIS
-- ============================================================

-- 3.1 Revenue and profit by category
SELECT
    p.category,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT oi.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 3.2 Category profit margin
SELECT
    p.category,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin
FROM 'data/raw/order_items.csv' AS oi
JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY profit_margin DESC;


-- 3.3 Top 10 products by revenue
SELECT
    oi.product_id,
    p.product_name,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT oi.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 3.4 Top 10 products by profit
SELECT
    oi.product_id,
    p.product_name,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT oi.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_name
ORDER BY total_profit DESC
LIMIT 10;


-- 3.5 Top 10 products by profit margin
SELECT
    oi.product_id,
    p.product_name,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin
FROM 'data/raw/order_items.csv' AS oi
JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_name
HAVING SUM(oi.revenue) > 0
ORDER BY profit_margin DESC
LIMIT 10;


-- ============================================================
-- 4. CUSTOMER VALUE ANALYSIS
-- ============================================================

-- 4.1 Customer order frequency
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM 'data/raw/orders.csv'
    GROUP BY customer_id
)
SELECT
    order_count,
    COUNT(*) AS customer_count
FROM customer_orders
GROUP BY order_count
ORDER BY order_count;


-- 4.2 Top 10 customers by revenue
SELECT
    o.customer_id,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 4.3 Top 10 customers by profit
SELECT
    o.customer_id,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY total_profit DESC
LIMIT 10;


-- 4.4 Top 10 customers by profit margin
SELECT
    o.customer_id,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
GROUP BY o.customer_id
HAVING SUM(oi.revenue) > 0
ORDER BY profit_margin DESC
LIMIT 10;


-- 4.5 Customer value: revenue + profit + margin + frequency + AOV
SELECT
    o.customer_id,

    ROUND(SUM(oi.revenue), 2) AS total_revenue,

    ROUND(SUM(oi.profit), 2) AS total_profit,

    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin,

    COUNT(DISTINCT o.order_id) AS order_count,

    ROUND(
        SUM(oi.revenue) / COUNT(DISTINCT o.order_id),
        2
    ) AS avg_order_value

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id

GROUP BY o.customer_id

HAVING SUM(oi.revenue) > 0

ORDER BY total_profit DESC

LIMIT 20;


-- ============================================================
-- 5. TIME-BASED ANALYSIS
-- ============================================================

-- 5.1 Yearly revenue, profit and orders
SELECT
    d.year,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        order_date
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
JOIN 'data/raw/dates.csv' AS d
    ON CAST(o.order_date AS DATE) = CAST(d.date AS DATE)
GROUP BY d.year
ORDER BY d.year;


-- 5.2 Yearly AOV
SELECT
    d.year,
    ROUND(
        SUM(oi.revenue) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        order_date
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
JOIN 'data/raw/dates.csv' AS d
    ON CAST(o.order_date AS DATE) = CAST(d.date AS DATE)
GROUP BY d.year
ORDER BY d.year;


-- 5.3 Monthly revenue, profit and orders
SELECT
    d.year,
    d.month_number,
    d.month_name,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        order_date
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
JOIN 'data/raw/dates.csv' AS d
    ON CAST(o.order_date AS DATE) = CAST(d.date AS DATE)
GROUP BY
    d.year,
    d.month_number,
    d.month_name
ORDER BY
    d.year,
    d.month_number;


-- ============================================================
-- 6. GEOGRAPHIC ANALYSIS
-- ============================================================

-- 6.1 Revenue and profit by region
SELECT
    l.region,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        location_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
JOIN 'data/raw/locations.csv' AS l
    ON o.location_id = l.location_id
GROUP BY l.region
ORDER BY total_revenue DESC;


-- 6.2 Top 10 states by revenue
SELECT
    l.state,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM 'data/raw/order_items.csv' AS oi
JOIN (
    SELECT DISTINCT
        order_id,
        location_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id
JOIN 'data/raw/locations.csv' AS l
    ON o.location_id = l.location_id
GROUP BY l.state
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 7. DISCOUNT & PROFITABILITY
-- ============================================================

-- 7.1 Discount vs profitability
SELECT
    oi.discount,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    COUNT(DISTINCT oi.order_id) AS order_count,
    COUNT(*) AS item_count,
    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin
FROM 'data/raw/order_items.csv' AS oi
GROUP BY oi.discount
ORDER BY oi.discount;


-- ============================================================
-- 8. SHIPPING & OPERATIONS
-- ============================================================

-- 8.1 Shipping performance
SELECT
    shipping_method,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(
        AVG(
            DATE_DIFF(
                'day',
                CAST(order_date AS DATE),
                CAST(shipping_date AS DATE)
            )
        ),
        2
    ) AS avg_shipping_days,
    MIN(
        DATE_DIFF(
            'day',
            CAST(order_date AS DATE),
            CAST(shipping_date AS DATE)
        )
    ) AS min_shipping_days,
    MAX(
        DATE_DIFF(
            'day',
            CAST(order_date AS DATE),
            CAST(shipping_date AS DATE)
        )
    ) AS max_shipping_days
FROM 'data/raw/orders.csv'
WHERE shipping_date IS NOT NULL
GROUP BY shipping_method
ORDER BY avg_shipping_days;


-- 8.2 Order status analysis
SELECT
    o.order_status,

    COUNT(DISTINCT o.order_id) AS order_count,

    ROUND(SUM(oi.revenue), 2) AS total_revenue,

    ROUND(SUM(oi.profit), 2) AS total_profit,

    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        order_status
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id

GROUP BY o.order_status

ORDER BY order_count DESC;


-- 8.3 Shipping method × profitability
SELECT
    o.shipping_method,

    COUNT(DISTINCT o.order_id) AS order_count,

    ROUND(SUM(oi.revenue), 2) AS total_revenue,

    ROUND(SUM(oi.profit), 2) AS total_profit,

    ROUND(
        SUM(oi.profit) / NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin,

    ROUND(
        AVG(
            DATE_DIFF(
                'day',
                CAST(o.order_date AS DATE),
                CAST(o.shipping_date AS DATE)
            )
        ),
        2
    ) AS avg_shipping_days

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        shipping_method,
        order_date,
        shipping_date
    FROM 'data/raw/orders.csv'
    WHERE shipping_date IS NOT NULL
) AS o
    ON oi.order_id = o.order_id

GROUP BY o.shipping_method

ORDER BY avg_shipping_days;


-- ============================================================
-- 9. DATA QUALITY & ANOMALY ANALYSIS
-- ============================================================

-- 9.1 Quantity outliers
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    revenue,
    profit
FROM 'data/raw/order_items.csv'
WHERE quantity = 99
ORDER BY quantity DESC;


-- 9.2 Revenue discrepancies
SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    oi.revenue AS recorded_revenue,

    ROUND(
        oi.quantity
        * oi.unit_price
        * (1 - oi.discount),
        2
    ) AS expected_revenue,

    ROUND(
        oi.revenue
        - (
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount)
        ),
        2
    ) AS revenue_difference

FROM 'data/raw/order_items.csv' AS oi

WHERE ABS(
    oi.revenue
    - (
        oi.quantity
        * oi.unit_price
        * (1 - oi.discount)
    )
) > 0.01

ORDER BY ABS(revenue_difference) DESC;


-- 9.3 Profit discrepancies
SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.revenue AS recorded_revenue,
    oi.profit AS recorded_profit,
    p.unit_cost,
    oi.shipping_cost,

    ROUND(
        oi.revenue
        - (oi.quantity * p.unit_cost)
        - oi.shipping_cost,
        2
    ) AS expected_profit,

    ROUND(
        oi.profit
        - (
            oi.revenue
            - (oi.quantity * p.unit_cost)
            - oi.shipping_cost
        ),
        2
    ) AS profit_difference

FROM 'data/raw/order_items.csv' AS oi

JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id

WHERE ABS(
    oi.profit
    - (
        oi.revenue
        - (oi.quantity * p.unit_cost)
        - oi.shipping_cost
    )
) > 0.01

ORDER BY ABS(profit_difference) DESC;


-- ============================================================
-- 10. CROSS-DIMENSIONAL ANALYSIS
-- ============================================================

-- 10.1 Category × customer segment
WITH customer_segments AS (
    SELECT
        customer_id,
        CASE
            WHEN LOWER(customer_segment) = 'regular' THEN 'Regular'
            WHEN LOWER(customer_segment) = 'new' THEN 'New'
            WHEN LOWER(customer_segment) = 'loyal' THEN 'Loyal'
            WHEN LOWER(customer_segment) = 'premium' THEN 'Premium'
            ELSE 'Missing'
        END AS customer_segment
    FROM 'data/raw/customers.csv'
)

SELECT
    p.category,
    cs.customer_segment,

    ROUND(SUM(oi.revenue), 2) AS total_revenue,

    ROUND(SUM(oi.profit), 2) AS total_profit,

    COUNT(DISTINCT o.order_id) AS order_count

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id

JOIN customer_segments AS cs
    ON o.customer_id = cs.customer_id

JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id

GROUP BY
    p.category,
    cs.customer_segment

ORDER BY total_revenue DESC;


-- 10.2 Region × category
SELECT
    l.region,
    p.category,

    ROUND(SUM(oi.revenue), 2) AS total_revenue,

    ROUND(SUM(oi.profit), 2) AS total_profit,

    COUNT(DISTINCT o.order_id) AS order_count

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        location_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id

JOIN 'data/raw/locations.csv' AS l
    ON o.location_id = l.location_id

JOIN 'data/raw/products.csv' AS p
    ON oi.product_id = p.product_id

GROUP BY
    l.region,
    p.category

ORDER BY
    l.region,
    total_revenue DESC;


-- ============================================================
-- 11. FINAL KPI RECONCILIATION
-- ============================================================

SELECT
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit,

    COUNT(DISTINCT o.order_id) AS total_orders,

    COUNT(DISTINCT o.customer_id) AS ordering_customers,

    ROUND(
        SUM(oi.revenue) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM 'data/raw/order_items.csv' AS oi

JOIN (
    SELECT DISTINCT
        order_id,
        customer_id
    FROM 'data/raw/orders.csv'
) AS o
    ON oi.order_id = o.order_id;