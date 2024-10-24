SELECT 
    city,
    CASE 
        WHEN DATEPART(WEEKDAY, transaction_date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday' 
    END AS day_type,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_spend
FROM 
    transactions
GROUP BY 
    city, 
    CASE 
        WHEN DATEPART(WEEKDAY, transaction_date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday' 
    END;
