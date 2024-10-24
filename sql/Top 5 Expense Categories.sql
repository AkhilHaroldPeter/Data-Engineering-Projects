
SELECT top 5
    exp_type, 
    SUM(amount) AS total_spend,
    (SUM(amount) * 100.0 / (SELECT SUM(amount) FROM DEProject.dbo.transactions)) AS percentage_contribution
FROM 
    [transactions]
GROUP BY 
    exp_type
ORDER BY 
    total_spend DESC;