SELECT 
    city,
    gender,
    SUM(amount) AS total_spend
FROM 
    transactions
GROUP BY 
    city, 
    gender
ORDER BY 
    city, 
    total_spend DESC;
