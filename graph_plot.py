import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, shortest_path):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=1000)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    nx.draw_networkx_edges(G, pos, edgelist=list(zip(shortest_path, shortest_path[1:])) +
                            [(shortest_path[-1], shortest_path[0])],
                            edge_color='b', width=2, arrows=True, arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['distance'] for u, v in G.edges()},
                                 label_pos=0.45)
    plt.axis('off')
    plt.show()
