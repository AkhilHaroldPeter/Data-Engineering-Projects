SELECT 
    card_type, 
    MAX(amount) AS highest_spend_amount, 
    MIN(amount) AS lowest_spend_amount
FROM 
    transactions
GROUP BY 
    card_type;