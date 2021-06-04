# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 16:13:01 2021

@author: Irene López
@descrip: Código calculo de robustez
RED Municipios - Hospitales SSA
El enlace cuenta con un peso definido como el número de pacientes que se hospitalizaron en esa unidad
"""

import sys
import networkx as nx
from networkx.algorithms import bipartite
import collections
import pandas as pd
import random
import numpy as np


def nodestoremove(p, q, nodes_0_c, nodes_1_c, df_atc, df_icd, type_method):
    if type_method == 0:
        atcNodesToRemove = random.sample(nodes_1_c, int(round(p * len(nodes_1_c))))
        icdNodesToRemove = random.sample(nodes_0_c, int(round(q * len(nodes_0_c))))
    elif type_method == 1:
        atcNodesToRemove = list(df_atc.head(int(round(p * len(nodes_1_c))))['node'])
        icdNodesToRemove = list(df_icd.head(int(round(q * len(nodes_0_c))))['node'])
    
    return icdNodesToRemove, atcNodesToRemove

def printvalues(np_avg_degree, np_conn_nodes, np_unconn_nodes, np_conn_components, np_mean_size, i, p_vector):
    np_avg_degree_div = np.true_divide(np_avg_degree, i)
    np_conn_nodes_div = np.true_divide(np_conn_nodes, i)
    np_unconn_nodes_div = np.true_divide(np_unconn_nodes, i)
    np_conn_components_div = np.true_divide(np_conn_components, i)
    np_mean_size_div = np.true_divide(np_mean_size, i)
#    np_clustering_div = np.true_divide(np_clustering, i)
    
    print("Creating files ... ")
    df = pd.DataFrame(np_avg_degree_div, index=p_vector, columns=p_vector)
    df.to_csv('results/np_avg_degree_'+str(type_proj)+'_'+str(type_method)+'_'+str(i)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    
    df = pd.DataFrame(np_conn_nodes_div, index=p_vector, columns=p_vector)
    df.to_csv('results/np_conn_nodes_'+str(type_proj)+'_'+str(type_method)+'_'+str(i)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    
    df = pd.DataFrame(np_unconn_nodes_div, index=p_vector, columns=p_vector)
    df.to_csv('results/np_unconn_nodes_'+str(type_proj)+'_'+str(type_method)+'_'+str(i)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    
    df = pd.DataFrame(np_conn_components_div, index=p_vector, columns=p_vector)
    df.to_csv('results/np_conn_components_'+str(type_proj)+'_'+str(type_method)+'_'+str(i)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    
    df = pd.DataFrame(np_mean_size_div, index=p_vector, columns=p_vector)
    df.to_csv('results/np_mean_size_'+str(type_proj)+'_'+str(type_method)+'_'+str(i)+'.csv', index=True, header=True, sep=',', encoding = 'utf-8-sig')
    
if __name__ == '__main__':
    # Remover al azar 0 o dirigido 1
    # Proyección ICD 0 o ATC 1 
    type_method = int(sys.argv[1])
    type_proj = int(sys.argv[2])
    
    print("Reading file ...")    

    data = pd.read_csv('data/lochosnx-robustez.csv')
    
    data['entresidencia'] = data.entresidencia.apply(lambda x: str(x).zfill(2))
    data['munresidencia'] = data.munresidencia.apply(lambda x: str(x).zfill(3))
    
    data['cvegeo'] = data['entresidencia'] + data['munresidencia']
    
    nodes_0 = list(dict.fromkeys(unique(data.cvegeo)))
    nodes_1 = list(dict.fromkeys(unique(data.clues)))
    
    print("Building a bipartite graph ...")
    # Build a bipartite graph:
    G = nx.Graph()
    # Add nodes ATC - ICD
    G.add_nodes_from(nodes_0, bipartite=0) # Add the node attribute “bipartite” disease
    G.add_nodes_from(nodes_1, bipartite=1) # active substance
    
    

