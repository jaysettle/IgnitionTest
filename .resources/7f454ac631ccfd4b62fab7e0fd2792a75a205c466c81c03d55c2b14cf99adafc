SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(oi.Quantity * oi.UnitPrice) AS TotalAmountSpent,
    AVG(DATEDIFF(DAY, o.OrderDate, ISNULL(pmt.PaymentDate, GETDATE()))) AS AvgDaysToPayment,
    MAX(pmt.Amount) AS LargestPayment
FROM 
    Customers c
INNER JOIN 
    Orders o ON c.CustomerID = o.CustomerID
INNER JOIN 
    OrderItems oi ON o.OrderID = oi.OrderID
INNER JOIN 
    Products p ON oi.ProductID = p.ProductID
LEFT JOIN 
    Payments pmt ON o.OrderID = pmt.OrderID
WHERE 
    o.Status = 'Completed'
    AND p.Price > 100  -- Filters products priced above 100
    AND c.FirstName LIKE '%a%'  -- Filters customers with 'a' in their first name
GROUP BY 
    c.CustomerID, c.FirstName, c.LastName
HAVING 
    SUM(oi.Quantity * oi.UnitPrice) > 500  -- Only show customers who spent more than 500
ORDER BY 
    TotalAmountSpent DESC, AvgDaysToPayment ASC;
