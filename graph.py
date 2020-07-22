import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
from os.path import join
from termcolor import colored
import json
import tools

acc=3
def printFloat(input):
    print(np.format_float_scientific(input,acc-1, sign=False,exp_digits=1), end= '\t')

def graph(outputDir):
    data = np.load(join(outputDir,'adj_matrix_750.npy'))
    coeff= np.load(join(outputDir,'coeff_matrix_750.npy'))
    data *= coeff ** 0.5
    data = data[:20,:20]


    # data = coeff
    nodes = data.shape[0]
    map =  tools.rev_list()
    # index=0
    # data = np.round(data,acc)
    # for arr in data:
    #     for i in range(len(arr)):
    #         if index==i:
    #
    #             print(colored(map[index][0][0:4], 'green'),end='\t')
    #         else:
    #             printFloat(arr[i])
    #     index+=1
    #     print()
    #     print()


    G=nx.DiGraph()
    G.add_nodes_from([i[0] for i in map[:nodes]])

    # levels = []
    # levels.append([map[0]])
    # visited = {map[0]}
    # while len(visted)<nodes:
    #     prevLevel = levels[-1]
    #     maxChildren = 5
    #     max

    seeds = 1
    for i in range(1,seeds):
        G.add_edge(map[i][0],map[0][0])


    for i in range(seeds,nodes):
        parent = np.argmax(data, axis=0)[i];
        G.add_edge(map[i][0],map[parent][0])


    nx.write_graphml(G, join("graph_output","reddit.graphml"))

    with open(join("website","graph.js"), 'w') as outfile:
        json_data = json.dumps(json_graph.node_link_data(G))
        outfile.write("graph = \'")
        outfile.write(json_data)
        outfile.write('\'')
    # with open(join("graph_output","nodes.json"), 'w') as outfile:
    #     json.dump(G.nodes(), outfile)
    #     print(G.nodes())

    # pos = nx.planar_layout(G)
    # nx.draw_networkx_nodes(G, pos, node_size=[i[1]/2e5 for i in map[:nodes]], node_color='blue')
    # nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edges(G, pos, node_size=[i[1]/1e6 for i in map[:nodes]],
    # arrows = True)
    # nx.draw_networkx(G, pos, with_label = True, node_color ='green')
    # plt.show()


    # levels = 6
    # shift = 1
    # hierarchy = [[] for _ in range(levels+1)]
    # for i in range(len(inDegree)):
    #     lev = (inDegree[i]+shift)*levels/inDegree.max()
    #     hierarchy[int(lev)].append(map[i])
    #
    # for arr in hierarchy:
    #     print(arr)

    # print(inDegree.max())
    # visited = [False]*nodes
    # count = 0
    # sorted = []
    # while count<nodes:
    #     minIndex = inDegree.argmin()
    #     sorted.append((minIndex,np.round(og_inDegree[minIndex],acc)))
    #     inDegree[minIndex] = 1e9
    #     for i in range(len(inDegree)):
    #         inDegree[i]-=data[minIndex,i]
    #     count+=1
    # print()
    # print()
    # print(sorted)



    # G = nx.from_numpy_matrix(np.matrix(data))
    # # print(list(nx.topological_sort(G)))
    # pos = nx.spring_layout(G)
    # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]
    # nx.draw_networkx_nodes(G, pos, node_size=250)
    #
    # # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge,
    #                        width=3)
    # nx.draw_networkx_edges(G, pos, edgelist=esmall,
    #                    width=1, alpha=0.1, edge_color='b', style='dashed')
    # nx.draw_networkx_labels(G,pos,map,font_size=10)
    # plt.axis('off')
    # plt.show()
