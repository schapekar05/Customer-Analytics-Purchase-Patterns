-- Customer Analytics & Purchase Pattern Analysis
-- SQL dialect: PostgreSQL. Import data/transactions.csv as public.transactions.

-- 1. Executive KPIs
SELECT
    COUNT(*) FILTER (WHERE order_status = 'Delivered') AS delivered_orders,
    COUNT(DISTINCT customer_id) FILTER (WHERE order_status = 'Delivered') AS purchasing_customers,
    ROUND(SUM(net_revenue)::numeric, 2) AS net_revenue,
    ROUND(
      SUM(net_revenue)::numeric /
      NULLIF(COUNT(*) FILTER (WHERE order_status = 'Delivered'), 0), 2
    ) AS aov_per_delivered_order
FROM transactions;

-- 2. Monthly revenue trend
SELECT DATE_TRUNC('month', order_date::date)::date AS month,
       COUNT(*) FILTER (WHERE order_status='Delivered') AS delivered_orders,
       ROUND(SUM(net_revenue)::numeric,2) AS net_revenue
FROM transactions
GROUP BY 1 ORDER BY 1;

-- 3. Category contribution
SELECT category, ROUND(SUM(net_revenue)::numeric,2) AS net_revenue,
       ROUND(100.0*SUM(net_revenue)/NULLIF(SUM(SUM(net_revenue)) OVER (),0),2) AS revenue_share_pct
FROM transactions
GROUP BY category ORDER BY net_revenue DESC;

-- 4. Product performance
SELECT category, product_name, SUM(quantity) AS units_sold,
       ROUND(SUM(net_revenue)::numeric,2) AS net_revenue
FROM transactions
GROUP BY category, product_name
ORDER BY net_revenue DESC;

-- 5. Repeat purchase analysis (delivered orders only)
WITH customer_orders AS (
  SELECT customer_id, COUNT(*) AS delivered_order_count,
         SUM(net_revenue) AS customer_revenue
  FROM transactions
  WHERE order_status='Delivered'
  GROUP BY customer_id
)
SELECT
  COUNT(*) AS customers,
  COUNT(*) FILTER (WHERE delivered_order_count > 1) AS repeat_customers,
  ROUND(100.0*COUNT(*) FILTER (WHERE delivered_order_count > 1)/NULLIF(COUNT(*),0),2) AS repeat_customer_pct,
  ROUND(AVG(customer_revenue)::numeric,2) AS avg_revenue_per_customer
FROM customer_orders;

-- 6. RFM base table
SELECT customer_id,
       MAX(order_date::date) AS last_purchase_date,
       COUNT(*) AS frequency,
       ROUND(SUM(net_revenue)::numeric,2) AS monetary
FROM transactions
WHERE order_status='Delivered'
GROUP BY customer_id;
