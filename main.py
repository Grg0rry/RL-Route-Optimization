import os, sys
import datetime

sys.path.append('models/')
import environment
import agent
import evaluation


def sumo_configuration():
    os.environ["SUMO_HOME"] = "D:/app/SUMO/SUMO/" # -- change to own directory

    # Check if SUMO sucessfully configured
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")


if __name__ == '__main__':
    # 01 Setup SUMO
    sumo_configuration()

    # 02 Configure network variables
    # -------------------
    # Fixed Network
    # [A, B, C, D, E, F, G, H, I, J, K, L, M, N]
    # -------------------
    network_file = './network_files/fixed_network.net.xml'
    blocked_routes = ["gneF_I", "gneI_F", "gneB_E", "gneE_B", "gneJ_M", "gneM_J"]
    start_node = "A"
    end_node = "N"

    # -------------------
    # OSM Network
    # [101: Sunway University, 102: Monash University, 103: Sunway Geo, 104: Sunway Medical, 105: Taylors University, 106: Sunway Pyramid, 107: Sunway Lagoon, 108: PJS10 Park]
    # -------------------
    # network_file = './network_files/sunway.net.xml'
    # blocked_routes = []
    # start_node = "101"
    # end_node = "105"

    # 03 Initiate Environment
    env = environment.traffic_env(network_file, blocked_routes)

    # 04 Activate Agent
    # -------------------
    # Dijkstra Algorithm
    # -------------------
    print(f'Dijkstra Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    D_agent = agent.Dijkstra(env, start_node, end_node)
    node_path, edge_path, *_ = D_agent.search()
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processsing Time: {seconds} seconds')
    distance = evaluation.evaluate_distance(env, node_path)
    print(f'Distance travelled: {round(distance, 2)} m')
    evaluation.visualize_plot(network_file, edge_path)

    # -------------------
    # Q_Learning Algorithm
    # -------------------
    print(f'\nQ_Learning Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    Q_agent = agent.Q_Learning(env, start_node, end_node)
    node_path, edge_path, *_ = Q_agent.train(1000, 5)
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processing Time: {seconds} seconds')
    distance = evaluation.evaluate_distance(env, node_path)
    print(f'Distance travelled: {round(distance, 2)} m')
    evaluation.visualize_plot(network_file, edge_path)

    # -------------------
    # SARSA Algorithm
    # -------------------
    print(f'\nSARSA Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    S_agent = agent.SARSA(env, start_node, end_node)
    node_path, edge_path, *_ = S_agent.train(1000, 5)
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processing Time: {seconds} seconds')
    distance = evaluation.evaluate_distance(env, node_path)
    print(f'Distance travelled: {round(distance, 2)} m')
    evaluation.visualize_plot(network_file, edge_path)    


    # Evaluate Model Performance
    # 01. Compare the time taken for processing between all Algorithms
    # 02. Compare the number of episodes taken to converge between Reinforcement Learning Algorithm
    # 03. Compare the distance of the optimal paths of all Algorithms --> Cost function
    # 04. Visualize the pathway choosen