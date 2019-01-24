import numpy as np
import matplotlib.pyplot as plt

def print_graph(vertices, edges, print_dist=False):
  for v in vertices:
    print("Vertex name: ", v)
    if not print_dist:
      for e in edges:
        if e[0] == v:
          print("-> ", e[1])
    else:
      for e in edges:
        if e[0] == v:
          print("-> ", e[1], e[2])

def print_graph_nx(vertices, edges, print_dist=False):
  import networkx as nx
  G=nx.DiGraph()
  labels = []

  for v in vertices:
    G.add_node(v)

  for v in vertices:
    for e in edges:
      G.add_edge(e[0], e[1], weight=int(e[2]))
      #labels += [(e[0], e[1]), e[2]]

  print("Nodes of graph: ")
  print(G.nodes())
  print("Edges of graph: ")
  print(G.edges())

  nx.draw(G, with_labels=True, node_color='y')
  #nx.draw_networkx_edge_labels(G,labels)
  plt.savefig("simulation_graph.png") # save as png
  plt.show()
