import heapq
import datetime


class Dijkstra:
    def __init__ (self, env, start_node, end_node):
        # Initialize environment
        self.env = env
        self.env.set_start_end(start_node, end_node)


    def reset(self):
        # Initialize the distance and predecessor arrays.
        self.cost = {node: float('inf') for node in self.env.nodes}
        self.predecessor = {node: None for node in self.env.nodes}
        self.cost[self.env.start_node] = 0
        self.priority_queue = [(0, self.env.start_node)]


    def cost_funct(self, current_cost, neigh_edge):
        if self.env.evaluation in ("distance", "d"):
            cost = current_cost + self.env.get_edge_distance(neigh_edge)
        else:
            cost = current_cost + self.env.get_edge_time(neigh_edge)
        return cost


    def search(self):
        start_time = datetime.datetime.now()
        self.reset()

        while self.priority_queue:
            current_cost, current_node = heapq.heappop(self.priority_queue)

            # If the node is the end node, then stop searching.
            if current_node == self.env.end_node:
                break

            # Explore the neighbors nodes
            for neigh_edge in self.env.decode_node_to_edges(current_node, direction = 'outgoing'):
                neigh_node = self.env.decode_edge_to_node(neigh_edge, direction = 'end')
                
                # Calculate the cost of the neighbor.
                tentative_cost = self.cost_funct(current_cost, neigh_edge)

                # If the tentative distance is less than the current distance of the neighbor:
                if tentative_cost < self.cost[neigh_node]:
                    # Update the distance of the neighbor.
                    self.cost[neigh_node] = tentative_cost
                    
                    # Update the predecessor of the neighbor.
                    self.predecessor[neigh_node] = current_node
                    
                    # Add the neighbor to the priority queue.
                    heapq.heappush(self.priority_queue, (tentative_cost, neigh_node))
                
        # Construct the path from the start node to the goal node.
        node_path = []
        edge_path = []
        current_node = self.env.end_node
        while current_node is not None:
            node_path.append(current_node)
            current_node = self.predecessor[current_node]
        node_path.reverse()

        for index in range(len(node_path)-1):
            edge = set(self.env.decode_node_to_edges(node_path[index], "outgoing")) & set(self.env.decode_node_to_edges(node_path[index+1], "incoming"))
            edge_path.append(next(iter(edge)))

        # time the search process
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        processing_seconds = time_difference.total_seconds()

        # Print out results
        print('Search Completed...')
        print(f'-- States: {node_path} \n-- Edges: {edge_path}')
        print(f'-- Processing Time: {processing_seconds} seconds')
        
        if self.env.evaluation in ("distance", "d"):
            print(f'-- Distance travelled: {round(self.env.get_edge_distance(edge_path), 2)} m')
        else:
            print(f'-- Travelled Time taken: {round(self.env.get_edge_time(edge_path), 2)} mins')

        return node_path, edge_path