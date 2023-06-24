import os, sys

sys.path.append('models/')
import environment
import agent
import dijkstra


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
    # network_file = './network_files/fixed_network.net.xml'
    # congested = [("gneF_I", 10), ("gneI_F", 10), ("gneB_E", 20), ("gneE_B", 20), ("gneJ_M", 30), ("gneM_J", 30)]
    # traffic_light = [("B", 5), ("I", 5), ("G", 5)]
    # start_node = "A"
    # end_node = "N"

    # -------------------
    # OSM Network
    # [101: Sunway University, 102: Monash University, 103: Sunway Geo, 104: Sunway Medical, 105: Taylors University, 106: Sunway Pyramid, 107: Sunway Lagoon, 108: PJS10 Park]
    # -------------------
    network_file = './network_files/sunway.net.xml'
    congested = [("gne2124969573_1000000001", 10), ("gne677583745_2302498575", 10), ("gne5236931684_143675326", 20), ("gne1000000001_5735834058", 20), ("gne10734244602_1640449323", 10)]
    traffic_light = [("463099148", 5), ("678457498", 5), ("678457535", 5), ("678457587", 5), ("712814465", 5), ("1197913486", 5), ("1197913517", 5), ("2210132568", 5), ("2210132847", 5), ("2747527085", 5), ("4123498068", 5), ("5727497436", 5), ("5762726921", 5), ("8948947765", 5), ("9209244285", 5), ("10845806303", 5), ("10845816012", 5)]
    start_node = "101"
    end_node = "105"

    # 03 Initiate Environment
    env = environment.traffic_env(network_file, congested, traffic_light, evaluation = "d")
    num_episodes = 5000
    num_converge = 5

    # 04 Activate Agent
    # -------------------
    # Dijkstra Algorithm
    # -------------------
    print(f'Dijkstra Algorithm{"." * 100}')
    Dijkstra = dijkstra.Dijkstra(env, start_node, end_node)
    node_path, edge_path, *_ = Dijkstra.search()
    env.visualize_plot(edge_path)

    # -------------------
    # Q_Learning Algorithm
    # -------------------
    print(f'\nQ_Learning Algorithm{"." * 100}')
    Q_agent = agent.Q_Learning(env, start_node, end_node)
    node_path, edge_path, *_ = Q_agent.train(num_episodes, num_converge)
    env.visualize_plot(edge_path)

    # -------------------
    # SARSA Algorithm
    # -------------------
    print(f'\nSARSA Algorithm{"." * 100}')
    S_agent = agent.SARSA(env, start_node, end_node, exploration_rate = 0.2)
    node_path, edge_path, *_ = S_agent.train(num_episodes, num_converge)
    env.visualize_plot(edge_path)


    # Evaluate Model Performance
    # 01. Compare the time taken for processing between all Algorithms
    # 02. Compare the number of episodes taken to converge between Reinforcement Learning Algorithm
    # 03. Compare the distance of the optimal paths of all Algorithms --> Cost function
    # 04. Visualize the pathway choosen