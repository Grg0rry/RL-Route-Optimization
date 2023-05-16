import os, sys
import traci
import sumolib
import datetime

sys.path.append('models/')
import traffic_network
import environment
import agent


def sumo_configuration():
    os.environ["SUMO_HOME"] = "D:/app/SUMO/SUMO/" # -- change to own directory

    # Check if SUMO sucessfully configured
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    
    # Check versioning
    sumo_version = os.popen("sumo --version").read().strip()
    traci_version = os.popen("pip show traci --version").read().strip()
    # if sumo_version == traci_version:
        # "The versions match."


def evaluate_distance(env, nodes):
    total_distance = 0
    for index in range(len(nodes)-1):
        total_distance += env.get_distance(nodes[index], nodes[index+1])[0]
    return total_distance


if __name__ == '__main__':
    # Setting Up SUMO
    # sumo_configuration()

    # Setting up Traffic Environment
    network_file_directory = 'network_files/'
    
    # Fixed Network
    blocked_routes = ["gneE2", "-gneE2", "gneE6", "-gneE6", "gneE13", "-gneE13"]
    network = traffic_network.fixed_network(network_file_directory, blocked_routes)
    
    # OSM Network
    # osm_file = 'sunway.osm.xml'
    # network = traffic_network.osm_network(network_file_directory, osm_file)

    # Initiate Environment
    env = environment.traffic_env(network)

    # Activate Agent
    """ 
    Choose a start and End Node with the map below:
        B =/= E ==  H == K
        |     |     |    |
        |     |     |    |
    A == C == F =/= I == L == N
        |     |     |    |
        |     |     |    |
        D ==  G == J =/= M
    """
    start_node = "A"
    end_node = "N"


    # Dijkstra Algorithm
    print(f'Dijkstra Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    D_agent = agent.Dijkstra(env, start_node, end_node)
    node_path, edge_path, *_ = D_agent.search()
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processsing Time: {seconds} seconds')
    distance = evaluate_distance(env, node_path)
    print(f'Distance travelled: {distance}')
    

    # Q_Learning Algorithm
    print(f'\nQ_Learning Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    Q_agent = agent.Q_Learning(env, start_node, end_node)
    node_path, edge_path, *_ = Q_agent.train(1000, 5)
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processing Time: {seconds} seconds')
    distance = evaluate_distance(env, node_path)
    print(f'Distance travelled: {distance}')


    # SARSA Algorithm
    print(f'\nSARSA Algorithm{"." * 100}')
    start_time = datetime.datetime.now()
    S_agent = agent.SARSA(env, start_node, end_node)
    node_path, edge_path, *_ = S_agent.train(1000, 5)
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()
    print(f'Processing Time: {seconds} seconds')
    distance = evaluate_distance(env, node_path)
    print(f'Distance travelled: {distance}')


    # Evaluate Model Performance
    # 01. Compare the time taken for processing between all Algorithms
    # 02. Compare the number of episodes taken to converge between Reinforcement Learning Algorithm
    # 03. Compare the distance of the optimal paths of all Algorithms --> Cost function

