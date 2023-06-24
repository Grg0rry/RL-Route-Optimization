import os, sys, shutil
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt


def visualize_plot(network_file, travel_edges, network_files_directory = "network_files", root_file="network"):
    """
    Plotting of network with selected route

    Args:
    - network_file (str): The directory of the SUMO network file.
    - travel_edges (list): The list of edges of the selected route.
    - network_files_directory (str): The directory of the network files.
    - root_file (str): The initial name of the root file to be converted from network_file.

    Return:
    - Plot of network
    """

    # change directory to store files output
    if not os.path.exists(network_files_directory):
        os.mkdir(network_files_directory)
    os.chdir(network_files_directory)

    # check if network_file exist in network_files_directory
    network_file_name = os.path.basename(network_file)
    if not os.path.exists(network_file_name):
        shutil.move(network_file, network_files_directory)
    network_file = network_file_name

    # convert network_file to root form
    print("Converting to Root file...")
    os.system(f"netconvert --sumo-net-file={network_file} --plain-output-prefix={root_file} --no-warnings=true")

    # convert nodes xml to dataframe
    def parse_nodes():
        node_file = f"{root_file}.nod.xml"
        if not os.path.exists(node_file):
            sys.exit("missing node file")
        
        tree = ET.parse(node_file)
        root = tree.getroot()
        nodes = {}

        # Iterate over the node elements
        for node in root.findall('node'):
            node_id = node.attrib['id']
            x_coord = float(node.attrib['x'])
            y_coord = float(node.attrib['y'])
            
            # Append the data
            nodes[node_id] = (x_coord, y_coord)

        return nodes
    
    # convert edges xml to dataframe
    def parse_edges():
        edge_file = f"{root_file}.edg.xml"
        if not os.path.exists(edge_file):
            sys.exit("missing edge file")
        
        tree = ET.parse(edge_file)
        root = tree.getroot()
        edges = {}

        # Iterate over the node elements
        for edge in root.findall('edge'):
            edge_id = edge.attrib['id']
            from_id = edge.attrib['from']
            to_id = edge.attrib['to']
            
            # Append the data
            edges[edge_id] = (from_id, to_id)

        return edges

    # plot networknx graph
    def plot_graph(nodes, edges):
        
        # Draws the network layout
        G = nx.Graph()
        for edge in edges:
            G.add_edge(edges[edge][0], edges[edge][1])

        # Draws the selected route
        route_G = nx.Graph()
        for edge in travel_edges:
            route_G.add_edge(edges[edge][0], edges[edge][1])
        
        # Plot graph
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color='red', node_size=300)

        pos = {node: nodes[node] for node in nodes}
        nx.draw(G, pos, with_labels=False, node_color='black', node_size=200, edge_color='gray')
        nx.draw(route_G, pos, with_labels=False, node_color='green', node_size=300, edge_color='green', width = 2)
        plt.show()

    plot_graph(parse_nodes(), parse_edges())

    # Change back to parent dir (cd ..)
    os.chdir(os.pardir)


def SUMO_GUI(network_file, travel_edges, blocked_routes, network_files_directory = "network_files", time_start = "0", time_end = "9000", route_file = 'nodes.nod.xml', route_output_file = 'routes.rou.xml', sumo_cfg_file = 'sumo_network.sumocfg'):
    """
    Configures the Route and SUMO cfg files.

    Args:
    - network_file (str): The directory of the SUMO network file.
    - travel_edges (list): The list of the edges of the selected route.
    - blocked_routes (list): The list of the routes that are blocked.
    - network_files_directory (str): The directory of the network files.
    - time_start (str): The start time of the simulation.
    - time_end (str): The end time of the simulation.
    - route_file (str): The name of the route file.
    - route_output_file (str): The name of the SUMO route file.
    - sumo_cfg_file (str): The name of the SUMO configuration file.

    Returns:
    - None
    """

    # change directory to store files output
    if not os.path.exists(network_files_directory):
        os.mkdir(network_files_directory)
    os.chdir(network_files_directory)

    # check if network_file exist in network_files_directory
    network_file_name = os.path.basename(network_file)
    if not os.path.exists(network_file_name):
        shutil.move(network_file, network_files_directory)
    network_file = network_file_name

    # configuration of route.XML
    print("Setting Up the Route file...")

    def route_file_config():
        # block selected edges
        def block_route(edge):
            vehicle_block = ET.SubElement(root, "vehicle", {"id": f"block_{edge}", "color": "0,1,0", "type": "truck", "depart": time_start})
            route_block = ET.SubElement(vehicle_block, "route", {"edges": edge})
            stop = ET.SubElement(vehicle_block, "stop", {"edge": edge, "duration": time_end})
        
        # selected travel pathway
        def travel_route(edges, index, depart_time):
            vehicle = ET.SubElement(root, "vehicle", {"id": f"route_vehicle_{index}", "type": "car", "depart": depart_time})
            route_travel = ET.SubElement(vehicle, "route", {"edges": ' '.join(edges)})

        # create route XML
        root = ET.Element("routes")

        block_vtype = ET.SubElement(root, "vType", {"id": "truck"})
        for route in blocked_routes:
            block_route(route)
        
        travel_vtype = ET.SubElement(root, "vType", {"id": "car"})
        for i, depart in enumerate(range(int(time_start), int(time_end), 30)):
            travel_route(travel_edges, i, str(depart))

        tree = ET.ElementTree(root)
        tree.write(route_file)

        # calls duarouter SUMO method
        os.system(f"duarouter --net-file={network_file} --route-files={route_file} --output-file={route_output_file}")    
    
    # route setup
    route_file_config()

    # configuration of SUMO.cfg
    print("Setting Up the SUMO cfg file...")

    def SUMO_file_config():
        # config SUMO file
        root = ET.Element("configuration")
        net = ET.SubElement(root, "input")
        ET.SubElement(net, "net-file", value=network_file)
        ET.SubElement(net, "route-files", value=route_output_file)
        time = ET.SubElement(root, "time")
        ET.SubElement(time, "begin", value=time_start)
        ET.SubElement(time, "end", value=time_end)
        ET.SubElement(time, "step-length", value="1", unit="m")
        tree = ET.ElementTree(root)
        tree.write(sumo_cfg_file)

        # calls sumo method
        os.system(f'sumo -c {sumo_cfg_file}')

    # SUMO setup
    SUMO_file_config()

    print("Setup Completed!!")
    # Change back to parent dir (cd ..)
    os.chdir(os.pardir)
