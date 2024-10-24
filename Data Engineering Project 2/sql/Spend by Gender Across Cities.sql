SELECT 
    city,
    gender,
    SUM(amount) AS total_spend,
    (SUM(amount) * 100.0 / (SELECT SUM(amount) FROM transactions WHERE city = ct.city)) AS percentage_contribution
FROM 
    transactions ct
GROUP BY 
    city, 
    gender;