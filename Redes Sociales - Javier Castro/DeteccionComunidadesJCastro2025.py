"""DETECCION DE COMUNIDADES ALGORITMOS MAS CONOCIDOS

El primer algoritmo que vamos a obtener el famoso algoritmo jerarquico divisivo de **Girvan and Newman** basado en la centralidad por intermediacion de las aristas. 
El algoritmo aplicado a una estructura tipo grafo nos da un objeto llamado generator
"""
import networkx as nx
import matplotlib.pyplot as plt

## empezamos con algunos grafos famoso 

Florentine = nx.florentine_families_graph()
Karate = nx.karate_club_graph()
Miserables = nx.les_miserables_graph()
women = nx.davis_southern_women_graph()
Krack = nx.krackhardt_kite_graph()

G=nx.karate_club_graph() 

'''Algoritmo de Girvan Newman'''

from networkx.algorithms import community
## algoritmo que nos da un objeto llamado generator que hay que tunear para tener la particion
# la funcion next ofrence las comunidades como una lista de conjuntos
communities_generator = community.girvan_newman(G)
##como el algoritmo es jerarquico divisivo podemos ir sacando las particiones desde el inicio hasta el final

primer_corte = next(communities_generator) ## primer corte
print(primer_corte)

## segundo corte ## 
segundo_corte = next(communities_generator)
#sorted(map(sorted, segundo_corte)) ## particion

import networkx.algorithms.community as nx_comm
modularidad_GN= nx_comm.modularity(G, primer_corte, weight='weight', resolution=1)
print('la modularidad para dos comunidades es  ' , modularidad_GN)

modularidad_GN= nx_comm.modularity(G, segundo_corte, weight='weight', resolution=1)
print('la modularidad para tres comunidades es  ' , modularidad_GN)

primer_corte[0] # devuelve la comunidad numero 1 de la primera iteracion
primer_corte[1] # devuelve la comunidad numero 2 de la primera iteracion

segundo_corte[0] # devuelve la comunidad numero 1 de la segunda iteracion
segundo_corte[1] # devuelve la comunidad numero 2 de la segunda iteracion
segundo_corte[2] # devuelve la comunidad numero 3 de la segunda iteracion

"""PINTANDO GIRVAN AND NEWMAN. 

Coloreamos cada elemento de la comunidad optima con un color y la dibujamos. 
Ojo, solo estamos coloreando next(comunidades) que es la primera iteracion del algoritmo.


"""

G = nx.karate_club_graph()
communities = community.girvan_newman(G) ## comunidades jerarquicas de GN

node_groups = []
for com in next(communities):
    node_groups.append(list(com))

print(node_groups) ## LISTA DE ARRAYS, CADA ELEMENTO DE LA LISTA ES UN VECTOR QUE TIENE TODOS LOS MIEMBROS DE la comunidad

## pintamos el primer corte

color_map = []
for node in G:
    if node in node_groups[0]:
        color_map.append("red")
    else:
        color_map.append("orange")
nx.draw(G, node_color=color_map, with_labels=True)
plt.show()

node_groups[0]

"""¿INTENTAMOS PINTAR LA SIGUIENTE ITERACION?"""

G = nx.karate_club_graph()
communities = community.girvan_newman(G)
lol = next(communities) # SIMPLEMENTE APLICAMOS UNA ITERACION PARA EMPEZAR POR LA SEGUNDDAA
node_groups = []
for com in next(communities):
    node_groups.append(list(com))

print(node_groups) ## LISTA DE ARRAYS, CADA ELEMENTO DE LA LISTA ES UN VECTOR QUE TIENE TODOS LOS MIEMBROS DE LA COMUNIDAD
# AHORA TRESS COMUNIDADES

color_map = []
for node in G:
    if node in node_groups[0]:
        color_map.append("red")
    if node in node_groups[1]:
        color_map.append("blue")    
    if node in node_groups[2]:
        color_map.append("orange")
nx.draw(G, node_color=color_map, with_labels=True)
plt.show()

"""El algoritmo de GN al ser jerarquico puede ser muy lengo. 
Existe la opción que nos muestre unicamente las comunidades hasta un valor 
maximo pero es necesario cargar la libreria itertools"""

### deteccion de comunidades ###
import networkx as nx
from networkx.algorithms import community
import itertools

G=nx.karate_club_graph()

#G = nx.path_graph(8)
k = 4
comp = community.girvan_newman(G)

limited = itertools.takewhile(lambda c: len(c) <= k, comp) ## fijamos el numero maximo de comunidades en 4
for communities in limited:
 print(tuple(sorted(c) for c in communities))

"""Como curiosidad del algoritmo de GN, podemos ver/ordenar las aristas que 
tienen mayor centralidad por intermediacion que son por las que suele cortar el algoritmo"""

from networkx import edge_betweenness_centrality
from random import random
G=nx.les_miserables_graph()
centrality = edge_betweenness_centrality(G)
sorted_centrality = dict(sorted(centrality.items(), key=lambda item:item[1])) ## ordenamos de menos a mas centralidad
print(sorted_centrality)

max_cent = max(centrality.values()) ## el maximo
print(max_cent)



''' Louvain '''

from networkx.algorithms import community
import networkx.algorithms.community as nx_comm

G = nx.karate_club_graph()

LouvainMejor=nx_comm.louvain_communities(G, weight='weight', resolution=1)
print(LouvainMejor)
modularidad_Lo= nx_comm.modularity(G, LouvainMejor, weight='weight', resolution=1)
print('la modularidad para lovain es  ' , modularidad_Lo)


'''pintamos los grupos'''

'''listado de colores'''
import matplotlib
for cname, hex in matplotlib.colors.cnames.items():
    print(cname,hex)

'''ajustamos al número de colores que tenemos, se puede hacer más general 
con un buble y un listado de colores amplio'''
color_map = []
for node in G:
    if node in LouvainMejor[0]:
        color_map.append("red")
    if node in LouvainMejor[1]:
        color_map.append("blue")    
    if node in LouvainMejor[2]:
        color_map.append("orange")
    if node in LouvainMejor[3]:
        color_map.append("maroon")
'''    if node in LouvainMejor[4]:
       color_map.append("teal")    
    if node in LouvainMejor[5]:
       color_map.append("lime")
    if node in LouvainMejor[6]:
       color_map.append("yellow")
    if node in LouvainMejor[7]:
       color_map.append("violet")    
    if node in LouvainMejor[8]:
       color_map.append("silver")
    if node in LouvainMejor[9]:
      color_map.append("pink")
    else:
      color_map.append("black")    
'''   

nx.draw(G, node_color=color_map, with_labels=True)
plt.show()





"""Otros algoritmos de deteccion de comunidades CLAUSET NEWMAN & MOORE"""

from networkx.algorithms.community import greedy_modularity_communities
import networkx as nx
G = nx.karate_club_graph()
CNM_comunidades=greedy_modularity_communities(G) ## Clauset NEWMAN and Moore
print(CNM_comunidades)

import networkx.algorithms.community as nx_comm

modularidad3 = nx_comm.modularity(G,CNM_comunidades)
print("La modularidad del algoritmo de Clauset Newman and Moore  es  {}".format(modularidad3))

color_map = []
for node in G:
    if node in CNM_comunidades[0]:
        color_map.append("red")
    if node in CNM_comunidades[1]:
        color_map.append("blue")    
    if node in CNM_comunidades[2]:
        color_map.append("orange")


nx.draw(G, node_color=color_map, with_labels=True)
plt.show()




'''OBTENIENDO SUBGRAFOS DESDE UNA PARTICION. 


En muchas ocasiones estaremos interesados en pintar o analizar unicamente 
una comunidad de las muchas que hemos obtenido dentro del grafo, por este 
motivo es importante ser capaz de generar otro grafo a partir de un subsonjunto de nodos. 
La operacion natural es con induced subgraof
'''

G = nx.path_graph(4) # 
plt.title("Grafo cadena de 4 nodos ")
nx.draw(G, with_labels=True)
plt.show()

B=[0, 1, 3] # sobconjunto de nodos
H = nx.induced_subgraph(G,B )
plt.title("Subgrafo Inducido por los nodos 0,1,3 ")
nx.draw(H, with_labels=True)
plt.show()

"""Desde una salida de las anteriores"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()

LouvainMejor=nx_comm.louvain_communities(G, weight='weight', resolution=1)
print(LouvainMejor)

# creamos una lista con la comunidad deseada, por ejemplo la primera, la 0
C0=[]
for nodes in G:
 if nodes in LouvainMejor[0]: # comunidad 0 
  C0.append(nodes)
print(C0)

H = nx.induced_subgraph(G,C0)
plt.title("Subgrafo Inducido por los nodos de la omponente 0 ")
nx.draw(H, with_labels=True)
plt.show()


'''Como medir la importancia de un cluster (por ejemplo para el cluster 0)'''

'''Por la consistencia interna (número de aristas en su interior)'''
'''Primero generamos el subgrafo de la componente conexa como hemos indicado antes
y luego le pedimos el número de arcos. Si deseamos lo podemos poner en porcentaje'''
PoderInterno=len(H.edges)
print(PoderInterno)
PoderInternoRelativoTotal=len(H.edges)/len(G.edges)
print(PoderInternoRelativoTotal)
PoderInternoRelativoParcial=len(H.edges)/len(H.nodes)
print(PoderInternoRelativoParcial)


'''Por la capacidad de intermediar con otros grafos (número de aristas entre ese
cluster y otros cluster)'''
'''Generamos la suma del grado en los elementos de ese cluster y le restamos dos 
veces la aristas internas, dejando entonces las aristas externas'''

degree=G.degree()
#wdegree=G.degree(weight='weight')
Total=0
for nodes in G:
 if nodes in LouvainMejor[0]: # comunidad 0 
  Total=Total+degree(nodes)
print(Total)
PoderIntermediacion=Total-2*PoderInterno
print(PoderIntermediacion)
PoderIntermediacionRelativoTotal=PoderIntermediacion/len(G.edges)
print(PoderIntermediacionRelativoTotal)
PoderIntermediacionRelativoParcial=PoderIntermediacion/len(H.nodes)
print(PoderIntermediacionRelativoParcial)


'''Por la poder global de sus miembros (suma del poder de sus miembros)'''
'''Sumamos la magnitud de centralidad que deseemos (o la agregación de ellas)'''

Total=0
for nodes in G:
 if nodes in LouvainMejor[0]: # comunidad 0 
  Total=Total+pd.DataFrame(dat_centralidad_Por)['AgregacionPor'][nodes]
print(Total)


PoderTotal=Total/100
print(PoderTotal)
PoderTotalRelativoParcial=PoderTotal/len(H.nodes)
print(PoderTotalRelativoParcial)

'''Si deseamos hacerlo para todos podemos hacerlo con un bucle for
for i in range(11): poniendo en el valor de rango el número de cluster
y haciedo que Total y PoderTotalRelativo sea una lista'''
Total=[]
for i in range(4):
 Total.append(0)
 for nodes in G:
  if nodes in LouvainMejor[i]: # comunidad 0 
   Total[i]=Total[i]+pd.DataFrame(dat_centralidad_Por)['AgregacionPor'][nodes]
print(Total)

PoderTotal=[]
for i in range(4):
 PoderTotal.append(0)   
 PoderTotal[i]=Total[i]/100
print(PoderTotal)