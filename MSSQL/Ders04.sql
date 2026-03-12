USE [northwind]
GO

INSERT INTO [dbo].[Customers]
           ([CustomerID]
           ,[CompanyName]
           ,[ContactName]
           ,[ContactTitle]
           ,[Address]
           ,[City]
           ,[Region]
           ,[PostalCode]
           ,[Country]
           ,[Phone]
           ,[Fax])
     VALUES
           (<CustomerID, nchar(5),>
           ,<CompanyName, nvarchar(40),>
           ,<ContactName, nvarchar(30),>
           ,<ContactTitle, nvarchar(30),>
           ,<Address, nvarchar(60),>
           ,<City, nvarchar(15),>
           ,<Region, nvarchar(15),>
           ,<PostalCode, nvarchar(10),>
           ,<Country, nvarchar(15),>
           ,<Phone, nvarchar(24),>
           ,<Fax, nvarchar(24),>)
GO


SELECT 
    e.EmployeeID,
    e.FirstName + ' ' + e.LastName AS EmployeeName,
    m.EmployeeID AS ManagerID,
    m.FirstName + ' ' + m.LastName AS ManagerName
FROM Employees e
LEFT JOIN Employees m
    ON e.ReportsTo = m.EmployeeID;

SELECT 
    e.FirstName AS EmployeeFirstName,
    e.LastName  AS EmployeeLastName,
    m.FirstName AS ManagerFirstName,
    m.LastName  AS ManagerLastName
FROM Employees e
LEFT JOIN Employees m
    ON e.ReportsTo = m.EmployeeID;


SELECT 
    e.EmployeeID,
    e.FirstName + ' ' + e.LastName AS EmployeeName,
    m.FirstName + ' ' + m.LastName AS ManagerName
FROM Employees e
INNER JOIN Employees m
    ON e.ReportsTo = m.EmployeeID;

SELECT 
    p.ProductName,
    c.CategoryName
FROM Products p
CROSS JOIN Categories c;

SELECT 
    c.CustomerID,
    c.CompanyName,
    o.OrderID
FROM Customers c
LEFT JOIN Orders o
    ON c.CustomerID = o.CustomerID;


SELECT 
    c.CustomerID,
    c.CompanyName,
    o.OrderID
FROM Customers c
RIGHT JOIN Orders o
    ON c.CustomerID = o.CustomerID;


SELECT 
    c.CustomerID,
    c.CompanyName,
    o.OrderID
FROM Customers c
FULL OUTER JOIN Orders o
    ON c.CustomerID = o.CustomerID;



SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (
    SELECT AVG(UnitPrice)
    FROM Products
);


SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (
    SELECT MIN(UnitPrice)
    FROM Products
);

SELECT 
    c.CustomerID,
    c.CompanyName,
    (
        SELECT COUNT(*)
        FROM Orders o
        WHERE o.CustomerID = c.CustomerID
    ) AS OrderCount
FROM Customers c;

WITH ExpensiveProducts AS
(
    SELECT ProductID, ProductName, UnitPrice
    FROM Products
    WHERE UnitPrice > 50
)
SELECT *
FROM ExpensiveProducts;

SELECT 
    ProductName,
    UnitPrice,
    ROW_NUMBER() OVER (ORDER BY UnitPrice DESC) AS RowNum
FROM Products;

SELECT 
    ProductName,
    UnitPrice,
    RANK() OVER (ORDER BY UnitPrice DESC) AS PriceRank
FROM Products;

SELECT
    ProductName,
    CategoryID,
    UnitPrice,
    ROW_NUMBER() OVER (
        PARTITION BY CategoryID
        ORDER BY UnitPrice DESC
    ) AS RowInCategory
FROM Products;