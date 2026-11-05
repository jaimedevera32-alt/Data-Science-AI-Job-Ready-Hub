
''' Centralidad en redes sociales'''
import networkx as nx
import matplotlib.pyplot as plt

## empezamos con algunos grafos famoso 

Florentine = nx.florentine_families_graph()
Karate = nx.karate_club_graph()
Miserables = nx.les_miserables_graph()
women = nx.davis_southern_women_graph()
Krack = nx.krackhardt_kite_graph()

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

nx.draw(Krack, with_labels=True, node_size=25)
plt.title("Grafo de David Krackhardt con visualizacion por defecto")
plt.show()

#G=Miserables
G=Karate
pos = nx.spring_layout(G, seed=367)  # Semilla para que siempre salga lo mismo
nx.draw(G, pos)
plt.show()



"""Observación. El grado como medida de centralidad que obtiene la libreria 
Networkx es el grado relativo, donde se divide entre el grado maximo posible. 
Si se quiere obtener el grado absoluto basta multiplicar por (n-1).
"""
deg_centrality = nx.degree_centrality(G)
print(deg_centrality)
grado = G.degree()
print(grado)
""" por defecto sale sin pesos, si queremos que sume los pesos de los vecinos
debemos añadirlo"""
grado = G.degree()


"""grado, grado ponderado,Closeness centrality; betweneess centrality (load centrality), 
eigenvector centrality, pagerank, Hub and Authority..."""

degree = nx.degree_centrality(G)
#degree = degree*len(G)
degree=G.degree
wdegree=G.degree(weight='weight')
closeness = nx.closeness_centrality(G)
betweenness =nx.betweenness_centrality(G) 
load_centrality =nx.load_centrality(G) 
eigenvector_centrality = nx.eigenvector_centrality(G)
#pagerank_centrality = nx.pagerank(G, alpha = 0.8)
#hits(G, max_iter=10000, tol=1e-06, nstart=None, normalized=True)

#pagerank_centrality = nx.pagerank(G, alpha=0.8, ersonalization=None, max_iter=100, tol=1e-06, nstart=None, dangling=None)

#paso a dicionario la lista
#wdegreeDic={n:g for (n,g) in list(wdegree)}
#degreeDic={n:g for (n,g) in list(degree)}

degreeDic=dict(degree)
wdegreeDic=dict(wdegree)
"""Si queremos tenerlo todo en un data frame para poder hacer una analisis descriptivo 
o de correlaciones podemos hacer lo siguiente:
a) Generamos un data frame unidimensional con cada una de las medidas de centralidad
b) Juntamos todas las variables en una unica tabla con el comando "concat"
"""

import pandas as pd
aux_grado = pd.DataFrame.from_dict(degreeDic, orient='index',columns=['Grado'])
aux_wgrado= pd.DataFrame.from_dict(wdegreeDic, orient='index',columns=['GradoPonderado'])
aux_clo = pd.DataFrame.from_dict(closeness, orient='index',columns=['Cercania'])
#df.insert(1, "bar", df["one"])
aux_bet=pd.DataFrame.from_dict(betweenness, orient='index',columns=['Intermediacion'])
aux_load=pd.DataFrame.from_dict(load_centrality, orient='index',columns=['Load'])
aux_auto=pd.DataFrame.from_dict(eigenvector_centrality, orient='index',columns=['Autovalor'])


# G is the Karate Social Graph

dat_centralidad = pd.concat([aux_grado,aux_wgrado,aux_clo, aux_bet, aux_load,aux_auto], axis=1)
#centralidad.merge(aux_bet, on="index", how="left")

display(dat_centralidad)

'''podemos ponerlo todo en la misma escala con porcentajes'''

dat_centralidad_Por=dat_centralidad.copy(deep=True)
sum_grado = pd.DataFrame(dat_centralidad)['Grado'].sum()
sum_wgrado = pd.DataFrame(dat_centralidad)['GradoPonderado'].sum()
sum_clo = pd.DataFrame(dat_centralidad)['Cercania'].sum()
sum_bet = pd.DataFrame(dat_centralidad)['Intermediacion'].sum()
sum_load = pd.DataFrame(dat_centralidad)['Load'].sum()
sum_auto = pd.DataFrame(dat_centralidad)['Autovalor'].sum()

pd.DataFrame(dat_centralidad_Por)['GradoPor']=(pd.DataFrame(dat_centralidad_Por)['Grado']/sum_grado)
pd.DataFrame(dat_centralidad_Por)['GradoPonderadoPor']=(pd.DataFrame(dat_centralidad_Por)['GradoPonderado']/sum_wgrado)
pd.DataFrame(dat_centralidad_Por)['CercaniaPor']=(pd.DataFrame(dat_centralidad_Por)['Cercania']/sum_clo)
pd.DataFrame(dat_centralidad_Por)['IntermediacionPor']=(pd.DataFrame(dat_centralidad_Por)['Intermediacion']/sum_bet)
pd.DataFrame(dat_centralidad_Por)['LoadPor']=(pd.DataFrame(dat_centralidad_Por)['Load']/sum_load)
pd.DataFrame(dat_centralidad_Por)['AutovalorPor']=(pd.DataFrame(dat_centralidad_Por)['Autovalor']/sum_auto)

pd.DataFrame(dat_centralidad_Por)['AgregacionPor']=\
    (pd.DataFrame(dat_centralidad_Por)['GradoPor']*0.2)+\
    (pd.DataFrame(dat_centralidad_Por)['GradoPonderadoPor']*0.4)+\
    (pd.DataFrame(dat_centralidad_Por)['CercaniaPor']*0.1)+\
    (pd.DataFrame(dat_centralidad_Por)['IntermediacionPor']*0.1)+\
    (pd.DataFrame(dat_centralidad_Por)['LoadPor']*0.1)+\
    (pd.DataFrame(dat_centralidad_Por)['AutovalorPor']*0.1)
pd.DataFrame(dat_centralidad_Por)['AgregacionPor']=100*pd.DataFrame(dat_centralidad_Por)['AgregacionPor']
display(dat_centralidad_Por)

'''podemos ponerlo todo en la misma escala con índices'''


dat_centralidad_ind=dat_centralidad.copy(deep=True)
mean_grado = pd.DataFrame(dat_centralidad)['Grado'].mean()
mean_wgrado = pd.DataFrame(dat_centralidad)['GradoPonderado'].mean()
mean_clo = pd.DataFrame(dat_centralidad)['Cercania'].mean()
mean_bet = pd.DataFrame(dat_centralidad)['Intermediacion'].mean()
mean_load = pd.DataFrame(dat_centralidad)['Load'].mean()
mean_auto = pd.DataFrame(dat_centralidad)['Autovalor'].mean()


pd.DataFrame(dat_centralidad_ind)['GradoInd']=pd.DataFrame(dat_centralidad_ind)['Grado']/mean_grado
pd.DataFrame(dat_centralidad_ind)['GradoPonderadoInd']=pd.DataFrame(dat_centralidad_ind)['GradoPonderado']/mean_wgrado
pd.DataFrame(dat_centralidad_ind)['CercaniaInd']=pd.DataFrame(dat_centralidad_ind)['Cercania']/mean_clo
pd.DataFrame(dat_centralidad_ind)['IntermediacionInd']=pd.DataFrame(dat_centralidad_ind)['Intermediacion']/mean_bet
pd.DataFrame(dat_centralidad_ind)['LoadInd']=pd.DataFrame(dat_centralidad_ind)['Load']/mean_load
pd.DataFrame(dat_centralidad_ind)['AutovalorInd'] =pd.DataFrame(dat_centralidad_ind)['Autovalor']/mean_auto
pd.DataFrame(dat_centralidad_ind)['AgregacionInd']=\
    pd.DataFrame(dat_centralidad_ind)['GradoInd']*0.2+\
    pd.DataFrame(dat_centralidad_ind)['GradoPonderadoInd']*0.4+\
    pd.DataFrame(dat_centralidad_ind)['CercaniaInd']*0.1+\
    pd.DataFrame(dat_centralidad_ind)['IntermediacionInd']*0.1+\
    pd.DataFrame(dat_centralidad_ind)['LoadInd']*0.1+\
    pd.DataFrame(dat_centralidad_ind)['AutovalorInd']*0.1
    
display(dat_centralidad_ind)


print(dat_centralidad_ind["AgregacionInd"])
b = dat_centralidad_ind["AgregacionInd"]
for v in G.nodes():
    print(f"{v:2} {b[v]:.3f}")



"""**VISUALIZANDO NODOS RELEVANTES**

Aunque existen algunos tutoriales interesantes sobre como tener en cuenta la centralidad de los nodos para dibujar la red, en general los mas extendidos son:

a) Hacer que el tamaño sea proporcional a la centralidad. 

b) Hacer que los colores frios/calidos representen los nodos con mayor centralidad. 

"""

nx.draw(Miserables, with_labels=True, node_size=25)
plt.title("Grafo de Les Miserables con visualizacion por defecto: Todos los nodos iguales")
plt.show()

grado=Miserables.degree()
d=dict(Miserables.degree)

"""Creamos una variable (el formato es tipo lista) que sea proporcional al grado. Por ejemplo el grado por 5. Para los que empiezan con Phyton con la opcion d.values() accedes a los valores de un dicccionario asociados a la clave. Asi en el siguiente bucle cuando hacemos "for n in d.values()" estamos escogiendo todos los grados."""

tamaño=[n * 10 for n in d.values()]
print(tamaño)

nx.draw(Miserables, node_size=tamaño, pos=nx.fruchterman_reingold_layout(Miserables),alpha=0.5, width=0.5 )
plt.title("Grafo de Les Miserables con tamaño proporcional al grado ")
plt.show()
plt.savefig("Miserables.jpg")

nx.draw(Miserables, node_color=tamaño, node_size=30, alpha=0.5, width=0.5)
plt.title("Grafo de Les Miserables con color proporcional al grado ")
plt.show()
