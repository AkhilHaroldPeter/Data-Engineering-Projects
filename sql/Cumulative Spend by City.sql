WITH CumulativeSpending AS (
    SELECT 
        city,
        transaction_date,
        SUM(amount) OVER (PARTITION BY city ORDER BY transaction_date) AS cumulative_spend
    FROM 
        transactions
)
SELECT 
    city,
    MIN(transaction_date) AS first_date_to_reach_500k
FROM 
    CumulativeSpending
WHERE 
    cumulative_spend >= 500000
GROUP BY 
    city;
