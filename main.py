import json
import networkx as nx
from ant_colony_optimizer import AntColonyOptimizer
from graph_plot import draw_graph


def create_graph_from_json(file_name):
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

    return G, weights, start_final_node


def create_graph_from_hardcode():
    nodes = ["ATB", "Novus", "Silpo", "Fora", "Velyka Kyshenya"]
    edges = [
        [0, 15, 20, 10, 25],
        [15, 0, 10, 18, 30],
        [20, 10, 0, 8, 23],
        [10, 18, 8, 0, 15],
        [25, 30, 23, 15, 0]
    ]
    weights = [7, 10, 5, 8, 3]
    weights = {nodes[i]: weights[i] for i in range(len(nodes))}
    h_list = [10, 17, 8, 12, 15]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            G.add_edge(nodes[i], nodes[j], distance=edges[i][j])

    start_final_node = "VH"
    nodes.insert(0, start_final_node)
    for i in range(1, len(nodes)):
        G.add_edge(start_final_node, nodes[i], distance=h_list[i - 1])

    return G, weights, start_final_node


if __name__ == '__main__':

    try:
        file_name = 'data_ruslan.json'
        #G, weights, start_final_node = create_graph_from_json(file_name)
        G, weights, start_final_node = create_graph_from_hardcode()

        aco = AntColonyOptimizer(G, weights, start_final_node, num_ants=30, evaporation_rate=0.1, alpha=1, beta=2, q=1)
        shortest_path, shortest_path_length, iterations = aco.run(min_num_of_iterations=10)

        draw_graph(G, shortest_path)

        shortest_path.append(start_final_node)
        print(f'Number of iterations: {iterations}')
        print(f'Shortest path: {shortest_path}')
        print(f'Shortest path length: {shortest_path_length}')

    except FileNotFoundError:
        print("File not found!")
    except json.JSONDecodeError:
        print("Invalid JSON format!")
    except KeyError as e:
        print(f"Error: Key '{e}' not found in the JSON data")
    except Exception as e:
        print(f"An error occurred: {e}")

