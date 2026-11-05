
--PLANET EXPRESS: Segementación de clientes

--1. Establecemos el contexto

USE DATABASE UCM;

USE SCHEMA PLANET_EXPRESS;

SELECT * FROM ORDERS;

--2. Levamos a cabo Análsis expolatorio

SELECT COUNT(ORDERID) AS Num_Pedidos, COUNT(*) AS Num_Filas,  COUNT(DISTINCT CUSTOMERID) AS Num_Clientes,
       ROUND(AVG(FREIGHT), 2) AS Promedio_Peso, ROUND(STDDEV(FREIGHT), 2) AS Desviacion_Peso, 
       MAX(FREIGHT) AS Maximo_Peso, MIN(FREIGHT) AS Minimo_Peso, 
       MIN(ORDERDATE) AS Pedido_mas_antiguo, MAX(ORDERDATE) Pedido_mas_actual
FROM ORDERS;

--3. Analizamos el promedio de pedidos al día por cliente
--3.1 Primero creamos la vista de número de pedidos al día por cliente (de todos los pedidos)
CREATE OR REPLACE VIEW Pedidos_dia AS 
SELECT CUSTOMERID, ORDERDATE, COUNT(*) AS Pedidos_dia
FROM ORDERS
GROUP BY CUSTOMERID, ORDERDATE;

SELECT * 
FROM PEDIDOS_DIA 
ORDER BY CUSTOMERID, ORDERDATE DESC;

--3.2 A continuación usamos la vista para obtener el proemdio de pedidos por cliente (UN ÚNICO VALOR POR CLIENTE)

SELECT CUSTOMERID, 
ROUND(AVG(Pedidos_dia), 2) AS Promedio_pedidos_dia_cliente
FROM PEDIDOS_DIA
GROUP BY CUSTOMERID
ORDER BY Promedio_pedidos_dia_cliente DESC;

--4. Analizamos el peso máximo por cliente (UN ÚNICO VALOR POR CLIENTE)

CREATE OR REPLACE VIEW Peso_cliente AS
SELECT CUSTOMERID, MAX(FREIGHT) AS Peso_maximo_envio
FROM ORDERS
GROUP BY CUSTOMERID;

SELECT * FROM PESO_CLIENTE PESO_MAXIMO_ENVIO;

--5. Confeccionamos la query final y obtenemos el insight final, obteniendo los clientes segmentados en GOLD, SILVER y STANDART

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


