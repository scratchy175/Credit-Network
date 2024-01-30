from src.processing import process_node_edges
from src.graph_utils import save_graph
from src.file_utils import save_parameters
from src.input_utils import *
import copy


if __name__ == "__main__":
    G, filename = choose_graph()
    strategy_func = choose_strategy()
    weights_func = choose_weights_strategy()
    num_simulations, weight_multiplier = input_simulation_parameters()

    simulation_dir = f"simulations/{filename}"
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)

    save_parameters(f"{simulation_dir}/parameters.json", strategy_func, weights_func, num_simulations, weight_multiplier)


    # a la fin de chaque simulation il faut reprer le graphe dans un fichier et rajouter les points ou jsp
    for i in range(num_simulations):
        SG = copy.deepcopy(G)
        weights_func(SG, weight_multiplier * i)

        edges_removed = True
        while edges_removed:
            edges_removed = False
            accumulated_weights = {}

            for node in SG.nodes():
                if process_node_edges(SG, node, accumulated_weights, strategy_func):
                    edges_removed = True

            for node, weight in accumulated_weights.items():
                SG.nodes[node]['weight'] += weight
        print(f"Simulation {i+1} done.")
        save_graph(SG,f"simulations/{filename}/simulation_{i+1}.gpickle")
    print("All simulations done.")

