CREATE VIEW vw_CustomerYearlyRevenue
AS
SELECT
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalRevenue
FROM Customers c
JOIN Orders o
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate);

CREATE VIEW vw_CustomerMonthlyRevenue
AS
SELECT
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    MONTH(o.OrderDate) AS SalesMonth,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalRevenue
FROM Customers c
JOIN Orders o
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate),
    MONTH(o.OrderDate);

SELECT * FROM vw_CustomerMonthlyRevenue;