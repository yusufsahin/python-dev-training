--Numeric 

CREATE TABLE dbo.NumericDemo(
	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	SmallI smallint,
	NormalI int,
	BigI bigint,
	TinyI tinyint
);
-- MAX değerler

INSERT dbo.NumericDemo(SmallI,NormalI,BigI,TinyI) VALUES (32767,2147483647,9223372036854775807,255);

SELECT * FROM dbo.NumericDemo;

--Hata verir değerler max atanabilecek üzerinde 
INSERT dbo.NumericDemo(SmallI,NormalI,BigI,TinyI) VALUES (32768,2147483648,9223372036854775808,256);


--MIN değerler
INSERT dbo.NumericDemo(SmallI,NormalI,BigI,TinyI) VALUES (-32768,-2147483648,-9223372036854775807,0);
SELECT * FROM dbo.NumericDemo;

--Hata verir değerler min atanabilecek üzerinde 
INSERT dbo.NumericDemo(SmallI,NormalI,BigI,TinyI) VALUES (-32769,-2147483649,-9223372036854775808,-1);
SELECT * FROM dbo.NumericDemo;

-------
--Ondalıklı / hassas

--decimal(p,s) / numeric(p,s) → finansal/precise
--float / real → yaklaşık (approx)

CREATE TABLE dbo.DecimalFloatDemo (
    Amount       decimal(18,2),
    RatioApprox  float,
    RatioReal    real
);

INSERT dbo.DecimalFloatDemo (Amount, RatioApprox, RatioReal)
VALUES (12345.67, 0.1, 0.1);

SELECT  * FROM DecimalFloatDemo;

INSERT dbo.DecimalFloatDemo (Amount, RatioApprox, RatioReal)
VALUES (9999999999999999.99, 0.1, 0.1); -- 0.1000000000555..

SELECT  * FROM DecimalFloatDemo;

--Hata verir toplam 19 basamak 2 si nokta/virgül deb sonra 
INSERT dbo.DecimalFloatDemo (Amount, RatioApprox, RatioReal)
VALUES (10000000000000000.00, 0.1, 0.1);
--Amount → para gibi kesin değer (kuruşlu)

--RatioApprox → oran, ölçüm, bilimsel hesap, istatistik (yaklaşık)

--RatioReal → daha düşük hassasiyetli yaklaşık

--p (precision) = toplam basamak sayısı (sol + sağ)

--s (scale) = virgülden sonraki basamak sayısı


--float / real
--Bunlar approximate (yaklaşık) sayılardır.
--IEEE 754 mantığıyla ikili (binary) biçimde saklandığı için bazı ondalık değerler tam temsil edilemez.
--real ≈ 4 byte (yaklaşık 7 basamak hassasiyet)
--float varsayılan olarak float(53) gelir ≈ 8 byte (yaklaşık 15-16 basamak hassasiyet)

--SQL Server’da float yazarsan genelde float(53) yani “double” gibi düşün.

--0.10000000000000000555… (temsil hatası)

SELECT
  CAST(0.1 AS decimal(18,17)) + CAST(0.2 AS decimal(18,17)) AS DecSum,
  CAST(0.1 AS float) + CAST(0.2 AS float)                   AS FloatSum;

SELECT
  Amount,
  CAST(RatioApprox AS decimal(38,30)) AS RatioApprox_as_Decimal,
  CAST(RatioReal   AS decimal(38,30)) AS RatioReal_as_Decimal
FROM dbo.DecimalFloatDemo;

SELECT CAST(1.999 AS decimal(18,2)) AS Rounded;  -- 2.00

SELECT CAST(9999999999999999.99 AS decimal(18,2)) AS MaxOk;

--Metin tipleri (String)
--varchar(n) / nvarchar(n) → değişken uzunluk (nvarchar Unicode)
--char(n) / nchar(n) → sabit uzunluk
--n  national / unicode farklı dilleri destekler

CREATE TABLE dbo.StringDemo (
    Code        char(5),
    NameTr      nvarchar(100),
    Email       varchar(255)
);

INSERT dbo.StringDemo (Code, NameTr, Email)
VALUES ('A0001', N'Çağrı Merkezi', 'test@example.com');

Select * from StringDemo;

--Tarih & zaman tipleri (Date/Time)
--date, time, datetime2, datetimeoffset

CREATE TABLE dbo.DateTimeDemo (
    CreatedDate     date,
    CreatedAt       datetime2(3),
    CreatedAtTz     datetimeoffset(0)
);

INSERT dbo.DateTimeDemo (CreatedDate, CreatedAt, CreatedAtTz)
VALUES (CONVERT(date, GETDATE()),
        SYSDATETIME(),
        SYSDATETIMEOFFSET());
select * from DateTimeDemo;

--Mantıksal (Boolean)
CREATE TABLE dbo.BoolDemo (
    IsActive bit NOT NULL
);

INSERT dbo.BoolDemo (IsActive) VALUES (1), (0);

SELECT * FROM BoolDemo;

--İkili veriler (Binary)

CREATE TABLE dbo.BinaryDemo (
    FileBytes varbinary(max),
    Sha256    varbinary(32)
);

INSERT dbo.BinaryDemo (FileBytes, Sha256)
VALUES (0x01020304, HASHBYTES('SHA2_256', 'hello'));

SELECT * FROM BinaryDemo;

SELECT
  CONVERT(varchar(max), FileBytes, 2) AS FileBytes_Hex,
  CONVERT(varchar(64),  Sha256,   2)  AS Sha256_Hex
FROM dbo.BinaryDemo;

--GUID (Unique Identifier)

CREATE TABLE dbo.GuidDemo (
    RowGuid uniqueidentifier NOT NULL DEFAULT NEWID()
);


INSERT dbo.GuidDemo DEFAULT VALUES;

SELECT * FROM dbo.GuidDemo;
INSERT dbo.GuidDemo DEFAULT VALUES;

SELECT * FROM dbo.GuidDemo;

--JSON / yarı-yapısal
--SQL Server’da JSON genelde nvarchar(max) içinde tutulur + JSON_VALUE/OPENJSON ile işlenir

CREATE TABLE dbo.JsonDemo (
    Payload nvarchar(max) NOT NULL
);

INSERT dbo.JsonDemo (Payload)
VALUES (N'{"customerId": 10, "tags":["vip","trial"]}');

SELECT JSON_VALUE(Payload, '$.customerId') AS customerId
FROM dbo.JsonDemo;

--XML

CREATE TABLE dbo.XmlDemo (
    Doc xml
);

INSERT dbo.XmlDemo (Doc)
VALUES (N'<root><id>1</id></root>');

SELECT Doc.value('(/root/id/text())[1]', 'int') AS Id
FROM dbo.XmlDemo;

--Eskiden text/ntext/image vardı; modern kullanım:
-varchar(max) / nvarchar(max) / varbinary(max) tercih et.