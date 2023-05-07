import os, sys
import traci
import sumolib
import datetime

sys.path.append('models/')
import traffic_network
import environment
import agent

sys.path.append('tests/')
import evaluation


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


if __name__ == '__main__':
    # Setting Up SUMO
    # sumo_configuration()

    # Setting up Traffic Network Environment
    network_file_directory = 'network_files/'
    network_file = traffic_network.network_file_config(network_file_directory)

    # Setting up Traffic Route Environment
    blocked_routes = ["gneE2", "-gneE2", "gneE6", "-gneE6", "gneE13", "-gneE13"]
    traffic_network.route_file_config(network_file_directory, network_file, blocked_routes)

    # Initiate Environment
    env = environment.traffic_env(network_file_directory, network_file, blocked_routes)

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
    start_node = "N"
    end_node = "A"
    
    start = datetime.datetime.now()
    D_agent = agent.Dijkstra(env, start_node, end_node)
    node_path, edge_path, *_ = D_agent.search()
    end = datetime.datetime.now()
    print(f'time taken: {end - start}')

    start = datetime.datetime.now()
    Q_agent = agent.Q_Learning(env, start_node, end_node)
    node_path, edge_path, *_ = Q_agent.train(1000, 5)
    end = datetime.datetime.now()
    print(f'time taken: {end - start}')

    start = datetime.datetime.now()
    S_agent = agent.SARSA(env, start_node, end_node)
    node_path, edge_path, *_ = S_agent.train(1000, 5)
    end = datetime.datetime.now()
    print(f'time taken: {end - start}')

    # Evaluate Model Performance
    # evaluation.funct()

