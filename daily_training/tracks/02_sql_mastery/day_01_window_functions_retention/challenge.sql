-- Reto SQL: MoM Growth con Window Functions
WITH monthly_lag AS (
    SELECT
        month_date,
        product_category,
        revenue,
        LAG(revenue, 1) OVER (
            PARTITION BY product_category 
            ORDER BY month_date
        ) AS prev_month_revenue
    FROM monthly_revenue
)
SELECT
    month_date,
    product_category,
    revenue,
    prev_month_revenue,
    ROUND(((revenue - prev_month_revenue) / prev_month_revenue) * 100.0, 2) AS mom_growth_pct
FROM monthly_lag
ORDER BY product_category, month_date;

