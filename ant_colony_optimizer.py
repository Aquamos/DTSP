import random


class AntColonyOptimizer:

    def __init__(self, G, weights, start_final_node, num_ants=10, evaporation_rate=0.1, alpha=1, beta=2, q=1):
        """
        :param G: the graph
        :param weights: additional parameter for each node
        :param start_final_node: the node where all ants start
        :param num_ants: number of ants
        :param evaporation_rate: the rate at which the pheromone trail evaporates
        :param alpha: larger -> more importance of the pheromone trail, lower -> more importance of heuristic
        :param beta: larger -> more importance of the pheromone trail, lower -> more importance of the distance
        :param q: affects the pheromone update rule
        """

        self.G = G
        self.start_final_node = start_final_node
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.q = q
        self.weights = weights
        self.pheromone = {(u, v): 1 for u, v in G.edges()}
        for u, v in G.edges():
            self.pheromone[(u, v)] = 1.0
            self.pheromone[(v, u)] = 1.0

    def run(self, min_num_of_iterations=10, threshold=0.001):
        shortest_path_length = float('inf')
        shortest_path = []
        iterations = 0
        prev_shortest_path_length = 0  # initialize variable with default value
        while iterations < min_num_of_iterations or (
                abs((shortest_path_length - prev_shortest_path_length) / prev_shortest_path_length) >= threshold):
            iterations += 1
            paths = []
            path_lengths = []
            for ant in range(self.num_ants):
                path = self._construct_path()
                paths.append(path)
                path_lengths.append(self._calculate_path_length(path))
                self._update_pheromone(path, path_lengths[-1])
            best_path_length = min(path_lengths)
            if best_path_length < shortest_path_length:
                shortest_path_length = best_path_length
                shortest_path = paths[path_lengths.index(shortest_path_length)]
            self._evaporate_pheromone()
            prev_shortest_path_length = shortest_path_length
        return shortest_path, shortest_path_length, iterations

    def _construct_path(self):
        path = [self.start_final_node]
        for i in range(1, self.G.number_of_nodes()):
            node = self._select_next_node(path[-1], path)
            path.append(node)
        return path

    def _select_next_node(self, node, path):
        pheromone_sum = sum(
            [self.pheromone[(node, neighbor)] ** self.alpha * ((1 / self.G[node][neighbor]['distance']) ** self.beta)
             for neighbor in self.G.neighbors(node) if neighbor not in path])
        if pheromone_sum == 0:
            return random.choice(list(self.G.neighbors(node)))
        probabilities = [(self.pheromone[(node, neighbor)] ** self.alpha * (
                (1 / self.G[node][neighbor]['distance']) ** self.beta)) / pheromone_sum if neighbor not in path else 0
                         for neighbor in self.G.neighbors(node)]
        if all(prob == 0 for prob in probabilities):
            return random.choice(list(self.G.neighbors(node)))
        return random.choices(list(self.G.neighbors(node)), probabilities)[0]

    def _calculate_path_length(self, path):
        load = 0
        cum_weight = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if i == 0:
                load = 0
            else:
                load = load + (self.G[u][v]['distance'] * (self.weights[u]+cum_weight))
                cum_weight += self.weights[u]
        load += self.G[path[-1]][self.start_final_node]['distance'] * (self.weights[path[-1]] + cum_weight)
        return load

    def _update_pheromone(self, path, path_length):
        for i in range(len(path) - 1):
            self.pheromone[(path[i], path[i + 1])] = (1 - self.evaporation_rate) * self.pheromone[
                (path[i], path[i + 1])] + self.q / path_length
        self.pheromone[(path[-1], path[0])] = (1 - self.evaporation_rate) * self.pheromone[
            (path[-1], path[0])] + self.q / path_length

    def _evaporate_pheromone(self):
        self.pheromone = {(u, v): (1 - self.evaporation_rate) * self.pheromone[(u, v)] for u, v in self.pheromone}
