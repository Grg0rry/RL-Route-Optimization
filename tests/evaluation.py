import traci


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