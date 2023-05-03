import os, sys
import traci
import xml.etree.ElementTree as ET
import sumolib
import numpy as np
import math

sys.path.append('models/')
import traffic_network
import environment

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
    

    print(os.getcwd())
    


