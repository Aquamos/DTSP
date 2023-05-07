import json
from graph_plot import draw_graph
from get_data import self_generate_problem, read_problem_from_hardcode, read_problem_from_json
from ant_colony_optimizer import AntColonyOptimizer


def aco_run_json_data(aco_params=(10, 0.1, 1, 2, 1, 10), file_name="data.json", draw_graph_flag=False):
    """
    :param aco_params: num_of_ants, evaporation_rate, alpha, beta, q
    :param file_name: the name of the json file
    :param draw_graph_flag: if True, draw graph for each iteration
    :return: nodes, best_path, best_path_length
    """

    try:
        nodes, g, weights, start_final_node = read_problem_from_json(f"data/{file_name}")
        aco = AntColonyOptimizer(g, weights, start_final_node, num_ants=aco_params[0],
                                 evaporation_rate=aco_params[1], alpha=aco_params[2],
                                 beta=aco_params[3], q=aco_params[4])

        best_path, best_path_length = aco.run(aco_params[5])

        if draw_graph_flag:
            draw_graph(g, best_path)

        return nodes, best_path, best_path_length

    except FileNotFoundError:
        print("File not found!")
    except json.JSONDecodeError:
        print("Invalid JSON format!")
    except KeyError as e:
        print(f"Error: Key '{e}' not found in the JSON data")
    except Exception as e:
        print(f"An error occurred: {e}")


def aco_run_generated_data(aco_params=(10, 0.1, 1, 2, 1, 10),
                           generator_params=(3, 5, 20),
                           draw_graph_flag=False):
    """
    :param aco_params: num_of_ants, evaporation_rate, alpha, beta, q
    :param generator_params: n, max_distance, max_mass
    :param draw_graph_flag: if True, draw graph for each iteration
    :return: nodes, best_path, best_path_length
    """
    nodes, edges, thau, weights = self_generate_problem(generator_params[0], generator_params[1], generator_params[2])

    g, weights, start_final_node = read_problem_from_hardcode(nodes, edges, thau, weights)

    aco = AntColonyOptimizer(g, weights, start_final_node, num_ants=aco_params[0], evaporation_rate=aco_params[1],
                             alpha=aco_params[2], beta=aco_params[3], q=aco_params[4])

    best_path, best_path_length = aco.run(aco_params[5])

    if draw_graph_flag:
        draw_graph(g, best_path)

    return nodes, best_path, best_path_length


def aco_run_hardcoded_data(data, aco_params=(10, 0.1, 1, 2, 1, 10), draw_graph_flag=False):
    """
    :param data: nodes, edges, thau, weights
    :param aco_params: num_of_ants, evaporation_rate, alpha, beta, q
    :param draw_graph_flag: if True, draw graph for each iteration
    :return:
    """
    g, weights, start_final_node = read_problem_from_hardcode(data[0], data[1], data[2], data[3])
    aco = AntColonyOptimizer(g, weights, start_final_node, num_ants=aco_params[0], evaporation_rate=aco_params[1],
                             alpha=aco_params[2], beta=aco_params[3], q=aco_params[4])

    best_path, best_path_length = aco.run(aco_params[5])

    if draw_graph_flag:
        draw_graph(g, best_path)

    return best_path, best_path_length


def iterations_experiment(aco_params=(10, 10, 0.1, 1, 2, 1, 10),
                          generator_params=(3, 5, 20),
                          num_of_iterations_experiment_set=(10, 50, 100),
                          num_of_experiments=20,
                          draw_graph_flag=False):
    """
    :param aco_params: num_of_ants, evaporation_rate, alpha, beta, q
    :param generator_params: n, max_distance, max_mass
    :param num_of_iterations_experiment_set: list of num_of_iterations
    :param draw_graph_flag: if True, draw graph for each iteration
    :param num_of_experiments: number of the experiments
    :return: experiment: list of lists of the best path lengths for each num_of_iterations
    """
    experiment = []
    for i in range(num_of_experiments):

        nodes, edges, thau, weights = self_generate_problem(n=generator_params[0],
                                                            max_distance=generator_params[1],
                                                            max_mass=generator_params[2])

        g, weights, start_final_node = read_problem_from_hardcode(nodes, edges, thau, weights)

        problem = []
        for num_of_iterations in num_of_iterations_experiment_set:
            aco = AntColonyOptimizer(g, weights, start_final_node, num_ants=aco_params[0],
                                     evaporation_rate=aco_params[1],
                                     alpha=aco_params[2], beta=aco_params[3], q=aco_params[4])

            best_path, best_path_length = aco.run(num_of_iterations)
            problem.append(best_path_length)

            if draw_graph_flag:
                draw_graph(g, best_path)
        experiment.append(problem)

    return experiment
