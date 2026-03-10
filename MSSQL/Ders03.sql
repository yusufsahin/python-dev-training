USE northwind;
GO
--SELECT 
SELECT * FROM Categories;

SELECT Categories.CategoryID, Categories.CategoryName FROM Categories;

SELECT c.CategoryID, c.CategoryName FROM Categories as c;

SELECT CategoryID,CategoryName FROM Categories;

--INSERT 

INSERT INTO Categories(CategoryName,Description)
VALUES ('Beverages 2','Soft drinks , coffies , teas ...');

SELECT * FROM Customers;

INSERT INTO Customers(CustomerID,CompanyName,ContactName,City,Country)
VALUES ('ACMEC','Acme Limited Sirketi','Bugs Bunny','Istanbul','Turkiye');

SELECT * FROM Customers WHERE CustomerID='ACMEC';

INSERT INTO Customers(CustomerID,CompanyName,ContactName,City,Country)
VALUES ('ACMEO','Acme Oil Limited Sirketi','Sylvester','Istanbul','Turkiye');

SELECT * FROM Customers WHERE CustomerID='ACMEO';

INSERT INTO Customers(CompanyName,ContactName,City,Country)
VALUES ('Acme Havacilik Limited Sirketi','Twety','Istanbul','Turkiye');

--Msg 515, Level 16, State 2, Line 29
--Cannot insert the value NULL into column 'CustomerID', table 'northwind.dbo.Customers'; column does not allow nulls. INSERT fails.

INSERT INTO Customers(CustomerID,CompanyName,ContactName,City,Country)
VALUES ('ACMEO','Acme Oil Limited Sirketi','Sylvester','Istanbul','Turkiye');
--unique olmalı 2 . ACMEO yu kabul etmez
--Msg 2627, Level 14, State 1, Line 35
--Violation of PRIMARY KEY constraint 'PK_Customers'. Cannot insert duplicate key in object 'dbo.Customers'. The duplicate key value is (ACMEO).
--The statement has been terminated.
--Completion time: 2026-03-10T20:53:58.4659243+03:00

--UPDATE
SELECT * FROM Customers WHERE CustomerID='ACMEO';

UPDATE Customers SET City='Ankara' WHERE CustomerID='ACMEO';

SELECT * FROM Customers WHERE CustomerID='ACMEO';

UPDATE Customers SET ContactName='Coyote',City='Istanbul' WHERE CustomerID='ACMEO';

SELECT * FROM Customers WHERE CustomerID='ACMEO';

SELECT * FROM Products;

UPDATE Products SET UnitPrice=UnitPrice * 1.10 WHERE ProductID=1

SELECT * FROM Products WHERE CategoryID=3;

UPDATE Products SET UnitPrice=UnitPrice * 1.15 WHERE  CategoryID=3;
SELECT * FROM Products WHERE CategoryID=3;


--DELETE 

SELECT * FROM Customers;

DELETE FROM Customers WHERE CustomerID='ACMEO';

SELECT * FROM Customers WHERE CustomerID='ACMEO';

---

SELECT * FROM Orders WHERE CustomerID='ACMEC';
INSERT INTO Orders (CustomerID,EmployeeID,OrderDate,RequiredDate,ShipCountry)
VALUES ('ACMEC',5,GETDATE(),GETDATE()+45,'Turkiye');

SELECT * FROM Orders WHERE CustomerID='ACMEC';

--Eklenen son sipariş ID’sini al:
DECLARE @NewOrderID INT;
SET @NewOrderID = SCOPE_IDENTITY();

SELECT @NewOrderID AS NewOrderID;

INSERT INTO [Order Details]
    (OrderID, ProductID, UnitPrice, Quantity, Discount)
VALUES
    (@NewOrderID, 1, 18.00, 5, 0);

SELECT * FROM  [Order Details] WHERE OrderID=11078

---
--- Fiyatı Product dan alıp %10 ekleyip OrderDetail a kalem/item ekliyoruz

INSERT INTO [Order Details]
    (OrderID, ProductID, UnitPrice, Quantity, Discount)
SELECT
    11078,
    p.ProductID,
    p.UnitPrice * 1.10,
    5,
    0
FROM Products p
WHERE p.ProductID = 2;

SELECT *
FROM [Order Details]
WHERE OrderID = 11078;

---
SELECT * FROM Customers;

SELECT * FROM Customers WHERE City=(SELECT City FROM Customers WHERE CustomerID='AROUT')
SELECT * FROM Customers WHERE City='London'
SELECT City FROM Customers WHERE CustomerID='AROUT'

--Sipariş veren müşterilerim

SELECT *
FROM Customers
WHERE CustomerID IN (
    SELECT CustomerID
    FROM Orders
);

--Sipariş vermeyen müşterilerim

SELECT *
FROM Customers
WHERE CustomerID NOT IN (
    SELECT CustomerID
    FROM Orders
);

--Siparişi olan müşteriler

SELECT *
FROM Customers c
WHERE EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.CustomerID = c.CustomerID
);
--Sipariş vermeyen müşterilerim
SELECT *
FROM Customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.CustomerID = c.CustomerID
);

--Her müşterinin siparişi var mı
SELECT c.CustomerID, c.CompanyName
FROM Customers c
WHERE (
    SELECT COUNT(*)
    FROM Orders o
    WHERE o.CustomerID = c.CustomerID
) > 0;

SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (
    SELECT AVG(UnitPrice)
    FROM Products
);

SELECT
    ProductName,
    UnitPrice,
    (SELECT AVG(UnitPrice) FROM Products) AS AvgPrice
FROM Products;

SELECT *
FROM (
    SELECT ProductName, UnitPrice
    FROM Products
    WHERE UnitPrice > 20
) AS ExpensiveProducts;


SELECT *
FROM (
    SELECT ProductName, UnitPrice
    FROM Products
    WHERE UnitPrice > 20
) AS Exp


SELECT *
FROM (
    SELECT ProductName, UnitPrice
    FROM Products
    WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products)
) AS ExpensiveProducts;

SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products);

SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice = (
    SELECT MAX(UnitPrice)
    FROM Products
);


SELECT   Products.ProductID, Products.ProductName, Categories.CategoryName
FROM         Categories INNER JOIN
                         Products ON Categories.CategoryID = Products.CategoryID


