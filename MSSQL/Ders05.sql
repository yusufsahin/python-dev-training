SELECT   Categories.CategoryName, Products.ProductName
FROM         Categories INNER JOIN
                         Products ON Categories.CategoryID = Products.CategoryID

SELECT   Customers.CustomerID, Customers.CompanyName, Orders.OrderID, Orders.OrderDate
FROM         Customers INNER JOIN
Orders ON Customers.CustomerID = Orders.CustomerID


SELECT Customers.CustomerID, Customers.CompanyName, Orders.OrderID, Orders.OrderDate
FROM Customers
INNER JOIN Orders
    ON Orders.CustomerID = Customers.CustomerID;


SELECT       Customers.CustomerID, Customers.CompanyName, Orders.OrderID, Orders.OrderDate
FROM         Customers LEFT JOIN
                         Orders ON Customers.CustomerID = Orders.CustomerID

SELECT Customers.CustomerID, Customers.CompanyName, Orders.OrderID, Orders.OrderDate
FROM Customers
LEFT JOIN Orders
    ON Orders.CustomerID = Customers.CustomerID;

SELECT Customers.CustomerID,
       Customers.CompanyName,
       Orders.OrderID,
       Orders.OrderDate
FROM Customers
RIGHT JOIN Orders
    ON Customers.CustomerID = Orders.CustomerID;

SELECT Customers.CustomerID,
       Customers.CompanyName,
       Orders.OrderID,
       Orders.OrderDate
FROM Customers
RIGHT JOIN Orders
    ON Orders.CustomerID = Customers.CustomerID;

--INNER JOIN → sadece eşleşenler
--LEFT JOIN → sol tablonun hepsi
--RIGHT JOIN → sağ tablonun hepsi


--En az 1 sipariş veren müşteriler

SELECT c.CustomerID, c.CompanyName
FROM dbo.Customers AS c
WHERE EXISTS (
    SELECT 1
    FROM dbo.Orders AS o
    WHERE o.CustomerID = c.CustomerID
);

--Hiç sipariş vermemiş müşteriler
SELECT c.CustomerID, c.CompanyName
FROM dbo.Customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.Orders AS o
    WHERE o.CustomerID = c.CustomerID
);

SELECT DISTINCT c.CustomerID, c.CompanyName
FROM dbo.Customers c
INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
INNER JOIN dbo.[Order Details] od ON o.OrderID = od.OrderID
INNER JOIN dbo.Products p ON od.ProductID = p.ProductID
INNER JOIN dbo.Categories cat ON p.CategoryID = cat.CategoryID
WHERE cat.CategoryName = 'Beverages'

SELECT c.CustomerID, c.CompanyName
FROM Customers c
WHERE EXISTS (
    SELECT 1
    FROM Orders o
    JOIN [Order Details] od ON od.OrderID = o.OrderID
    JOIN Products p ON p.ProductID = od.ProductID
    JOIN Categories cat ON cat.CategoryID = p.CategoryID
    WHERE o.CustomerID = c.CustomerID
      AND cat.CategoryName = 'Beverages'
);

-- Created by GitHub Copilot in SSMS - review carefully before executing
SELECT p.ProductID, p.ProductName, p.SupplierID, p.CategoryID
FROM dbo.Products AS p
LEFT JOIN dbo.[Order Details] AS od
    ON od.ProductID = p.ProductID
WHERE od.ProductID IS NULL;

SELECT e.EmployeeID, e.FirstName, e.LastName
FROM Employees e
WHERE EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.EmployeeID = e.EmployeeID
      AND o.ShippedDate > o.RequiredDate
);


SELECT p.ProductID, p.ProductName, p.UnitPrice
FROM Products p
WHERE p.UnitPrice > ANY (
    SELECT p2.UnitPrice
    FROM Products p2
    WHERE p2.CategoryID = 1
);

SELECT p.ProductID, p.ProductName, p.UnitPrice
FROM Products p
WHERE p.UnitPrice > ALL (
    SELECT p2.UnitPrice
    FROM Products p2
    WHERE p2.CategoryID = 1
);

SELECT p.ProductID, p.ProductName, p.UnitPrice
FROM Products p
WHERE p.UnitPrice > (
    SELECT MAX(p2.UnitPrice)
    FROM Products p2
    WHERE p2.CategoryID = 1
);

SELECT o.OrderID, o.CustomerID, o.Freight
FROM Orders o
WHERE o.Freight > ANY (
    SELECT o2.Freight
    FROM Orders o2
    WHERE o2.ShipVia = 1
);

SELECT o.OrderID, o.CustomerID, o.Freight
FROM Orders o
WHERE o.Freight > ALL (
    SELECT o2.Freight
    FROM Orders o2
    WHERE o2.ShipVia = 1
);


--ANY aslında çoğu zaman IN gibi davranır
SELECT p.ProductID, p.ProductName, p.SupplierID
FROM Products p
WHERE p.SupplierID = ANY (
    SELECT s.SupplierID
    FROM Suppliers s
    WHERE s.Country = 'USA'
);

SELECT p.ProductID, p.ProductName, p.SupplierID
FROM Products p
WHERE p.SupplierID IN (
    SELECT s.SupplierID
    FROM Suppliers s
    WHERE s.Country = 'USA'
);

--Her müşterinin sipariş sayısı
SELECT c.CustomerID,
       c.CompanyName,
       COUNT(o.OrderID) AS OrderCount
FROM Customers c
LEFT JOIN Orders o
    ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.CompanyName
ORDER BY OrderCount DESC, c.CompanyName ASC;

--10 dan sipariş veren müşteriler

SELECT   Customers.CustomerID, Customers.CompanyName, COUNT(Orders.OrderID) as OrderCount
FROM         Customers INNER JOIN
Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CustomerID, Customers.CompanyName
HAVING  COUNT(Orders.OrderID) >10
ORDER BY OrderCount DESC;

-- Created by GitHub Copilot in SSMS - review carefully before executing
SELECT c.CustomerID,
       c.CompanyName,
       SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalRevenue
FROM dbo.Customers c
LEFT JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN dbo.[Order Details] od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.CompanyName
ORDER BY TotalRevenue DESC;

SELECT 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalRevenue
FROM Customers c
JOIN Orders o
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate)
ORDER BY 
    c.CompanyName,
    SalesYear;

WITH Years AS (
    SELECT DISTINCT YEAR(OrderDate) AS SalesYear
    FROM Orders
)
SELECT 
    c.CustomerID,
    c.CompanyName,
    y.SalesYear,
    ISNULL(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 0) AS TotalRevenue
FROM Customers c
CROSS JOIN Years y
LEFT JOIN Orders o
    ON o.CustomerID = c.CustomerID
   AND YEAR(o.OrderDate) = y.SalesYear
LEFT JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY 
    c.CustomerID,
    c.CompanyName,
    y.SalesYear
ORDER BY 
    c.CompanyName,
    y.SalesYear;


SELECT *
FROM
(
    SELECT 
        c.CustomerID,
        c.CompanyName,
        YEAR(o.OrderDate) AS SalesYear,
        od.UnitPrice * od.Quantity * (1 - od.Discount) AS LineRevenue
    FROM Customers c
    JOIN Orders o
        ON o.CustomerID = c.CustomerID
    JOIN [Order Details] od
        ON od.OrderID = o.OrderID
) src
PIVOT
(
    SUM(LineRevenue)
    FOR SalesYear IN ([1996], [1997], [1998],[1999])
) p
ORDER BY CompanyName;

SELECT 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalRevenue
FROM Customers c
JOIN Orders o
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate)
ORDER BY 
    c.CompanyName,
    SalesYear;
SELECT 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalRevenue
FROM Customers c
JOIN Orders o
    ON o.CustomerID = c.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
WHERE c.CustomerID = 'ALFKI'
GROUP BY 
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate)
ORDER BY 
    SalesYear;

SELECT TOP 1 WITH TIES
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
FROM Employees e
JOIN Orders o
    ON o.EmployeeID = e.EmployeeID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    e.EmployeeID,
    e.FirstName,
    e.LastName
ORDER BY
    TotalSales DESC;

SELECT TOP 1
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    COUNT(DISTINCT o.OrderID) AS OrderCount
FROM Employees e
JOIN Orders o
    ON o.EmployeeID = e.EmployeeID
GROUP BY
    e.EmployeeID,
    e.FirstName,
    e.LastName
ORDER BY
    OrderCount DESC;

    --hangi çalışan, hangi müşteriye ne kadar satış yapmış

SELECT
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
FROM Employees e
JOIN Orders o
    ON o.EmployeeID = e.EmployeeID
JOIN Customers c
    ON c.CustomerID = o.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName
ORDER BY
    e.LastName,
    e.FirstName,
    TotalSales DESC;

SELECT
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
FROM Employees e
JOIN Orders o
    ON o.EmployeeID = e.EmployeeID
JOIN Customers c
    ON c.CustomerID = o.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName
ORDER BY
    TotalSales DESC;

SELECT
    YEAR(o.OrderDate) AS SalesYear,
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
FROM Employees e
JOIN Orders o
    ON o.EmployeeID = e.EmployeeID
JOIN Customers c
    ON c.CustomerID = o.CustomerID
JOIN [Order Details] od
    ON od.OrderID = o.OrderID
GROUP BY
    YEAR(o.OrderDate),
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    c.CustomerID,
    c.CompanyName
ORDER BY
    SalesYear,
    e.LastName,
    e.FirstName,
    TotalSales DESC;


WITH YearlySales AS
(
    SELECT
        YEAR(o.OrderDate) AS SalesYear,
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName,
        COUNT(DISTINCT o.OrderID) AS OrderCount,
        CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
    FROM Employees e
    JOIN Orders o
        ON o.EmployeeID = e.EmployeeID
    JOIN Customers c
        ON c.CustomerID = o.CustomerID
    JOIN [Order Details] od
        ON od.OrderID = o.OrderID
    GROUP BY
        YEAR(o.OrderDate),
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName
)
SELECT
    SalesYear,
    EmployeeID,
    FirstName,
    LastName,
    CustomerID,
    CompanyName,
    OrderCount,
    TotalSales,
    LAG(TotalSales) OVER
    (
        PARTITION BY EmployeeID, CustomerID
        ORDER BY SalesYear
    ) AS PreviousYearSales,
    CAST(
        CASE
            WHEN LAG(TotalSales) OVER
                 (
                     PARTITION BY EmployeeID, CustomerID
                     ORDER BY SalesYear
                 ) IS NULL THEN NULL
            WHEN LAG(TotalSales) OVER
                 (
                     PARTITION BY EmployeeID, CustomerID
                     ORDER BY SalesYear
                 ) = 0 THEN NULL
            ELSE
                (
                    (TotalSales - LAG(TotalSales) OVER
                        (
                            PARTITION BY EmployeeID, CustomerID
                            ORDER BY SalesYear
                        )
                    )
                    * 100.0
                )
                / LAG(TotalSales) OVER
                    (
                        PARTITION BY EmployeeID, CustomerID
                        ORDER BY SalesYear
                    )
        END
        AS DECIMAL(18,2)
    ) AS GrowthPercent
FROM YearlySales
ORDER BY
    SalesYear,
    LastName,
    FirstName,
    TotalSales DESC;


    WITH YearlySales AS
(
    SELECT
        YEAR(o.OrderDate) AS SalesYear,
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName,
        COUNT(DISTINCT o.OrderID) AS OrderCount,
        CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
    FROM Employees e
    JOIN Orders o
        ON o.EmployeeID = e.EmployeeID
    JOIN Customers c
        ON c.CustomerID = o.CustomerID
    JOIN [Order Details] od
        ON od.OrderID = o.OrderID
    GROUP BY
        YEAR(o.OrderDate),
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName
),
SalesWithPrev AS
(
    SELECT
        SalesYear,
        EmployeeID,
        FirstName,
        LastName,
        CustomerID,
        CompanyName,
        OrderCount,
        TotalSales,
        LAG(TotalSales) OVER
        (
            PARTITION BY EmployeeID, CustomerID
            ORDER BY SalesYear
        ) AS PreviousYearSales
    FROM YearlySales
)
SELECT
    SalesYear,
    EmployeeID,
    FirstName,
    LastName,
    CustomerID,
    CompanyName,
    OrderCount,
    TotalSales,
    PreviousYearSales,
    CAST(
        CASE
            WHEN PreviousYearSales IS NULL OR PreviousYearSales = 0 THEN NULL
            ELSE ((TotalSales - PreviousYearSales) * 100.0) / PreviousYearSales
        END
        AS DECIMAL(18,2)
    ) AS GrowthPercent
FROM SalesWithPrev
ORDER BY
    SalesYear,
    LastName,
    FirstName,
    TotalSales DESC;


    WITH YearlySales AS
(
    SELECT
        YEAR(o.OrderDate) AS SalesYear,
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName,
        COUNT(DISTINCT o.OrderID) AS OrderCount,
        CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
    FROM Employees e
    JOIN Orders o
        ON o.EmployeeID = e.EmployeeID
    JOIN Customers c
        ON c.CustomerID = o.CustomerID
    JOIN [Order Details] od
        ON od.OrderID = o.OrderID
    GROUP BY
        YEAR(o.OrderDate),
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName
),
SalesWithPrev AS
(
    SELECT
        SalesYear,
        EmployeeID,
        FirstName,
        LastName,
        CustomerID,
        CompanyName,
        OrderCount,
        TotalSales,
        LAG(TotalSales) OVER
        (
            PARTITION BY EmployeeID, CustomerID
            ORDER BY SalesYear
        ) AS PreviousYearSales
    FROM YearlySales
)
SELECT
    SalesYear,
    EmployeeID,
    FirstName,
    LastName,
    CustomerID,
    CompanyName,
    OrderCount,
    TotalSales,
    PreviousYearSales,
    CAST(
        CASE
            WHEN PreviousYearSales IS NULL OR PreviousYearSales = 0 THEN NULL
            ELSE ((TotalSales - PreviousYearSales) * 100.0) / PreviousYearSales
        END
        AS DECIMAL(18,2)
    ) AS GrowthPercent,
    CASE
        WHEN PreviousYearSales IS NULL THEN 'İlk Yıl / Karşılaştırma Yok'
        WHEN PreviousYearSales = 0 AND TotalSales > 0 THEN 'Yeni Satış'
        WHEN TotalSales > PreviousYearSales THEN 'Artış'
        WHEN TotalSales < PreviousYearSales THEN 'Azalış'
        ELSE 'Değişmedi'
    END AS TrendText,
    CASE
        WHEN PreviousYearSales IS NULL THEN '-'
        WHEN PreviousYearSales = 0 AND TotalSales > 0 THEN '↑'
        WHEN TotalSales > PreviousYearSales THEN '↑'
        WHEN TotalSales < PreviousYearSales THEN '↓'
        ELSE '→'
    END AS TrendArrow
FROM SalesWithPrev
ORDER BY
    SalesYear,
    LastName,
    FirstName,
    TotalSales DESC;

    --

    --

    WITH YearlySales AS
(
    SELECT
        YEAR(o.OrderDate) AS SalesYear,
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName,
        COUNT(DISTINCT o.OrderID) AS OrderCount,
        CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(18,2)) AS TotalSales
    FROM Employees e
    JOIN Orders o
        ON o.EmployeeID = e.EmployeeID
    JOIN Customers c
        ON c.CustomerID = o.CustomerID
    JOIN [Order Details] od
        ON od.OrderID = o.OrderID
    GROUP BY
        YEAR(o.OrderDate),
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        c.CustomerID,
        c.CompanyName
),
SalesWithPrev AS
(
    SELECT
        SalesYear,
        EmployeeID,
        FirstName,
        LastName,
        CustomerID,
        CompanyName,
        OrderCount,
        TotalSales,
        LAG(TotalSales) OVER
        (
            PARTITION BY EmployeeID, CustomerID
            ORDER BY SalesYear
        ) AS PreviousYearSales
    FROM YearlySales
),
FinalData AS
(
    SELECT
        SalesYear,
        EmployeeID,
        FirstName,
        LastName,
        CustomerID,
        CompanyName,
        OrderCount,
        TotalSales,
        PreviousYearSales,
        CAST(
            CASE
                WHEN PreviousYearSales IS NULL OR PreviousYearSales = 0 THEN NULL
                ELSE ((TotalSales - PreviousYearSales) * 100.0) / PreviousYearSales
            END
            AS DECIMAL(18,2)
        ) AS GrowthPercent
    FROM SalesWithPrev
)
SELECT TOP 10 *
FROM FinalData
WHERE GrowthPercent IS NOT NULL
ORDER BY GrowthPercent DESC;



---
SELECT TOP (1000) [OrderID]
      ,[ProductID]
      ,[ProductName]
      ,[UnitPrice]
      ,[Quantity]
      ,[Discount]
      ,[ExtendedPrice]
  FROM [northwind].[dbo].[Order Details Extended]
--VIEW OLUŞTURMA
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

CREATE VIEW vw_CustomerMonthlyRevenueByMounthName
AS
SELECT
    c.CustomerID,
    c.CompanyName,
    YEAR(o.OrderDate) AS SalesYear,
    MONTH(o.OrderDate) AS SalesMonth,
    DATENAME(MONTH, o.OrderDate) AS SalesMonthName,
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
    MONTH(o.OrderDate),
    DATENAME(MONTH, o.OrderDate);

    select * from vw_CustomerMonthlyRevenueByMounthName

    --view ile aylık ciro datasını hazırlarsın
    --stored procedure ile “hangi müşteri?”, “hangi yıl?” gibi filtrelerle
    
    --Örnek belirli bir müşteri için aylık ciro getiren stored procedure

CREATE PROCEDURE sp_GetCustomerMonthlyRevenue
@CustomerID NCHAR(5) = NULL,
 @SalesYear INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        CustomerID,
        CompanyName,
        SalesYear,
        SalesMonth,
        OrderCount,
        TotalRevenue
    FROM vw_CustomerMonthlyRevenue
    WHERE (@CustomerID IS NULL OR CustomerID = @CustomerID)
      AND (@SalesYear IS NULL OR SalesYear = @SalesYear)
    ORDER BY
        CompanyName,
        SalesYear,
        SalesMonth;
END;

EXEC sp_GetCustomerMonthlyRevenue;

EXEC sp_GetCustomerMonthlyRevenue @CustomerID = 'ALFKI';

EXEC sp_GetCustomerMonthlyRevenue @SalesYear = 1997;

EXEC sp_GetCustomerMonthlyRevenue @CustomerID = 'ALFKI', @SalesYear = 1997;

---Bir tabloda INSERT, UPDATE, DELETE olduğunda otomatik çalışan SQL kodudur.

--Yani:

--kayıt eklenince
--kayıt güncellenince
--kayıt silinince
--kendiliğinden çalışır.
--1) Örnek: Ürün fiyatı

CREATE TABLE ProductPriceAudit
(
    AuditID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT,
    ProductName NVARCHAR(100),
    OldPrice DECIMAL(18,2),
    NewPrice DECIMAL(18,2),
    ChangedDate DATETIME DEFAULT GETDATE()
);
--Örnek: Ürün fiyatı değişince log tut
CREATE TRIGGER trg_ProductPriceUpdate
ON Products
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO ProductPriceAudit
    (
        ProductID,
        ProductName,
        OldPrice,
        NewPrice,
        ChangedDate
    )
    SELECT
        i.ProductID,
        i.ProductName,
        d.UnitPrice AS OldPrice,
        i.UnitPrice AS NewPrice,
        GETDATE()
    FROM inserted i
    INNER JOIN deleted d
        ON i.ProductID = d.ProductID
    WHERE ISNULL(i.UnitPrice, 0) <> ISNULL(d.UnitPrice, 0);
END;

UPDATE Products
SET UnitPrice = UnitPrice * 1.15
WHERE ProductID = 1;

SELECT * FROM ProductPriceAudit;

---Sipariş olan müşteriler silimesin
CREATE TRIGGER trg_PreventCustomerDelete
ON Customers
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS
    (
        SELECT 1
        FROM Orders o
        INNER JOIN deleted d
            ON o.CustomerID = d.CustomerID
    )
    BEGIN
        RAISERROR('Siparişi olan müşteri silinemez.', 16, 1);
        RETURN;
    END

    DELETE FROM Customers
    WHERE CustomerID IN (SELECT CustomerID FROM deleted);
END;


DELETE FROM Customers
WHERE CustomerID = 'ALFKI';

SELECT * FROM Customers
WHERE CustomerID = 'ALFKI';

-- Sipariş toplamı otomatik hesaplasın

--yeni ordertotal kolonu ekleyelim

ALTER TABLE Orders
ADD OrderTotal DECIMAL(18,2) NULL;


CREATE OR ALTER TRIGGER trg_UpdateOrderTotal_OnOrderDetails
ON [Order Details]
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH ChangedOrders AS
    (
        SELECT OrderID FROM inserted
        UNION
        SELECT OrderID FROM deleted
    ),
    OrderTotals AS
    (
        SELECT
            co.OrderID,
            CAST(ISNULL(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 0) AS DECIMAL(18,2)) AS NewTotal
        FROM ChangedOrders co
        LEFT JOIN [Order Details] od
            ON od.OrderID = co.OrderID
        GROUP BY co.OrderID
    )
    UPDATE o
    SET o.OrderTotal = ot.NewTotal
    FROM Orders o
    JOIN OrderTotals ot
        ON ot.OrderID = o.OrderID;
END;


UPDATE [Order Details]
SET Quantity = Quantity + 2
WHERE OrderID = 10248
  AND ProductID = 11;

  SELECT OrderID, OrderTotal FROM Orders --WHERE OrderID = 10248;

  --Cursor sorgudan satırları tek tek çekip işlem yapmaya yarar. 
  --Genelde önerilmez, performans sorunlarına yol açabilir.

  --Sipariş toplamlarını tek tek güncelleyelim cursor ile

DECLARE @OrderID INT

DECLARE order_cursor CURSOR FOR
SELECT OrderID
FROM Orders

OPEN order_cursor

FETCH NEXT FROM order_cursor INTO @OrderID

WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE Orders
    SET OrderTotal =
    (
        SELECT ISNULL(SUM(UnitPrice * Quantity * (1 - Discount)), 0)
        FROM [Order Details]
        WHERE [Order Details].OrderID = Orders.OrderID
    )
    WHERE OrderID = @OrderID

    FETCH NEXT FROM order_cursor INTO @OrderID
END

CLOSE order_cursor
DEALLOCATE order_cursor

SELECT OrderID, OrderTotal FROM Orders

UPDATE o
SET o.OrderTotal = x.TotalAmount
FROM Orders o
OUTER APPLY
(
    SELECT ISNULL(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 0) AS TotalAmount
    FROM [Order Details] od
    WHERE od.OrderID = o.OrderID
) x;

---

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