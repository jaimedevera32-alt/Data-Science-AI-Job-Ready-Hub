-- 1. Queries I

-- SELECT
SELECT columna1, columna2
FROM tabla;

-- DISTINCT
SELECT DISTINCT columna1
FROM tabla;

-- SELECT ALL
SELECT ALL columna1, columna2
FROM tabla;

-- ALIAS para Columnas
SELECT columna1 AS alias_columna1, 
       columna2 AS alias_columna2
FROM tabla;

-- ALIAS para Tablas
SELECT t.columna1, t.columna2
FROM tabla AS t;

-- WHERE
SELECT columna1, columna2
FROM tabla
WHERE columna1 = 'valor';

--OPERADORES DE COMPARACIÓN
-- Ejemplo con = (igual a)
SELECT columna1, columna2
FROM tabla
WHERE columna1 = 'valor';

-- Ejemplo con <> (distinto de)
SELECT columna1, columna2
FROM tabla
WHERE columna1 <> 'valor';

-- Ejemplo con > (mayor que)
SELECT columna1, columna2
FROM tabla
WHERE columna1 > 100;

-- Ejemplo con < (menor que)
SELECT columna1, columna2
FROM tabla
WHERE columna1 < 100;

-- Ejemplo con >= (mayor o igual que)
SELECT columna1, columna2
FROM tabla
WHERE columna1 >= 50;

-- Ejemplo con <= (menor o igual que)
SELECT columna1, columna2
FROM tabla
WHERE columna1 <= 50;

-- ORDER BY
SELECT columna1, columna2
FROM tabla
ORDER BY columna1 [ASC | DESC];

-- TOP
SELECT TOP n columna1, columna2
FROM tabla
ORDER BY columna1 DESC;

-- CASE WHEN
SELECT columna1,
       CASE 
           WHEN columna2 = 'valor' THEN 'Resultado1'
           ELSE 'Resultado por defecto'
       END AS nueva_columna
FROM tabla;

-- Operadores Lógicos: AND, OR, NOT
SELECT * 
FROM tabla
WHERE columna1 > 100
AND columna2 = 'valor';

SELECT * 
FROM tabla
WHERE columna1 > 100
OR columna2 = 'valor';

SELECT * 
FROM tabla
WHERE NOT columna1 > 100;

-- IN
SELECT * 
FROM tabla
WHERE columna1 IN ('valor1', 'valor2', 'valor3');

-- BETWEEN
--Números
SELECT * 
FROM tabla
WHERE columna1 BETWEEN 100 AND 200;

-- Fechas
SELECT columna1, columna_fecha
FROM tabla
WHERE columna_fecha BETWEEN '2023-01-01' AND '2023-12-31';


-- NULL
SELECT * 
FROM tabla
WHERE columna1 IS NULL;

-- LIKE
SELECT * 
FROM tabla
WHERE columna1 LIKE 'A%';

-- FUNCIONES: UPPER, LOWER, CONCAT, TRUNCATE
SELECT UPPER(columna1), LOWER(columna2)
FROM tabla;

SELECT CONCAT(columna1, columna2)
FROM tabla;

SELECT TRUNCATE(columna1, 2)
FROM tabla;

-- FUNCIONES MATEMÁTICAS: POWER, SQRT, ROUND
SELECT POWER(columna1, 2), SQRT(columna2), ROUND(columna3, 1)
FROM tabla;

-- FUNCIONES DE FECHA: MONTH(), YEAR(), HOUR(), MINUTE()
SELECT MONTH(columna_fecha), 
       YEAR(columna_fecha), 
       HOUR(columna_fecha), 
       MINUTE(columna_fecha)
FROM tabla;

-- Verificar valores nulos
SELECT columna1
FROM tabla
WHERE columna2 IS NULL;

-- Reemplazar NULL con un valor predeterminado (IFNULL)
SELECT IFNULL(columna1, 'Valor por defecto') AS columna_con_valor
FROM tabla;

-- Devolver el primer valor no nulo (COALESCE)
SELECT COALESCE(columna1, columna2, 'Valor por defecto') AS columna_no_nula
FROM tabla;

-- Comparar y devolver NULL si dos valores son iguales (NULLIF)
SELECT NULLIF(columna1, columna2) AS resultado
FROM tabla;

-- GROUP BY
SELECT columna1, SUM(columna2)
FROM tabla
GROUP BY columna1;

-- HAVING
SELECT columna1, SUM(columna2)
FROM tabla
GROUP BY columna1
HAVING SUM(columna2) > 100;

--: COUNT, SUM, AVG, MAX, MIN
SELECT 
    COUNT(columna1) AS total_filas,      -- Cuenta el número total de filas
    SUM(columna2) AS suma_total,         -- Suma los valores de columna2
    AVG(columna2) AS promedio_valores,   -- Calcula el promedio de columna2
    MAX(columna2) AS valor_maximo,       -- Encuentra el valor máximo en columna2
    MIN(columna2) AS valor_minimo        -- Encuentra el valor mínimo en columna2
FROM tabla
WHERE condicion;


-- 2. Combinación de Tablas

-- JOIN NATURAL
SELECT *
FROM tabla1, tabla2
WHERE tabla1.columna_comun = tabla2.columna_comun;

-- INNER JOIN
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
INNER JOIN tabla2 t2 ON t1.columna_comun = t2.columna_comun;

-- LEFT JOIN
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
LEFT JOIN tabla2 t2 ON t1.columna_comun = t2.columna_comun;

-- RIGHT JOIN
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
RIGHT JOIN tabla2 t2 ON t1.columna_comun = t2.columna_comun;

-- FULL OUTER JOIN
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
FULL OUTER JOIN tabla2 t2 ON t1.columna_comun = t2.columna_comun;

-- SET OPERATORS

-- UNION
SELECT columna1 FROM tabla1
UNION
SELECT columna1 FROM tabla2;

-- INTERSECT
SELECT columna1 FROM tabla1
INTERSECT
SELECT columna1 FROM tabla2;

-- EXCEPT
SELECT columna1 FROM tabla1
EXCEPT
SELECT columna1 FROM tabla2;

-- 3. Queries II

-- SUBQUERIES

-- Subquery Independiente
SELECT columna1
FROM tabla1
WHERE columna2 = (SELECT MAX(columna2) FROM tabla2);

-- Subquery Relacionada
SELECT columna1
FROM (SELECT columna1 FROM tabla WHERE condicion) AS subquery;

-- VIEWS

-- Crear Vista
CREATE VIEW nombre_vista AS
SELECT columna1, columna2
FROM tabla
WHERE condicion;

-- WINDOW FUNCTIONS

-- Función de ventana sin partición ni ordenación: Suma total del salario para toda la tabla
SELECT nombre, 
       SUM(salario) OVER() AS total_salarial
FROM empleados;

-- Función de ventana con ordenación: Salario acumulado para cada empleado
SELECT nombre, 
       salario, 
       SUM(salario) OVER(ORDER BY salario DESC) AS acumulado_salarial
FROM empleados;

-- Función de ventana con PARTITION BY: Salario total por departamento
SELECT id_departamento, 
       nombre, 
       SUM(salario) OVER(PARTITION BY id_departamento ORDER BY salario DESC) AS total_salarial_departamento
FROM empleados;

