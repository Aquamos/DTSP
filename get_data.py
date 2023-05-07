import random
import json
import networkx as nx
import string


def self_generate_problem(n, max_distance, max_mass):
    distances = [[0 for _ in range(n)] for _ in range(n)]
    thau = [0 for _ in range(n)]
    mass = [0 for _ in range(n)]
    for i in range(n):
        thau[i] = round(random.randint(1, max_distance + 1), 2)
        mass[i] = round(random.randint(1, max_mass + 1), 2)
        for j in range(n):
            if i != j:
                distances[i][j] = round(random.randint(1, max_distance + 1), 2)
                distances[j][i] = distances[i][j]

    nodes = list(string.ascii_uppercase[:n])
    return nodes, distances, thau, mass


def read_problem_from_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    nodes = data['nodes']
    edges = [(edge['source'], edge['target'], {'distance': edge['distance']}) for edge in data['edges']]
    weights = data['weights']
    start_final_node = data['start']

    G = nx.Graph()
    G.add_nodes_from(nodes)
    for edge in edges:
        G.add_edge(edge[0], edge[1], distance=edge[2]['distance'])
        G.add_edge(edge[1], edge[0], distance=edge[2]['distance'])

    return nodes, G, weights, start_final_node


def read_problem_from_hardcode(nodes, edges, thau, weights, start_final_node="VH"):
    weights = {nodes[i]: weights[i] for i in range(len(nodes))}

    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            G.add_edge(nodes[i], nodes[j], distance=edges[i][j])

    nodes.insert(0, start_final_node)
    for i in range(1, len(nodes)):
        G.add_edge(start_final_node, nodes[i], distance=thau[i - 1])

    return G, weights, start_final_node
