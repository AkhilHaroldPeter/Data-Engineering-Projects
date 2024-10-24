WITH TransactionCounts AS (
    SELECT 
        card_type,
        COUNT(*) AS transaction_count,
        SUM(amount) AS total_spend
    FROM 
        transactions
    GROUP BY 
        card_type
)
SELECT TOP 1 
    card_type,
    transaction_count,
    total_spend,
    (total_spend * 1.0 / transaction_count) AS average_spend_per_transaction
FROM 
    TransactionCounts
ORDER BY 
    average_spend_per_transaction DESC;
