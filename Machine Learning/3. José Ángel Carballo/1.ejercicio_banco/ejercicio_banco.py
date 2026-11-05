#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier
#from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from pandas.plotting import scatter_matrix
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import accuracy_score, auc, confusion_matrix, f1_score, precision_score, recall_score, roc_curve
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score
import pickle



def tramos(varib,varib_destino,tamanio,maximo,df):
    	df[varib_destino]=np.where(df[varib]==0,-1,(df[varib]//tamanio)*tamanio)
    	df[varib_destino]=np.where(df[varib_destino]>=maximo,maximo,df[varib_destino])


def pre_processing(df_bank):


	lista_numericas=['age','balance','duration','day','pdays','previous','campaign']
	lista_categoricas=['job','marital','education','contact','month','poutcome']
	categoricas_binarias = ['default','housing','loan']

	for j in categoricas_binarias:
    		df_bank[j] = [0 if x == 'no' else 1 for x in df_bank[j]]

	for k in lista_categoricas:
    		dummies = pd.get_dummies(df_bank[k],prefix=k)
    		df_bank = pd.concat([df_bank, dummies], axis=1)



	df_bank.month.replace(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),
                      (1,2,3,4,5,6,7,8,9,10,11,12),inplace=True)

	df_bank.education.replace(('primary','secondary','tertiary','unknown'),
                      (1,2,3,4),inplace=True)

	df_bank.marital.replace(('married','single','divorced'),
                      (1,2,3),inplace=True)

	df_bank.contact.replace(('cellular','unknown','telephone'),
                      (1,2,3),inplace=True)

	df_bank.poutcome.replace(('failure','unknown','other','success'),
                      (1,2,3,4),inplace=True)



	le = LabelEncoder()



	le.fit(df_bank.job.unique())
	le.classes_


	df_bank.job = le.transform(df_bank.job)



	## AGE (realizamos una variable con 3 rangos de edad y 3 variables con esos mismos rangos)
	df_bank['age_joven'] = df_bank['age'].apply(lambda x: 1 if x<=35 else 0)
	df_bank['age_adulto'] = df_bank['age'].apply(lambda x: 1 if x>35 & x<60 else 0)
	df_bank['age_jubilado'] = df_bank['age'].apply(lambda x: 1 if x>60 else 0)
	df_bank['age_new'] = df_bank['age'].apply(lambda x: 0 if x<=35 else (1 if x>35 and x<60 else(2)))  


	tramos('duration','duration_new',5,5000,df_bank) 
	df_bank['duration_new'] = df_bank['duration_new'].apply(lambda x: 0 if x<=0 else x)
	df_bank['duration_new2'] = df_bank['duration_new']//60

	## CAMPAIGN (observamos que la mitad de los datos están entre 1 y 2, creamos una nueva clase para el resto)
	df_bank['campaign_new'] = df_bank['campaign'].apply(lambda x: 0 if x<=15 else 1)
	df_bank['campaign_new2'] = df_bank['campaign'].apply(lambda x: 1 if x==1 else (2 if x==2 else(3))) 

	## PDAYS (casi todos los datos están en -1 (no contactado), por tanto, transformamos la variable en contactados y no contactados)
	df_bank['pdays_new5'] = df_bank['pdays'].apply(lambda x: 0 if x<=0 else (1 if x<7 else(2 if x>=7 and x<14 else(3))))
	df_bank['pdays_new'] = df_bank['pdays'].apply(lambda x: 0 if x==-1 else x)
	df_bank['pdays_new2'] = df_bank['pdays']//30
	df_bank['pdays'] = df_bank['pdays'].apply(lambda x: 0 if x==-1 else x)
	df_bank['pdays_new2'] = df_bank['pdays_new2'].apply(lambda x: 0 if x==-1 else x)
	tramos('pdays_new2','pdays_new3',2,14,df_bank) 
	df_bank['pdays_new3'] = df_bank['pdays_new3'].apply(lambda x: 0 if x<=0 else x)

	## PREVIOUS (al igual que anteriormente, la mayoría no han sido contactados anteriormente, creamos una variable binaria)
	df_bank['previous_new'] = df_bank['previous'].apply(lambda x: 0 if x == 0 else 1)
	df_bank['previous_new_2'] = df_bank['previous'].apply(lambda x: 0 if x == 0 else 1)
	tramos('previous','previous_new_2',2,10,df_bank) 
	df_bank['previous_new_2'] = df_bank['previous_new_2'].apply(lambda x: 0 if x<=0 else x)

	## BALANCE (en este caso, hacemos tramos de la variable)    
	tramos('balance','balance_new',500,10000,df_bank)
	df_bank['balance_new'] = df_bank['balance_new'].apply(lambda x: 0 if x<=0 else x)
	df_bank['balance_negativo'] = df_bank['balance'].apply(lambda x: 1 if x<=0 else 0)
	df_bank['balance_new2'] = df_bank['balance'].apply(lambda x: 0 if x<=100 else (1 if x>100 and x<=500 else(2 if x>500 and x<=2000 else(3 if x>2000 and x<10000 else(4)))))
	df_bank['balance'] = df_bank['balance'].apply(lambda x: 0 if x<=0 else x)

	## DAY (en este caso podemos crear una variable que calcule la quincena)
	tramos('day','day_new',15,31,df_bank)

	## JOB (podemos hacer una variable de empleado y no empleado)
	df_bank['job_new'] = df_bank['job'].apply(lambda x: 0 if x==11 or x ==6 or x==9  else 1)
	
	
	return df_bank



if __name__ == "__main__":

   df_bank=pd.read_csv('bank-full.csv', sep=';')
                                      
   x_test_preprocessed = pre_processing(df_bank)
   
   with open('modelo.pkl', 'rb') as file:

   	model5 = pickle.load(file)
   
   
   print(model5.predict(x_test_preprocessed))
   print("la clase 1 es la mejor")




