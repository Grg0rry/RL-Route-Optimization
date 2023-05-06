import traci


def test(self):
    net = traci.sumolib.net.Net()
    veh = traci.vehicle.Vehicle("veh0", net)
    route = 

    traci.start(["sumo", "--net-file", "network_files\\network.net.xml"], traceFile="traci.log")
    for step in range(100):
        current_time = traci.simulation.getCurrentTime()
        current_position = traci.vehicle.getPosition(veh)


    # traci.start(["/usr/bin/sumo-gui", "-c", "sumo_network.sumocfg", "--start", "--quit-on-end", "--remote-port"], numTries=100)