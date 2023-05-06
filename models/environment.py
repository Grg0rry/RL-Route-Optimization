import os, sys
import xml.etree.ElementTree as ET
import sumolib
import math


class traffic_env:
    def __init__ (self, network_folder, network_output_file, blocked_routes, route_map, time_start = "0", time_end = "3600", route_file = 'route.xml', route_output_file = 'routes.rou.xml', sumo_cfg_file = 'sumo_network.sumocfg'):
        # Setup Route File
        self.route_file_config(network_folder, time_start, time_end, blocked_routes, network_output_file, route_file, route_output_file, sumo_cfg_file)

        # Define route nature
        self.blocked_routes = blocked_routes
        self.route_map = route_map

        # Parameters 
        self.net = sumolib.net.readNet(os.path.join(network_folder,network_output_file))
        self.nodes = [node.getID().upper() for node in self.net.getNodes()]
        self.edges = [edge.getID() for edge in self.net.getEdges()]

        # Left to Right
        # self.action_space = {0: 'Up', 1: 'Right', 2: 'Down', 3: 'Left'}
        
        # Right to Left 
        # self.action_space = {0: 'Left', 1: 'Up', 2: 'Right', 3: 'Down'}

        self.state_space = edges
        self.state_direction = self.decode_state_to_direction()


    def set_action_space(self, direction):
        general_directions = ['Up', 'Left', 'Down', 'Right']

        starting_index = general_directions.index(direction)
        reorder_list = general_directions[starting_index:] + general_directions[:starting_index]
        
        action_space = {}
        for i in range(len(general_directions)):
            action_space[i] = reorder_list[i]
        
        print(action_space)
        return action_space


    # Set starting and ending nodes
    def set_start_end(self):
        """
        Receive user input to set the Starting and Ending Nodes for the route

        Returns:
        - None
        """
        
        nodes_lst = self.nodes

        # Receive Input from User to select starting and ending Nodes
        def node_response(nodes_lst, prompt):
            print(self.route_map)
            response = input(prompt).upper()
            if response not in nodes_lst:
                print("Invalid node!!!")
                return node_response(nodes_lst, prompt)
            return response

        start_node = node_response(nodes_lst, "Please Enter a Starting Point ==> ")
        end_node = node_response(nodes_lst, "Please Enter a Ending Point ==> ")
        # start_node = "M"
        # end_node = "B"
        start_edges = self.decode_node_to_edge(start_node, 'outgoing')
        end_edges = self.decode_node_to_edge(end_node, 'incoming')
        action_space = self.set_action_space(self.get_distance(start_node, end_node)[1])
        return start_node, end_node, start_edges, end_edges, action_space


    # Distance between two edges/nodes
    def get_distance(self, start, end, start_type = 'node', end_type = 'node'):
        """
        Given a start and end point (node or edge), returns the distance between them

        Args:
        - start (str): The ID of the starting point
        - end (str): The ID of the ending point
        - start_type (str): The type of the starting point (node or edge)
        - end_type (str): The type of the ending point (node or edge)

        Returns:
        - Distance between the two points
        """

        # Check if the nodes or edges are valid
        if start not in self.nodes and start not in self.state_space:
            sys.exit('Error: Invalid Start Point!')
        elif end not in self.nodes and end not in self.state_space:
            sys.exit('Error: Invalid End Point!')
        
        # Convert all Edges to Nodes for comparison
        if start_type == 'edge':
            start = self.net.getEdge(start).getToNode().getID()
        elif end_type == 'edge':
            end = self.net.getEdge(end).getToNode().getID()
        
        # Get the coordinates
        start_x, start_y = self.net.getNode(start).getCoord()
        end_x, end_y = self.net.getNode(end).getCoord()

        # Calculates the distance
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx**2 + dy**2)

        # Get the direction either Up, Down, Left or Right
        if abs(dx) > abs(dy):
            if dx > 0:
                direction = 'Right'
            else:
                direction = 'Left'
        else:
            if dy > 0:
                direction = 'Up'
            else:
                direction = 'Down'
        return distance, direction


    # Match node to edge
    def decode_node_to_edge(self, node, direction = None):
        """
        Given a node and direction, returns a list of edges associated with that node.

        Args:
        - node (str): The ID of the node to match to edges
        - direction (str or None): The direction of the edges to return.
            If None, all edges are returned. Otherwise, must be one of the following strings:
            - 'incoming': return only edges where the node is the end
            - 'outgoing': return only edges where the node is the start

        Returns:
        - A list of edges (str) associated with the given node, in the specified direction if specified.
        """

        # Check if the direction is valid
        if direction not in ('incoming', 'outgoing', None):
            sys.exit(f'Invalid direction: {direction}')
    
        edges = []
        net_node = self.net.getNode(node)

        # Match node and direction to return edges
        if direction == 'incoming':
            for edge in net_node.getIncoming():
                if edge.getToNode().getID() == node:
                    edges.append(edge.getID())

        elif direction == 'outgoing':
            for edge in net_node.getOutgoing():
                if edge.getFromNode().getID() == node:
                    edges.append(edge.getID())

        else:
            for edge in net_node.getIncoming() + net_node.getOutgoing():
                if edge.getToNode().getID() == node or edge.getFromNode().getID() == node:
                    edges.append(edge.getID())

        if not edges:
            print(f'No edges found for node {node}')
        return edges


    # Find the direction from a given state
    def decode_state_to_direction(self):
        """
        Iterates through the whole state space and returns a dictionary of each state and the direction it is headed.

        Returns:
        - A dictionary of states (str) matched with its direction.
        """

        state_direction = {}
        def get_state_direction(state):
            # Find the direction and angle between two nodes to determine the edge direction
            start_node = self.net.getEdge(state).getFromNode().getID()
            end_node = self.net.getEdge(state).getToNode().getID()

            start_x, start_y = self.net.getNode(start_node).getCoord()
            end_x, end_y = self.net.getNode(end_node).getCoord()
            
            # Calculate the direction of the nodes in radians
            direction = math.degrees(math.atan2(end_y - start_y, end_x - start_x))

            # Get the degree boundary it falls in
            if direction < 0:
                direction += 360
            
            if direction < 90:
                return 'Right'
            elif direction < 180:
                return 'Up'
            elif direction < 270:
                return 'Left'
            else:
                return 'Down'
        
        # Iterate through every state in the state space and compute its direction
        for state in self.state_space:
            state_direction[state] = get_state_direction(state)
        return state_direction


    # Find available actions from a given state
    def decode_state_to_actions(self, action_space, state):
        """
        Calls `decode_state_direction` to determine the direction of the given state. 
        Returns a list of available actions from that given state.

        Args:
        - state (str): The ID of the state (edge)

        Returns:
        - A list of actions (int)
        """

        # Check if state is in the State Space
        if state not in self.state_space:
            sys.exit('Error: State not in State Space!')

        # Determine the possible actions of the state
        state_direction = self.state_direction # self.decode_state_to_direction()
        serounding_states = [edge.getID() for edge in self.net.getEdge(state).getOutgoing().keys()]

        # Returns a list of actions
        actions_lst = []
        for action, direction in action_space.items():
            if direction in [state_direction[state_i] for state_i in serounding_states]:
                actions_lst.append(action)
        return actions_lst


    # Find the new state from a given state and action
    def decode_state_action_to_state(self, action_space, current_state, action):
        """
        Calls `decode_state_direction` to determine the new state given the current_state and action taken.
        
        Args:
        - current_state (str): The ID of the current state (edge).
        - action (int): The action taken from the current state.

        Returns:
        - The new state (str) or None if no match is found.
        """

        # Check if state is in the State Space and action is in the Action Space
        if current_state not in self.state_space:
            sys.exit('Error: State not in State Space!')
        elif action not in [action for action in action_space]:
            sys.exit('Error: Action not in Action Space!')

        # Determine the possible directions of the current_state
        state_direction = self.state_direction # self.decode_state_to_direction()
        serounding_states = [edge.getID() for edge in self.net.getEdge(current_state).getOutgoing().keys()]
        
        # Match the direction with the action to determine the new state
        for state, direction in state_direction.items():
            if state in serounding_states:
                if direction == action_space[action]:
                    # print(f'current_state: {current_state}, state_space: {serounding_states}, action": {action_space[action]}, state: {state}\n')
                    return state
        return None


    # Configure Route File
    def route_file_config(self, network_folder, time_start, time_end, blocked_routes, network_output_file, route_file, route_output_file, sumo_cfg_file):
        """
        Configures the SUMO route files.

        Args:
        - network_folder (str): The directory where the network files are stored.
        - time_start (str): The start time of the simulation.
        - time_end (str): The end time of the simulation.
        - blocked_routes (list): A list of the routes that are blocked.
        - network_output_file (str): The name of the SUMO network file.
        - route_file (str): The name of the route file.
        - route_output_file (str): The name of the SUMO route file.
        - sumo_cfg_file (str): The name of the SUMO configuration file.

        Returns:
        - None
        """

        # Change directory to store files
        os.chdir(network_folder)

        # Create XML document for routes
        def route_setup():
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

        # Convert route XML to SUMO format
        def route_SUMO_setup():
            try:
                print(f"**Converting Route file to SUMO format --> {route_output_file} ...**")
                os.system(f"duarouter --net-file={network_output_file} --route-files={route_file} --output-file={route_output_file}")
                print("**Convert Completed!**")
                print("**Successfully Convert Route file to SUMO format**\n")
            except Exception as e:
                print(f"**Error in converting Route file to SUMO format: {e}**")
                sys.exit(1)

        # Create SUMO document for combining route and network
        def SUMO_setup():
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

        # Convert SUMO cfg to SUMO format
        def SUMO_SUMO_setup():
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