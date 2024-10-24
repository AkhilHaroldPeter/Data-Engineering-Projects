SELECT 
    age_group, 
    card_type, 
    SUM(amount) AS total_spend
FROM 
    credit_card_transactions
GROUP BY 
    age_group, 
    card_type
ORDER BY 
    total_spend DESC;
