﻿from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
get_ipython().run_line_magic('matplotlib', 'inline')

def com_member(tag_dict):
    member=defaultdict(list)
    for i in tag_dict.keys():
        member[tag_dict[i]].append(i)
    return(member)

def modularity(tag_dict,map_dict):
    #根据tag和图的连接方式计算模块度
    m = 0
    community_dict = defaultdict(list)
    #同属一个社群的人都有谁
    for key in map_dict.keys():
        m += map_dict[key].__len__()
        community_dict[tag_dict[key]].append(key)
    Q = 0
    for com in community_dict.keys():
        sum_in = 0
        sum_tot = 0
        for u in community_dict[com]:
            sum_tot+=map_dict[u].__len__()
            for v in map_dict[u]:
                if(tag_dict[v]==tag_dict[u]) :
                    sum_in+=1;
        Q += (sum_in/m-(sum_tot/m)**2)
    return Q

def changeTagRound(tag_dict2,map_dict2,Q):
    global tag_dict
    for u in map_dict2.keys():
        for v in map_dict2[u]:
            tag_dict_copy=tag_dict.copy()
            tag_dict2_copy = dict(tag_dict2)
            tag_dict2_copy[u]=tag_dict2_copy[v]
            for p in member[u]:
                tag_dict_copy[p]=tag_dict2_copy[v]
            Q_new = modularity(tag_dict_copy,map_dict)
            if(Q_new>Q):
                Q = Q_new
                tag_dict=tag_dict_copy
                tag_dict2=tag_dict2_copy
                #print(tag_dict)
                #print('\n')
    return Q,tag_dict,tag_dict2

def rebuildMap(tag_dict,map_dict):
    #将一个社区作为一个节点重新构造图
    map2 = defaultdict(list)
    for u in map_dict.keys():
        tagu = tag_dict[u]
        for v in map_dict.keys():
            tagv = tag_dict[v]
            if(tagu!=tagv and (map_dict[u].count(v)!=0) and (map2[tagu].count(tagv)==0)) :
                map2[tagu].append(tagv)
                #map2[tagv].append(tagu)
                #print(u,v, map2)
    tag2 = dict(zip(map2.keys(),map2.keys()))
    return tag2,map2

def readData(filename):
    graph = defaultdict(list)
    f = open(filename,'r')
    for line in f.readlines():
        line= line.strip('\n').split(' ')
        u,v = int(line[0]),int(line[1])
        graph[u].append(v)
        graph[v].append(u)
    return graph

def read_txt(data):
    g = nx.read_edgelist(data, create_using=nx.Graph())
    nx.draw(g,pos=nx.random_layout(g),with_labels=True,font_color='w',node_size=100,font_size=10)

map_dict=readData('C:\\Users\\李威\Desktop\\test_data.txt')
tag_dict = dict(zip(map_dict.keys(),map_dict.keys()))
member=com_member(tag_dict)
Q = 0
Q_new = modularity(tag_dict,map_dict)
tag_dict2=tag_dict
map_dict2=map_dict
while(Q != Q_new):
    Q = Q_new
    Q_new,tag_dict,tag_dict2 = changeTagRound(tag_dict2,map_dict2,Q)
    member=com_member(tag_dict)
    tag_dict2,map_dict2 = rebuildMap(tag_dict,map_dict)
print(member)
print(Q)