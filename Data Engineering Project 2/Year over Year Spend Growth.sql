WITH YearlySpend AS (
    SELECT 
        city,
        card_type,
        YEAR(transaction_date) AS year,
        SUM(amount) AS total_spend
    FROM 
        transactions
    WHERE 
        YEAR(transaction_date) IN (2013, 2014)
    GROUP BY 
        city, 
        card_type, 
        YEAR(transaction_date)
)
SELECT 
    y2014.city,
    y2014.card_type,
    (y2014.total_spend - COALESCE(y2013.total_spend, 0)) AS growth
FROM 
    YearlySpend y2014
LEFT JOIN 
    YearlySpend y2013 
ON 
    y2014.city = y2013.city 
    AND y2014.card_type = y2013.card_type 
    AND y2013.year = 2013
WHERE 
    y2014.year = 2014
ORDER BY 
    growth DESC
OFFSET 0 ROWS FETCH NEXT 1 ROW ONLY; -- SQL Server syntax for LIMIT
