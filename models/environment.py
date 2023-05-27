import sys
import sumolib
import math
import random


class traffic_env:
    def __init__ (self, network_file, blocked_routes = [], random_edge = 6):
        # Parameters 
        self.net = sumolib.net.readNet(network_file)
        self.nodes = [node.getID().upper() for node in self.net.getNodes()]
        self.edges = [edge.getID() for edge in self.net.getEdges()]
        self.action_space = [0, 1, 2, 3]
        self.state_space = self.nodes
        self.edge_label = self.decode_edges_to_label()

        # Define route nature
        if not blocked_routes:
            self.blocked_routes = random.choices(self.edges, k = random_edge)
        else:
            self.blocked_routes = blocked_routes
        print(f'Blocked Routes: {self.blocked_routes}\n')


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

        return distance


    # Match node to edges
    def decode_node_to_edges(self, node, direction = None):
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
        
        return edges
    

    # Label edges based of junction from (Right -> Up -> Left -> Down)
    def decode_edges_to_label(self):
        """
        Iterates through the whole state space and returns a dictionary of each state and the direction it is headed.

        Returns:
        - A dictionary of states (str) matched with its direction.
        """

        edge_labelled = {edge: None for edge in self.edges}
        
        def get_edge_label(node, outgoing_edges):
            # store edge angle
            edge_angle = []

            # get the nodes outgoing
            start_x, start_y = self.net.getNode(node).getCoord()
            
            # get outgoing edges
            for edge in outgoing_edges:
                end_node = self.decode_edge_to_node(edge)
                end_x, end_y = self.net.getNode(end_node).getCoord()

                x_diff = end_x - start_x
                y_diff = end_y - start_y

                # get their angle
                angle = math.degrees(math.atan2(y_diff, x_diff))
                edge_angle.append((edge, angle))

            # sort from 0 to 180 to -180 to 0 (Right -> Up -> Left -> Down -> Right)
            edge_angle = sorted(edge_angle, key=lambda x: ((x[1] >= 0) * -180, x[1]))
            
            # label edges
            for i in range(len(edge_angle)):
                edge_labelled[edge_angle[i][0]] = i

        for node in self.nodes:
            outgoing_edges = self.decode_node_to_edges(node, 'outgoing')
            if outgoing_edges:
                get_edge_label(node, outgoing_edges)
        return edge_labelled


    # Find the actions from a given edges
    def decode_edges_to_actions(self, edges):
        """
        Translate a list of given edges to their actions

        Args:
        - edges (list): The list of edges to be translated

        Returns:
        - A list of actions (int)
        """

        # Check if edges is in the edges list
        for edge in edges:
            if edge not in self.edges:
                sys.exit(f'Error: Edge {edge} not in Edges Space!')

        # Get the label of each edge
        edge_label = self.edge_label

        # Returns a list of actions
        actions_lst = []
        for action in self.action_space:
            if action in [edge_label[edge] for edge in edges]:
                actions_lst.append(action)
        return actions_lst


    # Find the edge from a given edge and action
    def decode_edges_action_to_edge(self, edges, action):
        """
        Compute the new edge from a given edges and action taken.

        Args:
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
        edge_label = self.edge_label
        
        for edge in edges:
            if edge_label[edge] == action:
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