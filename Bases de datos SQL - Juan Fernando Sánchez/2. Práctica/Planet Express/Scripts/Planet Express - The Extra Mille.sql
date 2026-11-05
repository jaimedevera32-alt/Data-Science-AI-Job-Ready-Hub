
--1. Analizamos el promedio de pedidos al día por cliente
--1.1 Primero creamos la vista de número de pedidos al día por cliente (de todos los pedidos)
CREATE OR REPLACE VIEW Pedidos_dia AS 
SELECT CUSTOMERID, ORDERDATE, COUNT(*) AS Pedidos_dia
FROM ORDERS
GROUP BY CUSTOMERID, ORDERDATE;

SELECT * 
FROM PEDIDOS_DIA 
ORDER BY CUSTOMERID, ORDERDATE DESC;

--1.2 A continuación usamos la vista para obtener el proemdio de pedidos por cliente (UN ÚNICO VALOR POR CLIENTE)

SELECT CUSTOMERID, 
ROUND(AVG(Pedidos_dia), 2) AS Promedio_pedidos_dia_cliente
FROM PEDIDOS_DIA
GROUP BY CUSTOMERID
ORDER BY Promedio_pedidos_dia_cliente DESC;

--2. Analizamos el peso máximo por cliente (UN ÚNICO VALOR POR CLIENTE)

CREATE OR REPLACE VIEW Peso_cliente AS
SELECT CUSTOMERID, MAX(FREIGHT) AS Peso_maximo_envio
FROM ORDERS
GROUP BY CUSTOMERID;

SELECT * FROM PESO_CLIENTE PESO_MAXIMO_ENVIO;

--3. Confeccionamos la query final y obtenemos el insight final, obteniendo los clientes segmentados en GOLD, SILVER y STANDART

--3.1 JOIN de VIEWS

SELECT d.CUSTOMERID, 
ROUND(AVG(d.Pedidos_dia), 2) AS Promedio_pedidos_dia_cliente,
Peso_maximo_envio AS Peso_maximo_cliente,
CASE 
    WHEN Promedio_pedidos_dia_cliente>1 AND Peso_maximo_cliente < 195.70 THEN 'Cliente Gold'
    WHEN Promedio_pedidos_dia_cliente>1 AND Peso_maximo_cliente > 195.70 THEN 'Cliente Silver'
    ELSE 'Cliente Standart'
end as Tipo_de_cliente
FROM PEDIDOS_DIA AS d JOIN PESO_CLIENTE AS c
ON d.CUSTOMERID=c.CUSTOMERID
GROUP BY ALL
ORDER BY Tipo_de_cliente, Promedio_pedidos_dia_cliente DESC, Peso_maximo_cliente DESC;



--6. Alternativa con CTE

-- Analizamos el promedio de pedidos al día por cliente con CTEs
WITH Pedidos_dia AS (
    SELECT CUSTOMERID, ORDERDATE, COUNT(*) AS Pedidos_dia
    FROM ORDERS
    GROUP BY CUSTOMERID, ORDERDATE
),
Promedio_pedidos_dia AS (
    SELECT CUSTOMERID, ROUND(AVG(Pedidos_dia), 2) AS Promedio_pedidos_dia_cliente
    FROM Pedidos_dia
    GROUP BY CUSTOMERID
),
Peso_cliente AS (
    SELECT CUSTOMERID, MAX(FREIGHT) AS Peso_maximo_envio
    FROM ORDERS
    GROUP BY CUSTOMERID
)
SELECT p.CUSTOMERID, 
       p.Promedio_pedidos_dia_cliente,
       pc.Peso_maximo_envio AS Peso_maximo_cliente,
       CASE 
           WHEN p.Promedio_pedidos_dia_cliente > 1 AND pc.Peso_maximo_envio < 195.70 THEN 'Cliente Gold'
           WHEN p.Promedio_pedidos_dia_cliente > 1 AND pc.Peso_maximo_envio >= 195.70 THEN 'Cliente Silver'
           ELSE 'Cliente Standard'
       END AS Tipo_de_cliente
FROM Promedio_pedidos_dia AS p
JOIN Peso_cliente AS pc
ON p.CUSTOMERID = pc.CUSTOMERID
ORDER BY Tipo_de_cliente, p.Promedio_pedidos_dia_cliente DESC, pc.Peso_maximo_envio DESC;

--7. SELF JOIN
SELECT d.CUSTOMERID, 
       ROUND(AVG(d.Pedidos_dia), 2) AS Promedio_pedidos_dia_cliente,
       c.Peso_maximo_envio AS Peso_maximo_cliente,
       CASE 
           WHEN ROUND(AVG(d.Pedidos_dia), 2) > 1 AND c.Peso_maximo_envio < 195.70 THEN 'Cliente Gold'
           WHEN ROUND(AVG(d.Pedidos_dia), 2) > 1 AND c.Peso_maximo_envio >= 195.70 THEN 'Cliente Silver'
           ELSE 'Cliente Standard'
       END AS Tipo_de_cliente
FROM (
    SELECT CUSTOMERID, ORDERDATE, COUNT(*) AS Pedidos_dia
    FROM ORDERS
    GROUP BY CUSTOMERID, ORDERDATE
) AS d
JOIN (
    SELECT CUSTOMERID, MAX(FREIGHT) AS Peso_maximo_envio
    FROM ORDERS
    GROUP BY CUSTOMERID
) AS c
ON d.CUSTOMERID = c.CUSTOMERID
GROUP BY d.CUSTOMERID, c.Peso_maximo_envio
ORDER BY Tipo_de_cliente, Promedio_pedidos_dia_cliente DESC, Peso_maximo_cliente DESC;
