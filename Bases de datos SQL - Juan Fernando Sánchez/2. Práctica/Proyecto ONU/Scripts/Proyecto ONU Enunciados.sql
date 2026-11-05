-- PROYECTO ONU: PARTE 1

-- Ejercicios SELECT y FROM
-- 1. Mostrar todas las filas y columnas de las tres tablas.

-- 2. Mostrar la columna country_id, year, gender y esperanza de vida al nacer.

-- 3. Mostrar distintos country_id de la tabla de poblaciones (1 vez cada country_id).

-- 4. Mostrar el country_id y la población. Crear un alias y llamarlo población.

--------------------------------------------------------

-- Ejercicios WHERE
-- 1. Mostrar toda la información de la tabla HDI para España.


-- 2. Mostrar los datos de población de España (ESP) después del 2010.

-- 3. Mostrar todos los datos de la tabla de paid_days_off para aquellos países que tengan más de 10 festivos nacionales.

-- 4. Mostrar todos los datos de la tabla de paid_days_off para aquellos países que tengan más de 10 festivos nacionales y más de 15 días de vacaciones al año.

-- 5. Mostrar las columnas id, género e índice de desarrollo humano para España y Portugal.

-- 6. Mostrar los datos de población de España entre 1990 y el 2000.

-- 7. Mostrar todos los datos de la tabla HDI para aquellos países en que el índice no sea nulo.

-- 8. Mostrar todos los países de la tabla HDI cuyo ID empieza por T.

-- 9. Mostrar todos los países de la tabla HDI cuyo ID contiene una V.

--------------------------------------------------------

-- Ejercicios GROUP BY
-- 1. Obtener la suma de la población mundial en 2020.

-- 2. Obtener la media de los años esperados de escolarización por ID para el año 2020.

-- 3. Obtener la media del índice de desarrollo humano por género entre los años 2000 y 2020.

-- 4. Obtener para cada país el mayor índice de desarrollo humano que haya tenido en su historia.

-- 5. Obtener el promedio del índice de desarrollo humano, la esperanza de vida al nacer y la renta per capita, para todos las países entre los años 1990 y 2000.

--------------------------------------------------------

-- Ejercicios HAVING

-- 1. Obtener los ID y el índice de desarrollo humano para los países cuyo valor mínimo del índice de desarrollo humano esté por encima de 0.7 entre los años 2000 y 2020.

-- 2. Obtener para el género femenino los países y el promedio de los años de escolarización para aquellos países cuyo promedio de los años de escolarización esperados para las mujeres sea mayor de 10 en los años 90.

-- 3. Obtener los países y la renta per capita para aquellos países cuyo promedio de la renta per capita de los años 90 sea mayor a 35000.

-- 4. Obtener el promedio por país y género de la esperanza de vida al nacer para aquellos países que tengan un promedio del índice de desarrollo humano menor a 0.7 en los años 90.


--------------------------------------------------------

-- Ejercicios ORDER BY

-- 1. Obtener una lista de países, el índice de desarrollo humano y la esperanza de vida al nacer ordenada de manera descendente en función del promedio del índice de desarrollo humano. Filtrar la información para el año 2020 y los valores del HDI nulos.

-- 2. Obtener una lista con los países y el promedio de los años esperados de escolarización ordenada de manera descendente en base al promedio de los años esperados de escolarización. Filtrar la información para los años 90 y mostrar solo aquellos países cuyos años esperados de escolarización sean menos de 7.

-- 3. Obtener una lista con los países y su promedio de la renta per capita y ordenar el resultado de manera descendente en base al promedio de la renta per capita. Filtrar para los años 2000 y diferenciar el resultado entre hombres y mujeres.

--------------------------------------------------------

-- Ejercicios JOIN

-- 1. Realizar una consulta donde se muestre el país, el promedio del índice del desarrollo humano, el promedio de la esperanza de vida y el promedio de la población. Mostrar los valores para los años 90 y solo para aquellos países que tengan un promedio del índice del desarrollo humano mayor de 0.75.

-- 2. Realizar una consulta donde se muestre el país, la región, el promedio de población, el promedio de días libres y el promedio del índice del desarrollo humano. Filtrar para los años más allá del 2000 y el género masculino.

-- 3. Creamos una consulta en donde categorizamos los países en base a los siguientes criterios
--Si el índice de desarrollo humano es mayor que 0.8 y sus días libre son más de 20 “Top Country”
--Si el índice de desarrollo humano está entre 0.7 y 0.8 y sus días libres son más de 15 “Medium Country”
--Si el índice de desarrollo humano es menor que 0.7 “Bottom Country”
--El resto “Other” Mostramos el país, el índice de desarrollo humano, el total de días libres y su categoría.  Filtramos los datos para los años 90. 


--Ejercicios SET OPERATORS

-- 1. Creamos una tabla donde unimos el resultado de dos consultas:
-- Seleccionamos el id del país y el año desde la tabla country_population y country_population_2021.

-- 2. Creamos una tabla en que solo mostremos aquellos países que se encuentran en la tabla de población y días libres.
-- Aquellos países que no estén en las dos no los mostramos.

-- 3. Creamos una tabla en que solo mostremos aquellos países que no se encuentren en las dos tablas de población y días libres.
-- Solo mostramos los países que no se encuentran en ambas tablas.

--PROYECTO ONU: PARTE 2
--------------------------------------------------------
-- Ejercicios CASE WHEN
-- 1. Creamos una categorización de los datos que identifica el año 2021 como “Current Year”, el año 2020 como “Previous Year” y el resto como “Otros” y mostramos el promedio de índice de desarrollo humano para estos tres categorías.


-- 2. Creamos una categorización de los datos que identifica los países del G7 como “G7” y el resto de países como “Otros”, hacemos un conteo del número de países y mostramos su promedio del índice de desarrollo humano y su renta per cápita. 
-- Filtramos la información para el año 2020 e incluimos solo los países con el índice de desarrollo humano no nulo.


-- 3. Creamos una categorización de los países basada en la esperanza de vida en 2020:
-- Mayor que 80 -> “Alta”
-- Entre 60 y 80 -> “Media”
-- Menor que 60 -> “Baja”.
-- Calculamos el promedio del índice de desarrollo humano para estas tres categorías y ordenamos los resultados por el promedio del HDI de forma ascendente.

-- Ejercicios VISTAS
-- 1. Crear una vista que muestre el promedio del índice de desarrollo humano, la esperanza de vida al nacer y la renta per capita por país y año.

-- 2. Utilizar la vista creada para mostrar el índice de desarrollo humano promedio por país y año.

--------------------------------------------------------

-- Ejercicios FUNCIONES DE VENTANA
-- 1. Crear una consulta que muestre el país, el año y el índice de desarrollo humano, junto con el índice de desarrollo humano del año anterior. Ordenar los resultados por país y año.

-- 2. Crear una consulta que muestre el país, el año y el índice de desarrollo humano (Human Development Index), junto con el promedio del índice de desarrollo humano para ese país a lo largo de todos los años disponibles. Utiliza una función de ventana para calcular el promedio del índice de desarrollo humano por país.


-- Ejercicios SUBQUERIES
-- 1. Crear una consulta donde se seleccione el país, el género y el promedio del índice de desarrollo humano. Mostrar solo aquellos países que tengan una población de más de 1 millón en 2020.

-- 2. Creamos una consulta donde seleccionamos el país, el género y el promedio del índice de desarrollo humano. Mostramos sólo el país con menor número de días libres del planeta. 

--------------------------------------------------------

-- Ejercicios TOP

-- 1. Obtener una lista con los 3 países con el mayor promedio de renta per capita para los años 90.

-- 2. Obtener una lista con los 5 países con el mayor promedio de años de escolarización para las mujeres en los años 2000.



