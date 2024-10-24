SELECT 
    card_type, 
    YEAR(transaction_date) AS transaction_year,
    MONTH(transaction_date) AS transaction_month,
    AVG(amount) AS average_spend_per_transaction
FROM 
    transactions
GROUP BY 
    card_type, 
    YEAR(transaction_date),
    MONTH(transaction_date);