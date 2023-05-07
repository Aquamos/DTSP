from service import iterations_experiment, aco_run_generated_data, aco_run_json_data, aco_run_hardcoded_data


if __name__ == '__main__':

    # * Algorithm parameters:
    num_of_iterations = 10
    num_of_ants = 10
    evaporation_rate = 0.1
    alpha = 1
    beta = 2
    q = 1

    # * Iterations experiment parameters:
    nodes_num = 5
    max_distance = 30
    max_mass = 20
    num_of_iterations_experiment_set = [10, 50, 90, 130, 170, 210, 250, 290, 330, 370]

    # * When data is generated:
    # nodes, best_path, best_path_length = aco_run_generated_data()
    # print(f'Shortest path: {best_path}')
    # print(f'Shortest path length: {best_path_length}')

    # * When data is read from JSON:
    # nodes, best_path, best_path_length = aco_run_json_data()
    # print(f'Shortest path: {best_path}')
    # print(f'Shortest path length: {best_path_length}')

    # * When data is hardcoded:
    # nodes = ["ATB", "Novus", "Silpo", "Fora", "Velyka Kyshenya"]
    # edges = [
    #     [0, 15, 20, 10, 25],
    #     [15, 0, 10, 18, 30],
    #     [20, 10, 0, 8, 23],
    #     [10, 18, 8, 0, 15],
    #     [25, 30, 23, 15, 0]
    # ]
    # weights = [7, 10, 5, 8, 3]
    # thau = [10, 17, 8, 12, 15]
    # best_path, best_path_length = aco_run_hardcoded_data((nodes, edges, thau, weights))
    # print(f'Shortest path: {best_path}')
    # print(f'Shortest path length: {best_path_length}')

    # * Iterations experiment usage example:
    # iteration_experiment = iterations_experiment((num_of_ants, evaporation_rate, alpha, beta, q, num_of_iterations),
    #                                              (nodes_num, max_distance, max_mass),
    #                                              num_of_iterations_experiment_set)
    # exp_iter_nums = []
    # for el in iteration_experiment:
    #     exp_iter_nums.append(num_of_iterations_experiment_set[el.index(min(el))])
    # print(f'Experiment results: ')
    # print(f"Best number of iterations for n = {nodes_num} is {max(exp_iter_nums)}")
