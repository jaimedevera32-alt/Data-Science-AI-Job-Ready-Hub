-- PROYECTO ONU: SOLUCIONES CORREGIDAS
-- Orden ajustado según enunciados del PDF del material docente

-- ================================================
-- EJERCICIOS SELECT Y FROM
-- ================================================

-- 1. Mostrar todas las filas y columnas de las cinco tablas.
SELECT * FROM countries;
SELECT * FROM human_developments;
SELECT * FROM country_populations;
SELECT * FROM country_populations_2021;
SELECT * FROM paid_days_off;

-- 2. Mostrar la columna country_id, year, gender y esperanza de vida al nacer.
SELECT country_id, year, gender, life_expectancy_at_birth
FROM human_developments;

-- 3. Mostrar distintos country_id de la tabla de poblaciones (1 vez cada country_id).
SELECT DISTINCT country_id 
FROM country_populations;

-- 4. Mostrar el country_id y la población. Crear un alias y llamarlo población.
SELECT country_id, population AS "Poblacion"
FROM country_populations;

-- ================================================
-- EJERCICIOS WHERE
-- ================================================

-- 1. Mostrar toda la información de la tabla índice de desarrollo humano para España.
SELECT *
FROM human_developments
WHERE country_id = 'ESP';

-- 2. Mostrar los datos de población de españa (ESP) después del 2010.
SELECT * 
FROM country_populations
WHERE country_id = 'ESP' AND year > 2010;

-- 3. Mostrar todos los datos de la tabla de días libres para aquellos países que tengan más de 10 festivos nacionales.
SELECT *
FROM paid_days_off
WHERE paid_public_holidays > 10;

-- 4. Mostrar todos los datos de la tabla de días libres para aquellos países que tengan más de 10 festivos nacionales y más de 15 días de vacaciones al año.
SELECT *
FROM paid_days_off
WHERE paid_public_holidays > 10 AND paid_leave_days > 15;

-- 5. Mostrar las columnas id, género e índice de desarrollo humano para España y Portugal.
SELECT country_id, gender, human_development_index
FROM human_developments
WHERE country_id IN ('ESP', 'PRT');

-- 6. Mostrar los datos de población de España entre 1990 y el 2000.
SELECT *
FROM country_populations
WHERE country_id = 'ESP' AND year BETWEEN 1990 AND 2000;

-- 7. Mostrar todos los datos de la tabla de índice de desarrollo humano para aquellos países en que el índice no sea nulo.
SELECT *
FROM human_developments
WHERE human_development_index IS NOT NULL;

-- 8. Mostrar todos los países de la tabla del índice de desarrollo humano para aquellos IDs cuyo nombre empieza por T.
SELECT *
FROM human_developments
WHERE country_id LIKE 'T%';

-- 9. Mostrar todos los países de la tabla del índice de desarrollo humano para aquellos IDs cuyo nombre contiene una V.
SELECT *
FROM human_developments 
WHERE country_id LIKE '%V%';

-- ================================================
-- EJERCICIOS GROUP BY
-- ================================================

-- 1. Obtener la suma de la población mundial en 2020.
SELECT SUM(population) AS poblacion_mundial_en_2020
FROM country_populations
WHERE year = 2020;

-- 2. Obtener la media de los años esperados de escolarización por países para el año 2020.
SELECT country_id, AVG(expected_years_of_schooling) AS promedio_escolarizacion
FROM human_developments 
WHERE year = 2020
GROUP BY country_id;

-- 3. Obtener la media del índice de desarrollo humano por género entre los años 2000 y 2020.
SELECT gender, AVG(human_development_index) AS promedio_hdi
FROM human_developments
WHERE year BETWEEN 2000 AND 2020
GROUP BY gender;

-- 4. Obtener para cada país el mayor índice de desarrollo humano que haya tenido en su historia.
SELECT country_id, MAX(human_development_index) AS mayor_hdi
FROM human_developments
GROUP BY country_id;

-- 5. Obtener el promedio del índice de desarrollo humano, la esperanza de vida al nacer y la renta per capita, para todas los países entre los años 1990 y 2000.
SELECT country_id, 
       AVG(human_development_index) AS promedio_hdi, 
       AVG(life_expectancy_at_birth) AS promedio_esperanza_vida, 
       AVG(gross_national_income_per_capita) AS promedio_renta
FROM human_developments 
WHERE year BETWEEN 1990 AND 2000
GROUP BY country_id;

-- ================================================
-- EJERCICIOS HAVING
-- ================================================

-- 1. Obtener aquellos países y el índice de desarrollo humano para los países cuyo valor mínimo del índice de desarrollo humano esté por encima de 0.7 entre los años 2000 y 2020.
SELECT country_id, MIN(human_development_index) AS min_hdi
FROM human_developments
WHERE year BETWEEN 2000 AND 2020
GROUP BY country_id
HAVING MIN(human_development_index) > 0.7;

-- 2. Obtener para el género femenino los países y el promedio de los años de escolarización para aquellos países cuyo promedio de los años de escolarización esperados para las mujeres sean mayor de 10 en los años 90.
SELECT country_id, AVG(expected_years_of_schooling) AS avg_school_years
FROM human_developments
WHERE gender = 'Female' AND year BETWEEN 1990 AND 1999
GROUP BY country_id
HAVING AVG(expected_years_of_schooling) > 10;

-- 3. Obtener los países y la renta per capita para aquellos países cuyo promedio de la renta per capita de los años 90 se mayor a 35000.
SELECT country_id, AVG(gross_national_income_per_capita) AS avg_income
FROM human_developments 
WHERE year BETWEEN 1990 AND 1999
GROUP BY country_id
HAVING AVG(gross_national_income_per_capita) > 35000;

-- 4. Obtener el promedio por país y género de la esperanza de vida al nacer para aquellos países que tengan un promedio del índice de desarrollo humano menor 0.7 en los años 90.
SELECT country_id, gender, AVG(life_expectancy_at_birth) AS avg_life_expectancy
FROM human_developments
WHERE year BETWEEN 1990 AND 1999
GROUP BY country_id, gender
HAVING AVG(human_development_index) < 0.7;

-- ================================================
-- EJERCICIOS ORDER BY
-- ================================================

-- 1. Obtener una lista de países, el índice de desarrollo humano y la esperanza de vida al nacer ordenada de manera descendente en función del promedio del índice de desarrollo humano. Filtrar la información para el año 2020 y los valores del HDI nulos.
SELECT country_id, human_development_index, life_expectancy_at_birth
FROM human_developments
WHERE year = 2020 AND human_development_index IS NOT NULL
ORDER BY human_development_index DESC;

-- 2. Obtener una lista con los países y el promedio de los años esperados de escolarización ordenada de manera descendente en base al promedio de los años esperados de escolarización. Filtrar la información para los años 90 y mostrar solo aquellos países cuyos años esperados de escolarización sean menos de 7.
SELECT country_id, AVG(expected_years_of_schooling) AS avg_school_years
FROM human_developments
WHERE year BETWEEN 1990 AND 1999
GROUP BY country_id
HAVING AVG(expected_years_of_schooling) < 7
ORDER BY avg_school_years DESC;

-- 3. Obtener una lista con los países y su promedio de la renta per capita y ordenar el resultado de manera descendente en base al promedio de la renta per capita. Filtrar para los años 2000 y diferenciar el resultado entre hombres y mujeres.
SELECT country_id, gender, AVG(gross_national_income_per_capita) AS avg_income
FROM human_developments 
WHERE year BETWEEN 2000 AND 2009
GROUP BY country_id, gender
ORDER BY avg_income DESC;

-- 4.4 Obtener una lista países, promedio de esperanza de vida y promedio de renta per capita ordenada de manera descendente en base a la esperanza de vida. Filtrar la información para los años 2000 y mostrar solo aquellos países cuyo promedio de la renta per capita sea mayor a 45000.
SELECT country_id, AVG(life_expectancy_at_birth) AS promedio_vida, AVG(gross_national_income_per_capita) AS promedio_renta 
FROM human_developments 
WHERE year BETWEEN 2000 AND 2009 
GROUP BY country_id 
HAVING AVG(gross_national_income_per_capita) > 45000 
ORDER BY promedio_vida DESC;
-- ================================================
-- EJERCICIOS JOIN
-- ================================================

-- 1. Realizar una consulta donde se muestra el país, el promedio del índice del desarrollo humano, el promedio de la esperanza de vida y el promedio de la población. Mostrar los valores para los años 90 y solo para aquellos países que tengan un promedio del índice del desarrollo humano mayor de 0.75.
SELECT c.country, 
       AVG(hd.human_development_index) AS avg_hdi, 
       AVG(hd.life_expectancy_at_birth) AS avg_life_expectancy, 
       AVG(cp.population) AS avg_population
FROM human_developments hd
JOIN countries c ON hd.country_id = c.country_id
JOIN country_populations cp ON hd.country_id = cp.country_id AND hd.year = cp.year
WHERE hd.year BETWEEN 1990 AND 1999
GROUP BY c.country
HAVING AVG(hd.human_development_index) > 0.75;

-- 2. Realizar una consulta donde se muestra el país, la región, el promedio de población, el promedio de días libres y el promedio del índice del desarrollo humano. Filtrar para los años más allá del 2000 y el género masculino.
SELECT c.country, 
       c.region, 
       AVG(cp.population) AS avg_population, 
       AVG(pdo.paid_leave_days + pdo.paid_public_holidays) AS avg_free_days, 
       AVG(hd.human_development_index) AS avg_hdi
FROM countries c
LEFT JOIN human_developments hd ON c.country_id = hd.country_id AND hd.gender = 'Male'
LEFT JOIN country_populations cp ON c.country_id = cp.country_id AND cp.year > 2000
LEFT JOIN paid_days_off pdo ON c.country_id = pdo.country_id
GROUP BY c.country, c.region;

-- 3. Crear una consulta en donde categorizamos los países en base a los siguientes criterios:
-- Si el índice de desarrollo humano es mayor que 0.8 y sus días libre son más de 20 "Top Country"
-- Si el índice de desarrollo humano está entre 0.7 y 0.8 y sus días libres son más de 15 "Medium Country"
-- Si el índice de desarrollo humano es menor que 0.7 "Bottom Country"
-- El resto "Other"
-- Mostrar el país, el índice de desarrollo humano, el total de días libres y su categoría. Filtrar los datos para los años 90.
SELECT c.country, 
       hd.human_development_index, 
       (pdo.paid_leave_days + pdo.paid_public_holidays) AS total_days_off,
       CASE
           WHEN hd.human_development_index > 0.8 AND (pdo.paid_leave_days + pdo.paid_public_holidays) > 20 THEN 'Top Country'
           WHEN hd.human_development_index BETWEEN 0.7 AND 0.8 AND (pdo.paid_leave_days + pdo.paid_public_holidays) > 15 THEN 'Medium Country'
           WHEN hd.human_development_index < 0.7 THEN 'Bottom Country'
           ELSE 'Other'
       END AS country_category
FROM human_developments hd
JOIN countries c ON hd.country_id = c.country_id
JOIN paid_days_off pdo ON hd.country_id = pdo.country_id
WHERE hd.year BETWEEN 1990 AND 1999;

-- ================================================
-- EJERCICIOS SET OPERATORS
-- ================================================

-- 1. Crear una tabla donde unimos el resultado de dos consultas:
-- Seleccionar el id del país y el año desde la tabla country_population y country_population_2021.
SELECT country_id, year
FROM country_populations
WHERE year = 2020

UNION

SELECT country_id, year
FROM country_populations_2021
WHERE year = 2021;

-- 2. Crear una tabla en que solo mostremos aquellos países que se encuentran en la tabla de población y días libres.
-- Aquellos países que no estén en las dos no los mostramos.
SELECT country_id
FROM country_populations
INTERSECT
SELECT country_id
FROM paid_days_off;

-- 3. Crear una tabla en que solo mostremos aquellos países que no se encuentren en las dos tablas de población y días libres.
-- Solo mostramos los países que no se encuentran en ambas tablas.
SELECT country_id
FROM country_populations
EXCEPT
SELECT country_id
FROM paid_days_off;



-- ================================================
-- PROYECTO ONU: PARTE 2 - CONSULTAS AVANZADAS
-- ================================================

-- ================================================
-- EJERCICIOS CASE WHEN
-- ================================================

-- 1. Crear una categorización de los datos que identifica el año 2021 como "Current Year", el año 2020 como "Previous Year" y el resto como "Otros" y mostrar el promedio de índice de desarrollo humano para estos tres categorías.
SELECT 
    CASE 
        WHEN year = 2021 THEN 'Current Year'
        WHEN year = 2020 THEN 'Previous Year'
        ELSE 'Otros'
    END AS year_category,
    AVG(human_development_index) AS promedio_hdi
FROM human_developments
GROUP BY year_category
ORDER BY year_category;

-- 2. Crear una categorización de los datos que identifica los países del G7 como "G7" y el resto de países como "Otros", hacer un conteo del número de países y mostrar su promedio del índice de desarrollo humano y su renta per cápita. Filtrar la información para el año 2020 e incluir solo los países con el índice de desarrollo humano no nulo.
SELECT 
    CASE
        WHEN country_id IN ('USA', 'CAN', 'GBR', 'FRA', 'DEU', 'ITA', 'JPN') THEN 'G7'
        ELSE 'Otros'
    END AS group_category,
    COUNT(DISTINCT country_id) AS num_paises,
    AVG(human_development_index) AS promedio_hdi,
    AVG(gross_national_income_per_capita) AS promedio_renta
FROM human_developments
WHERE year = 2020 AND human_development_index IS NOT NULL
GROUP BY group_category;

-- 3. Crear una categorización de los países basada en la esperanza de vida en 2020:
-- Mayor que 80 -> "Alta"
-- Entre 60 y 80 -> "Media"
-- Menor que 60 -> "Baja".
-- Calcular el promedio del índice de desarrollo humano para estas tres categorías y ordenar los resultados por el promedio del HDI de forma ascendente.
SELECT 
    CASE 
        WHEN life_expectancy_at_birth > 80 THEN 'Alta'
        WHEN life_expectancy_at_birth BETWEEN 60 AND 80 THEN 'Media'
        ELSE 'Baja'
    END AS esperanza_vida_categoria,
    AVG(human_development_index) AS promedio_hdi
FROM human_developments
WHERE year = 2020
GROUP BY esperanza_vida_categoria
ORDER BY promedio_hdi ASC;

-- ================================================
-- EJERCICIOS VISTAS
-- ================================================

-- 1. Crear una vista que muestre el promedio del índice de desarrollo humano, la esperanza de vida al nacer y la renta per capita por país y año.
CREATE VIEW IF NOT EXISTS vista_pais_anio AS
SELECT country_id, 
       year, 
       AVG(human_development_index) AS promedio_hdi, 
       AVG(life_expectancy_at_birth) AS promedio_esperanza_vida, 
       AVG(gross_national_income_per_capita) AS promedio_renta
FROM human_developments
GROUP BY country_id, year;

-- 2. Utilizar la vista creada para mostrar el índice de desarrollo humano promedio por país y año.
SELECT country_id, year, promedio_hdi
FROM vista_pais_anio;

-- ================================================
-- EJERCICIOS FUNCIONES DE VENTANA
-- ================================================

-- 1. Crear una consulta que muestre el país, el año y el índice de desarrollo humano, junto con el índice de desarrollo humano del año anterior. Ordenar los resultados por país y año.
SELECT country_id, 
       year, 
       AVG(human_development_index) OVER (PARTITION BY country_id ORDER BY year) AS hdi_ano_anterior
FROM human_developments
ORDER BY country_id, year;

-- 2. Crear una consulta que muestre el país, el año y el índice de desarrollo humano (Human Development Index), junto con el promedio del índice de desarrollo humano para ese país a lo largo de todos los años disponibles. Utilizar una función de ventana para calcular el promedio del índice de desarrollo humano por país.
SELECT country_id, 
       year, 
       human_development_index,
       AVG(human_development_index) OVER (PARTITION BY country_id) AS promedio_hdi
FROM human_developments
ORDER BY country_id, year;

-- ================================================
-- EJERCICIOS SUBQUERIES
-- ================================================

-- 1. Crear una consulta donde se seleccione el país, el género y el promedio del índice de desarrollo humano. Mostrar solo aquellos países que tengan una población de más de 1 millón en 2020.
SELECT c.country, 
       hd.gender, 
       AVG(hd.human_development_index) AS promedio_hdi
FROM human_developments hd
JOIN countries c ON hd.country_id = c.country_id
WHERE hd.country_id IN (
    SELECT country_id
    FROM country_populations
    WHERE year = 2020 AND population > 1000000
)
GROUP BY c.country, hd.gender;

-- 2. Crear una consulta donde seleccionamos el país, el género y el promedio del índice de desarrollo humano. Mostrar sólo el país con menor número de días libres del planeta.
SELECT c.country, 
       (pdo.paid_leave_days + pdo.paid_public_holidays) AS total_days_off
FROM countries c
JOIN paid_days_off pdo ON c.country_id = pdo.country_id
WHERE (pdo.paid_leave_days + pdo.paid_public_holidays) = (
    SELECT MIN(paid_leave_days + paid_public_holidays) 
    FROM paid_days_off
);

-- ================================================
-- EJERCICIOS TOP
-- ================================================

-- 1. Obtener una lista con los 3 países con el mayor promedio de renta per capita para los años 90.
SELECT TOP 3 country_id, AVG(gross_national_income_per_capita) AS avg_income
FROM human_developments
WHERE year BETWEEN 1990 AND 1999
GROUP BY country_id
ORDER BY avg_income DESC;

-- 2. Obtener una lista con los 5 países con el mayor promedio de años de escolarización para las mujeres en los años 2000.
SELECT TOP 5 country_id, AVG(expected_years_of_schooling) AS avg_school_years
FROM human_developments 
WHERE gender = 'Female' AND year BETWEEN 2000 AND 2009
GROUP BY country_id
ORDER BY avg_school_years DESC;