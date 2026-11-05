"""El objetivo de este archivo es ser capaz de empezar a trabajar con grafos en phyton. Entre otras tareas queremos

1. Generar redes aleatorias, de pequeño mundo y libres de escala con los 
parametros que hemos aprendido en clase
2. Visualizar estas redes de tamaño medio con algunos algoritmos de visualizacion
3. Ser capaz de leer redes desde otros ficheros distinguiendo si son desde un archivo excel, .net. glm, entre otras. Tambien generar redes famosas implementadas en phyton.

4. Analizar la distribucion del grado de manera descriptiva comparando con otras distribuciones.
5. Constrastar si el grafo es aleatorio.
6. Constrastar si el grafo es libre de escalaa.
7. Contrastar si el grao es de pequeño mundo

"""

import networkx as nx

### creamos un grafo y un digrafo en blanco G y G2
G = nx.Graph() 
G2 = G = nx.DiGraph() 

### añadimos un arco con peso 2 al grafo 
G.add_edge(1,2, weight=2)

## añadimos una lista de aristas sin valorar
elist = [(1,2), (2,3), (1,4), (4,2)]
G.add_edges_from(elist)

## añadimos una lista de aristas valoradas con nombre
elist = [('a', 'b', 5.0), ('b', 'c', 3.0), ('a', 'c', 1.0), ('c', 'd', 7.3)]
G.add_weighted_edges_from(elist)

## quitamos un subconjunto de aristas
quitar = [(1, 2), (2, 3)]
G.remove_edges_from(quitar)

## definomos una cadena de longitud 5
G = nx.path_graph(5)
list(G.nodes)
list(G.edges)
list(G)
G.edges.data("weight", default=1) ## ponemos peso 1 a todos los arcos por defecto
print(G.nodes)
print(G.edges)

"""Ahora vamos a generar un grafo aleatorio. 
El algoritmo de generacion escogido se conoce como binomial, 
ya que escogido el numero de nodos (10 en este caso) y 
la probabilidad de exito/enlace (p=0.4 en este caso), generamos el grafo. 
El numero esperado de aristas será de (n sobre 2) por p que en este caso 
es 45*0.4=18 aristas"""

import random
import matplotlib.pyplot as plt


## 1. grafo aleatorio con algoritmo binomial 
G = nx.binomial_graph(n=10, p=0.4, seed=1234, directed=False)


print(G[1]) ### lista de conexiones del nodo 1
print(G[9]) ### lista de conexiones del nodo 9

"""Para saber si un nodo en particular esta en el grafo se pregunta xx in G. 
Como en phyton empezamos desde 0 y el grafo tiene 10 nodos, el nodo 10 
no deberia estar

"""

10 in G ## deberia ser falso

# for n in G: iterates through the graph.
# for nbr in G[n]: iterates through neighbors
for n in G:
    print(G[n])
    
### info del grafo
print(len(G.nodes)) # 10 nodos
print(len(G.edges)) # 20 aristas
print(G.nodes)
print(G.edges)


"""**2. Ser capaz de leer redes **"""

import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import warnings


"""Ahora vamos a ver si podemos descargar algunas de las redes mas famosas. 
Karate, Miserables,..

"""
# https://networkx.org/documentation/stable/_modules/networkx/generators/social.html#florentine_families_graph
Florentine = nx.florentine_families_graph()
Karate = nx.karate_club_graph()
Miserables = nx.les_miserables_graph()
women = nx.davis_southern_women_graph()


print('El numero de nodos de la Red Florentine ') 
print(len(Florentine.nodes))
print('El numero de aristas es') 
print(len(Florentine.edges))


print('El numero de nodos de la Red Karate ') 
print(len(Karate.nodes))
print('El numero de aristas es') 
print(len(Karate.edges))


print('El numero de nodos de la Red Miserables ') 
print(len(Miserables.nodes))
print('El numero de aristas es') 
print(len(Miserables.edges))


print('El numero de nodos de la Red Davis women  ') 
print(len(women.nodes))
print('El numero de aristas es') 
print(len(women.edges))

"""Visualizaciones de las 4 redes"""

import matplotlib.pyplot as plt
nx.draw(Florentine, with_labels=True, node_size=25)
plt.title("Grafo de Florentine con visualizacion por defecto")
plt.show()

nx.draw(Karate, with_labels=True, node_size=25)
plt.title("Grafo de Karate con visualizacion por defecto")
plt.show()

nx.draw(Miserables, with_labels=True, node_size=25)
plt.title("Grafo de Les Miserables con visualizacion por defecto")
plt.show()

nx.draw(women, with_labels=True, node_size=25)
plt.title("Grafo de Davis women  con visualizacion por defecto")
plt.show()




"""**3. GENERANDO Y DIBUJANDO GRAFOS ALEATORIOS ERDOS RENYi y Barabasi Albert**"""

############################################
## 2. Grafo aleatorio Erdos renyi erdos_renyi_graph(n, p, seed=None, directed=False)
G = nx.erdos_renyi_graph(n=30, p=0.2, seed=123, directed=False) 
print(len(G.nodes))
print(len(G.edges))

nx.draw(G) # VISUALIZACION POR DEFECTO

"""El commando draw tiene muchisimas opciones, de las mas importantes 
es la posicion que ocupan sus nodos. 

"""

nx.draw(G, pos=nx.spring_layout(G), node_color='g', edge_color='b') ## ALGUNOS AJUSTES

"""Otras opciones....

"""

# Fruchterman Reingold
nx.draw(G, with_labels=True, node_size=15, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G))
plt.title("fruchterman_reingold")
plt.show()
 
# Circular
nx.draw(G, with_labels=True, node_size=25, node_color="b", pos=nx.circular_layout(G))
plt.title("circular")
plt.show()
 
# Random
nx.draw(G, with_labels=True, node_size=1, node_color="red", pos=nx.random_layout(G))
plt.title("random")
plt.show()
 
# Spectral
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.spectral_layout(G))
plt.title("spectral")
plt.show()
 
# Spring
nx.draw(G, with_labels=True, node_size=50, node_color="skyblue", pos=nx.spring_layout(G))
plt.title("spring")
plt.show()


G_barabasi = nx.barabasi_albert_graph(n=100,m=3,seed=123,initial_graph=None )
nx.draw(G_barabasi, with_labels=True, node_size=25, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G_barabasi))
plt.title("Grafo de Barabasi con visualizacion de fruchterman_reingold")
plt.show()
print('El numero de nodos es') 
print(len(G_barabasi.nodes))
print('El numero de aristas es') 
print(len(G_barabasi.edges))



"""4. Analizando la distribución del grado de un grafo.


La opción por defecto de phyton es la centralidad por grado relativa pero 
se puede obtener el grado como número de vecinos.

"""
### Medida de centralidad de grado relativa
deg_cen_GOT = nx.degree_centrality(Karate) ## network trabaja con diccionarios

### Desde un diccionario a un data frame
centralidad_data_frame = pd.DataFrame(deg_cen_GOT.values(), columns=['Centralidad'])
###

plt.hist(deg_cen_GOT.values(), bins=30)
plt.show()

"""A modo de comparativa vamos a generar una red aleatoria de las mismas 
caracteristicas que GOT para ver similitudes

"""
#GOT=nx.florentine_families_graph()
#GOT=nx.les_miserables_graph()
GOT=nx.karate_club_graph()

n_got=len(GOT.nodes)
m=len(GOT.edges)
p_got=(2*m)/(n_got*(n_got-1))
print(n_got,m,p_got)

GOT_random = nx.erdos_renyi_graph(n= n_got, p=p_got, seed=123, directed=False) 
print(len(GOT_random.nodes))
print(len(GOT_random.edges))

### Medida de centralidad de grado relativa
deg_cen_rand_GOT = nx.degree_centrality(GOT_random) ## network trabaja con diccionarios

### Desde un diccionario a un data frame
centralidad_data_frame_random = pd.DataFrame(deg_cen_rand_GOT.values(), columns=['Centralidad'])
###

plt.hist(deg_cen_rand_GOT.values(), bins=20)
plt.show()

"""La centralidad "bruta" se puede obtener a partir de la secuencia GOT.degree 

"""

#grado = GOT.degree(weight='weight') ## con pesos
grado = GOT.degree()
print(grado)

grado_random= GOT_random.degree(weight='weight')
print(grado_random)

"""De nuevo la salida es un diccionario que se puede transformar a Data Frame 
si queremos

"""

grado = pd.DataFrame(grado)
grado_random = pd.DataFrame(grado_random)
#print(grado)
print(grado.to_markdown(tablefmt="grid"))
plt.hist(grado[1], bins=25)
plt.show()

plt.hist(grado_random[1], bins=25)
plt.show()
# Podemos cambiar el nombre de las columnas 
#grado.columns = ['Personaje', 'Poder']



degree_sequence = sorted((d for n, d in GOT.degree()), reverse=True)
dmax = max(degree_sequence)
print(degree_sequence)

"""Pintamos de mayor a menor los grados de esta distribución para ver si hay 
muchos nodos con grado pequeño y pocos con grado alto..

"""

### analizando el grado GOT
degree_sequence = pd.DataFrame(degree_sequence)
type(degree_sequence )
degree_sequence.dtypes
x=np.arange(0,n_got)
y=degree_sequence[0]

# Plotting
plt.scatter(x, y)
plt.show()



"""TABLA DE FRECUENCIAS DEL GRADO  

Calculamos la distribución del grado, es decir \$(x_i,n_i)$\ para la variable X degree. 
Sin embargo no ordena las x_i de menor a mayor por lo que la tabla de frecuencia 
es un poco fea. 
"""
# Cojemos la variable numerica grado sin los nombres 
grado_v2=grado[1]
#grado.value_counts(sort=True)
print(grado_v2)

distribucion= grado_v2.value_counts(sort=False)
print(distribucion)

sorted_series = distribucion.sort_values(ascending = False)
print(sorted_series)

"""Con la opcion crosstab tenemos lo que queremos"""

tabla_frecuencia_grado=pd.crosstab(index=grado[1], columns='count')

print(tabla_frecuencia_grado)

plt.plot(tabla_frecuencia_grado) ## diagrama de barras de ni


"""5. Métodos analíticos para contrastar normalidad (Poisson)

Para una Red Aleatoria
"""

# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y análisis
# ==============================================================================
import statsmodels.api as sm
from scipy import stats

# Configuración matplotlib
# ==============================================================================
plt.style.use('ggplot')
# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

# Histograma + curva normal teórica
# ==============================================================================

degree=grado[1]


# Valores de la media (mu) y desviación típica (sigma) de los datos
mu, sigma = stats.norm.fit(degree)

# Valores teóricos de la normal en el rango observado
x_hat = np.linspace(min(degree), max(degree), num=100)
y_hat = stats.norm.pdf(x_hat, mu, sigma)

# Gráfico
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(x_hat, y_hat, linewidth=2, label='normal')
ax.hist(x=degree, density=True, bins=30, color="#3182bd", alpha=0.5)
ax.plot(degree, np.full_like(degree, -0.01), '|k', markeredgewidth=1)
ax.set_title('Distribución del grado ')
ax.set_xlabel('grado')
ax.set_ylabel('Densidad de probabilidad')
ax.legend();

"""Otra representación utilizada con frecuencia son los gráficos de 
cuantiles teóricos (Gráficos Q-Q). Estos gráficos comparan 
los cuantiles de la distribución observada con los cuantiles teóricos 
de una distribución normal con la misma media y desviación estándar que los datos. 
Cuanto más se aproximen los datos a una normal, más alineados están los puntos 
entorno a la recta."""

# Gráfico Q-Q
# ==============================================================================
fig, ax = plt.subplots(figsize=(7,4))
sm.qqplot(
    degree,
    fit   = True,
    line  = 'q',
    alpha = 0.4,
    lw    = 2,
    ax    = ax
)
ax.set_title('Gráfico Q-Q del grado en la GOT network ', fontsize = 10,
             fontweight = "bold")
ax.tick_params(labelsize = 7)

"""**Métodos analíticos asimetría y curtosis**

Los estadísticos de asimetría (Skewness) y curtosis pueden emplearse para 
detectar desviaciones de la normalidad. Un valor de curtosis y/o coeficiente 
de asimetría entre -1 y 1, es generalmente considerada una ligera desviación 
de la normalidad (Bulmer, 1979), (Brown, n.d.). 
Entre -2 y 2 hay una evidente desviación de la normal pero no extrema.
"""

print('Kursotis:', stats.kurtosis(degree))
print('Skewness:', stats.skew(degree))

"""**Contraste de hipótesis**

Los test Shapiro-Wilk test y D'Agostino's K-squared test son dos de los test 
de hipótesis más empleados para analizar la normalidad. En ambos, se considera 
como hipótesis nula que los datos proceden de una distribución normal.

El p-value de estos test indica la probabilidad de obtener unos datos como 
los observados si realmente procediesen de una población con una distribución 
normal con la misma media y desviación que estos. Por lo tanto, si el p-value 
es menor que un determinado valor (típicamente 0.05), entonces se considera 
que hay evidencias suficientes para rechazar la normalidad.

El test de Shapiro-Wilk se desaconseja cuando se dispone de muchos datos 
(más de 50) por su elevada sensibilidad a pequeñas desviaciones de la normal.
"""

# Shapiro-Wilk test
# ==============================================================================
shapiro_test = stats.shapiro(degree)
shapiro_test 

# D'Agostino's K-squared test
# ==============================================================================
k2, p_value = stats.normaltest(degree)
print(f"Estadístico = {k2}, p-value = {p_value}")


"""**6 Redes de pequeño mundo**

Algunas sentencias son:
newman_watts_strogatz_graph(n, k, p, seed=None)
watts_strogatz_graph (n, k, p, seed=None)
connected_watts_strogatz_graph(n, k, p, tries=100, seed=None)

Vamos a la pregunta importante, ¿Es una red de pequeño mundo?. 
Cuando sigma es mayor que 1 y omega cercano a 0

"""

G_watts = nx.watts_strogatz_graph (n=50, k=4, p=0.2, seed=123)
nx.draw(G_watts)
plt.title("Grafo de Watts Strogatz con visualizacion por defecto")
plt.show()


G=Karate
sigma_value=nx.sigma(G, niter=10, nrand=10, seed=None) ## valor estimado para pequeño mundo
print(sigma_value)

omega= nx.omega(G, niter=10, nrand=10, seed=None)
print (omega)

