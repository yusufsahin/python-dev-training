CREATE DATABASE Northwind2;

USE Northwind2;

CREATE TABLE Categories(
	CategoryID int PRIMARY KEY,
	CategoryName nvarchar(255),
	[Description] ntext,
	Picture image
);

ALTER TABLE Categories ADD ShortName nvarchar(50);

SELECT * FROM Categories;

TRUNCATE TABLE Categories;

SELECT * FROM Categories;

DROP TABLE Categories;

SELECT * FROM Categories;

DROP DATABASE Northwind2;
SELECT
    s.session_id,
    s.login_name,
    s.host_name,
    s.program_name,
    s.status
FROM sys.dm_exec_sessions s
JOIN sys.dm_exec_connections c ON s.session_id = c.session_id
WHERE s.database_id = DB_ID('Northwind2')
  AND s.session_id <> @@SPID;

ALTER DATABASE Northwind2 SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

DROP DATABASE Northwind2;

CREATE DATABASE Northwind2;
GO

USE Northwind2;
GO

CREATE TABLE dbo.Categories(
    CategoryID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    CategoryName nvarchar(255) NULL,
    [Description] nvarchar(max) NULL,
    Picture varbinary(max) NULL
);
GO

--Tek satırlı Comment 
/*
Çok 
satırlı 
comment
*/

TRUNCATE TABLE Categories;
GO

ALTER TABLE Categories ADD ShortName nvarchar(50);

DROP TABLE Categories;
