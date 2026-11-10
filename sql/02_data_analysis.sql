
-- 1. Monthly number of orders
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month_year,
    COUNT(order_id) AS orders_per_month
FROM orders
GROUP BY month_year
ORDER BY month_year;


-- 2. Monthly payment totals
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month_year,
    ROUND(SUM(p.payment_value), 2) AS payments_per_month
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY month_year
ORDER BY month_year;


-- 3. Average payment per order by month
SELECT
    month_year,
    ROUND(AVG(payment_per_order), 2) AS avg_payment_per_order
FROM (
    SELECT
        o.order_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month_year,
        SUM(p.payment_value) AS payment_per_order
    FROM orders o
    JOIN order_payments p
        ON o.order_id = p.order_id
    GROUP BY o.order_id, month_year
) AS monthly_orders
GROUP BY month_year
ORDER BY month_year;


