import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def make_graph(ent_dict,qubit_list):
    G = nx.Graph()
    G.add_nodes_from(qubit_list)
    for i in range(len(qubit_list)):
        for j in range(i+1,len(qubit_list)):
                if ent_dict[(i,j)] != 0.0:
                    G.add_edge(i,j,weight=ent_dict[(i,j)]*10)
                
    return G

def draw_ent_graph(ent_dict,qubit_list,layout="circular"):
    G=make_graph(ent_dict,qubit_list)
    valid_layout = {"circular","spring"}
    if layout not in valid_layout:
            raise ValueError("Not a valid layout name (circular,spring).")
    
    if layout == "circular":
        pos = nx.circular_layout(G, dim=2, scale=1, center=None)
    if layout == "spring":
        pos = nx.spring_layout(G)
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]
    nodesize = [e[1]*100 for e in G.degree(weight='weight')]
    print(nodesize)
    plt.figure(1)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=nodesize)
    nx.draw_networkx_edges(G, pos, width=edgewidth)
    nx.draw_networkx_labels(G,pos)
    

#test_list=np.arange(4).tolist()
#test_dict= {(0,1): 0.1,
#            (1,2): 0.2,
#            (0,2): 0.3,
#            (0,3): 0,
#            (1,3):0.7,
#            (2,3):0.1
#            }

draw_ent_graph(,)


