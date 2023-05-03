import os, sys
import xml.etree.ElementTree as ET
import sumolib


class traffic_env:
    def __init__ (self, network_folder, network_output_file, blocked_routes, route_map, route_start = "0", route_end = "3600", route_file = 'route.xml', route_output_file = 'routes.rou.xml', sumo_cfg_file = 'sumo_network.sumocfg'):
        # Setup Route File
        self.route_file_config(network_folder, route_start, route_end, blocked_routes, network_output_file, route_file, route_output_file, sumo_cfg_file)

        # Define route nature
        self.blocked_routes = blocked_routes
        self.route_map = route_map        

        # Parameters 
        self.net = sumolib.net.readNet(network_output_file)
        self.nodes = [node.getID().upper() for node in self.net.getNodes()]
        self.action_space = [0, 1, 2, 3]  # 0 = 'Up', 1 = 'Down', 2 = 'Left', 3 = 'Right'
        self.state_space = [edge.getID() for edge in self.net.getEdges()]

    

    # Match node to edge
    def node_edge(self, node, node_type = 'all'):
        if node_type not in ('start', 'end', 'all'):
            raise ValueError('Invalid node_type')

        edges_lst = []
        net_node = self.net.getNode(node)

        # Only return the edges where the node is the start  
        if node_type == 'start':
            edges = net_node.getOutgoing()
            for edge in edges:
                if edge.getFromNode().getID() == node:
                    edges_lst.append(edge.getID())
        
        # Only return the edges where the node is the end
        elif node_type == 'end':
            edges = net_node.getIncoming()
            for edge in edges:
                if edge.getToNode().getID() == node:
                    edges_lst.append(edge.getID())

        # return all edges associated with the node
        else: # all
            edges = net_node.getOutgoing()
            edges.extend(net_node.getIncoming())
            for edge in edges:
                if edge.getToNode().getID() == node or edge.getFromNode().getID() == node:
                    edges_lst.append(edge.getID())
        
        if edges_lst == []:
            print('No edges found!')

        return edges_lst


    # distance between two edges/nodes
    def get_distance(self, start, end, start_type = 'node', end_type = 'node'):

        if start_type == 'edge':
            start = self.net.getEdge(start).getToNode().getID()
        elif end_type == 'edge':
            end = self.net.getEdge(end).getToNode().getID()
        
        start_x, start_y = self.net.getNode(start).getCoord()
        end_x, end_y = self.net.getNode(end).getCoord()

        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        return distance


    # find the given state direction
    def decode_state(self):
        state_direction = {}

        def get_direction(state):
            start_node = self.net.getEdge(state).getFromNode().getID()
            end_node = self.net.getEdge(state).getToNode().getID()

            start_x, start_y = self.net.getNode(start_node).getCoord()
            end_x, end_y = self.net.getNode(end_node).getCoord()
            direction = math.atan2(end_y - start_y, end_x - start_x)

            direction = math.degrees(direction)
            if direction < 0:
                direction += 360

            # 0 = 'Up', 1 = 'Down', 2 = 'Left', 3 = 'Right'
            if direction < 90:
                return 3
            elif direction < 180:
                return 0
            elif direction < 270:
                return 2
            else:
                return 1
        
        for state in self.state_space:
            state_direction[state] = get_direction(state)
        return state_direction


    # Find available actions from state
    def avail_actions(self, current_state):
        state_direction = self.decode_state()
        serounding_states = [edge.getID() for edge in self.net.getEdge(current_state).getOutgoing().keys()]
        return [state_direction[state] for state in serounding_states]


    # Translate given state and action to new state
    def translate_state(self, current_state, action):
        state_direction = self.decode_state()
        serounding_states = [edge.getID() for edge in self.net.getEdge(current_state).getOutgoing().keys()]
        for state, direction in state_direction.items():
            if state in serounding_states:
                if direction == action:
                    return state
        return None            








    # Setup SUMO Route files
    def route_file_config(self, network_folder, time_start, time_end, blocked_routes, network_output_file, route_file, route_output_file, sumo_cfg_file):
        # Change directory to store files
        os.chdir(network_folder)

        def route_setup():
            # Create XML document for routes
            def block_route(edge):
                # Function to Block Edges
                route_block = ET.SubElement(root, "route", {"id": f"route_block_{edge}", "edges": edge})
                vehicle_block = ET.SubElement(root, "vehicle", {"id": f"block_{edge}", "type": "car", "route": f"route_block_{edge}", "depart": time_start})
                stop = ET.SubElement(vehicle_block, "stop", {"edge": edge, "duration": time_end})
            try:
                print(f"**Setting Up Route file --> {route_file} ...**")
                root = ET.Element("routes")
                vtype_car = ET.SubElement(root, "vType", {"id": "car"})
                for route in blocked_routes:
                    block_route(route)
                tree = ET.ElementTree(root)
                tree.write(route_file)
                print("**Setup Completed!**")
                print("**Successfully Setup Route file**\n")
            except Exception as e:
                print(f"**Error in setting up Route file: {e}**")
                sys.exit(1)


        def route_SUMO_setup():
            # Convert route XML to SUMO format
            try:
                print(f"**Converting Route file to SUMO format --> {route_output_file} ...**")
                os.system(f'duarouter --net-file={network_output_file} --route-file={route_file} --output-file={route_output_file}')
                print("**Convert Completed!**")
                print("**Successfully Convert Route file to SUMO format**\n")
            except Exception as e:
                print(f"**Error in converting Route file to SUMO format: {e}**")
                sys.exit(1)


        def SUMO_setup():
            # Create SUMO document for combining route and network
            try:
                print(f"**Setting Up SUMO file --> {sumo_cfg_file} ...**")
                root = ET.Element("configuration")
                net = ET.SubElement(root, "input")
                ET.SubElement(net, "net-file", value=network_output_file)
                ET.SubElement(net, "route-files", value=route_output_file)
                time = ET.SubElement(root, "time")
                ET.SubElement(time, "begin", value=time_start)
                ET.SubElement(time, "end", value=time_end)
                ET.SubElement(time, "step-length", value="0.1")
                tree = ET.ElementTree(root)
                tree.write(sumo_cfg_file)
                print("**Setup Completed!**")
                print("**Successfully Setup SUMO file**\n")
            except Exception as e:
                print(f"**Error in setting up SUMO file: {e}**")
                sys.exit(1)

        
        def SUMO_SUMO_setup():
            # Convert SUMO cfg to SUMO format
            try:
                print(f"**Converting SUMO file to SUMO format --> {sumo_cfg_file} ...**")
                os.system(f'sumo -c {sumo_cfg_file}')
                print("**Convert Completed!**")
                print("**Successfully Convert SUMO file to SUMO format**\n")
            except Exception as e:
                print(f"**Error in converting SUMO file to SUMO format: {e}**")
                sys.exit(1)


        # Call the setup functions
        route_setup()
        route_SUMO_setup()
        SUMO_setup()
        SUMO_SUMO_setup()

        # Change back to parent dir (cd ..)
        os.chdir(os.pardir)