import os, sys
import xml.etree.ElementTree as ET
import sumolib
import math


class traffic_env:
    def __init__ (self, network_folder, network_output_file, blocked_routes):
        # Define route nature
        self.blocked_routes = blocked_routes

        # Parameters 
        self.net = sumolib.net.readNet(os.path.join(network_folder,network_output_file))
        self.nodes = [node.getID().upper() for node in self.net.getNodes()]
        self.edges = [edge.getID() for edge in self.net.getEdges()]
        # self.action_space = initiated in agent.py
        self.state_space = self.nodes
        self.edge_direction = self.decode_edges_to_direction()


    def set_action_space(self, directions):
        """
        Adjust the action_space according to the direction of the start and end node

        Args:
        - directions (list): The direction of the start node to the end node. Either only
        one direction or two like Down, Right or only Down
        
        Returns:
        - A directionary of the action_space
        """
        
        # Define the clockwise rotation of directions
        direction_dict = {'Up': 'Down', 'Right': 'Left', 'Down': 'Up', 'Left': 'Right'}
        general_directions = list(direction_dict.keys())

        # Sort the general direction list with the directions given
        if len(directions) == 1:
            starting_index = general_directions.index(directions[0])
            reorder_list = general_directions[starting_index:] + general_directions[:starting_index]
        elif len(directions) == 2:
            opposite = [direction_dict[directions[0]], direction_dict[directions[1]]]
            reorder_list = directions + opposite
        else:
            reorder_list = general_directions

        # Returns action space
        action_space = {i: reorder_list[i] for i in range(len(reorder_list))}
        return action_space


    # Set starting and ending nodes
    def set_start_end(self, start_node, end_node):
        """
        Validates the input starting and ending node and calls the 'set_action_space'
        then returns the action space with it

        Returns:
        - A dictionary of the action_space
        """
        
        # Check if the nodes are valid
        if start_node not in self.nodes:
            sys.exit('Error: Invalid Start Node!')
        elif end_node not in self.nodes:
            sys.exit('Error: Invalid End Node!')

        action_space = self.set_action_space(self.get_distance(start_node, end_node)[1])
        return action_space


    # Distance between two edges/nodes
    def get_distance(self, start, end, start_type = 'node', end_type = 'node'):
        """
        Given a start and end point (node or edge), returns the distance and direction between them.

        Args:
        - start (str): The ID of the starting point
        - end (str): The ID of the ending point
        - start_type (str): The type of the starting point (node or edge)
        - end_type (str): The type of the ending point (node or edge)

        Returns:
        - A tuple of Distance (int) and Direction (list) between the two points 
        """

        # Check if the nodes or edges are valid
        if start not in self.nodes and start not in self.edges:
            sys.exit('Error: Invalid Start Point!')
        elif end not in self.nodes and end not in self.edges:
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
        x_diff = end_x - start_x
        y_diff = end_y - start_y
        distance = math.sqrt(x_diff**2 + y_diff**2)

        # Get the direction either Up, Down, Left or Right
        direction = []
        if y_diff != 0:
            if y_diff > 0:
                direction.append('Up')
            else:
                direction.append('Down')

        if x_diff != 0:
            if x_diff > 0:
                direction.append('Right')
            else:
                direction.append('Left')
        return distance, direction


    # Match node to edges
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
    

    # Find the direction from a given edge
    def decode_edges_to_direction(self):
        """
        Iterates through the whole state space and returns a dictionary of each state and the direction it is headed.

        Returns:
        - A dictionary of states (str) matched with its direction.
        """

        edge_direction = {}
        def get_edge_direction(edge):
            # Find the direction and angle between two nodes to determine the edge direction
            start_node = self.net.getEdge(edge).getFromNode().getID()
            end_node = self.net.getEdge(edge).getToNode().getID()

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
        for edge in self.edges:
            edge_direction[edge] = get_edge_direction(edge)
        return edge_direction


    # Find the actions from a given edges
    def decode_edges_to_actions(self, action_space, edges):
        """
        Translate a list of given edges to their actions

        Args:
        - action_space (dict): The action_space of the agent
        - edges (list): The list of edges to be translated

        Returns:
        - A list of actions (int)
        """

        # Check if edges is in the edges list
        for edge in edges:
            if edge not in self.edges:
                sys.exit(f'Error: Edge {edge} not in Edges Space!')

        # Get the direction of each edge
        edge_direction = self.edge_direction

        # Returns a list of actions
        actions_lst = []
        for action, direction in action_space.items():
            if direction in [edge_direction[edge] for edge in edges]:
                actions_lst.append(action)
        return actions_lst


    # Find the edge from a given edge and action
    def decode_edges_action_to_edge(self, action_space, edges, action):
        """
        Compute the new edge from a given edges and action taken.

        Args:
        - action_space (dict): The action_space of the agent
        - edges (list): The list of edges to be translated
        - action (int): The action taken

        Returns:
        - The new edge (str) or None if no match is found.
        """
        
        # Check if edges is in the edges list
        for edge in edges:
            if edge not in self.edges:
                sys.exit(f'Error: Edge {edge} not in Edges Space!')

        # Get the direction of each edge
        edge_direction = self.edge_direction
        
        for edge in edges:
            if edge_direction[edge] == action_space[action]:
                return edge
        return None
    

    # Find the end node from a given edge
    def decode_edge_to_node(self, search_edge):
        """
        Given an edge return the ending node of that edge

        Args:
        - search_edge (str): The edge to be computed

        Returns:
        - The end node (str)
        """

        # Check if edges is in the edges list
        if search_edge not in self.edges:
            sys.exit('Error: Edge not in Edges Space!')

        edge = self.net.getEdge(search_edge)
        return edge.getToNode().getID()