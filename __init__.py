import os, sys
import traci
import sumolib
import cProfile

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
    if sumo_version == traci_version:
        print("The versions match.")
    else:
        print("SUMO version doesnt match with Traci")


def sumo_simulation(network_file_directory, network_file, route):
    traci.start(["sumo", "--net-file", os.path.join(network_file_directory,network_file)], traceFile="traci.log")

    traci.route.add("Route", route)
    vehicle_id = traci.vehicle.add("veh", "Route", typeID="car")
    # traci.vehicle.setRoute(vehicle_id, "Route")

    traci.simulation.start()
    
    time_travelled = traci.vehicle.getTravelTime(vehicle_id)
    distance_travelled = traci.vehicle.getDistance(vehicle_id)

    print("Time travelled: {} s".format(time_travelled))
    print("Distance travelled: {} m".format(distance_travelled))

    traci.close()


if __name__ == '__main__':
    # Setting Up SUMO
    sumo_configuration()

    # Setting up Traffic Environment
    network_file_directory = 'network_files/'
    network_file = traffic_network.network_file_config(network_file_directory)
    route_map = """
     B =/= E == H == K
     |    |     |    |
     |    |     |    |
A == C == F =/= I == L == N
     |    |     |    |
     |    |     |    |
     D == G == J =/= M
    """
    blocked_routes = ["gneE2", "-gneE2", "gneE6", "-gneE6", "gneE13", "-gneE13"]
    env = environment.traffic_env(network_file_directory, network_file, blocked_routes, route_map)
    
    # cProfile.run('agent.Q_Learning(env).train(1000)')

    # Activate Agent
    # for start_state in env.state_space:
    #     for end_state in env.state_space:
    #         Q_agent = agent.Q_Learning(env, start_state, end_state)
    #         logs, episode = Q_agent.train(1000)
    Q_agent = agent.Q_Learning(env)
    logs, episode = Q_agent.train(1000)
    # sumo_simulation(network_file_directory, network_file, logs[episode])

    S_agent = agent.SARSA(env)
    logs, episode = S_agent.train(1000)



