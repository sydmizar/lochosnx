# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 02:21:55 2020

@author: BALAMLAPTOP2
"""


import pandas as pd
import numpy as np
import geopy.distance

print("Reading hospitals and localities ...")
clues = pd.read_csv('data/clues_junio_2020.csv', encoding = 'utf-8-sig')
localities = pd.read_csv('data/localidades_mayo_2020.csv', encoding = 'utf-8-sig')

geo_distance = np.zeros((localities.shape[0], clues.shape[0]))

print("Calculating geographic distance between them ...")
index_l = 0
index_c = 0
for locality in localities.iterrows():
    print(locality['mapa'])
    coords_1 = (locality[1]['latitud'], locality[1]['longitud'])
    for clue in clues.iterrows():
        print(clue['clues'])
        coords_2 = (clue[1]['latitud'], clue[1]['longitud'])
        geo_distance[index_l][index_c] = geopy.distance.geodesic(coords_1, coords_2).km
        index_c += 1
    index_l += 1
    index_c = 0
    
df = pd.DataFrame(geo_distance, index=localities['mapa'], columns=clues['clues'])
df.to_csv('distance_localities_hospitals.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')

t_vector = [ round(x * 0.1, 1) for x in range(0, 10)]

print("Calculating effective distance between them")
for tetha in t_vector:
    effective_distance = np.zeros((localities.shape[0], clues.shape[0]))
    for locality in range(0,geo_distance.shape[0], 1):
        pop_1 = localities.iloc[locality]['pob_total']
        if pop_1 != '-':
            for clue in range(0, geo_distance.shape[1], 1):
                pop_2 = clues.iloc[clue]['total_camas']
                if pop_2 != 0:
                    effective_distance[locality][clue] = geo_distance[locality][clue]/(int(pop_1) * pop_2)**tetha
    dfaux = pd.DataFrame(effective_distance, index=localities['mapa'], columns=clues['clues'])
    dfaux.to_csv('effective_distance_'+str(tetha)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    