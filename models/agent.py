import numpy as np
from collections import Counter
import heapq


class rl_agent:
    def __init__ (self, env, start_node, end_node, learning_rate = 0.9, discount_factor = 0.1):
        # Define the learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Initialize environment
        self.env = env
        self.start_node = start_node
        self.end_node = end_node


    # Reset agent
    def reset(self):
        # Complete reset agent
        self.__init__(self.env, self.start_node, self.end_node)
        self.action_space = self.env.set_start_end(self.start_node, self.end_node)
        self.q_table = np.zeros((len(self.env.state_space), len(self.action_space)))


    def act(self, state):
        pass


    def step(self, action, current_state, current_edge):
        # initialize var
        terminate = False
        reward = 0

        # Get list of outgoing edges     
        outgoing_edges = self.env.decode_node_to_edges(current_state, direction = 'outgoing')

        # Compute reward and next state
        if action not in self.env.decode_edges_to_actions(self.action_space, outgoing_edges): # -- out of bound
            reward -= 50
            next_state = current_state
            next_edge = current_edge
        else:
            next_edge = self.env.decode_edges_action_to_edge(self.action_space, outgoing_edges, action)
            next_state = self.env.decode_edge_to_node(next_edge)

            if next_edge in self.env.blocked_routes: # -- blocked_routes
                reward -= 50
                terminate = True
            elif next_state in self.end_node: # -- completed
                reward += 100
                terminate = True
            else:
                if self.env.get_distance(next_state, self.end_node) < self.env.get_distance(current_state, self.end_node):
                    reward += 0
                elif current_edge != "":
                    if self.env.edge_direction[current_edge] == self.env.edge_direction[next_edge]:
                        reward += 50
                    elif current_edge.replace("-", "") == next_edge.replace("-", ""):
                        reward -= 50
        return next_edge, next_state, reward, terminate


    def learn(self, current_state, action, next_state, reward):
        # Update the Q-table
        q_predict = self.q_table[self.env.state_space.index(current_state)][action]
        q_target = reward + self.discount_factor * np.max(self.q_table[self.env.state_space.index(next_state)])
        self.q_table[self.env.state_space.index(current_state)][action] += self.learning_rate * (q_target - q_predict)


    def train(self, num_episodes, threshold):
        logs = {}
        self.reset()
        print('\nTraining Started...')

        for episode in range(num_episodes):
            # Initialize state
            state = self.start_node
            edge = ""
            state_journey = [state]
            edge_journey = []
            terminate = False

            # Iterate till terminate
            while True:
                if terminate or state in self.end_node:
                    break

                action = self.act(state)
                next_edge, next_state, reward, terminate = self.step(action, state, edge)

                # Learn from the outcome
                self.learn(state, action, next_state, reward)
                
                # Update state
                if state != next_state:
                    edge_journey.append(next_edge)
                    state_journey.append(next_state)
                state = next_state
                edge = next_edge


            # Append to logs and print after every episode
            logs[episode] = [state_journey, edge_journey]
            print(f'{episode}: {logs[episode]}')

            # Compute Convergence
            if episode > 0 and logs[episode][0][-1] == self.end_node:
                
                count_state_lst = Counter(tuple(state_lst[0]) for state_lst in logs.values())
                journey = [list(state_lst) for state_lst, count in count_state_lst.items() if count == threshold]
                
                if len(journey) != 0:
                    print('Training Completed...\n')
                    print(f'Episode {episode}: \n-- States: {logs[episode][0]} \n-- Edges: {logs[episode][1]}')
                    return logs[episode][0], logs[episode][1], episode, logs
                    break
            
            # Unable to converge
            if episode == num_episodes:
                print('Training Completed...')
                print(f'Couldnt find shortest path with {num_episodes} episodes\n')


class SARSA(rl_agent):
    def __init__ (self, env, start_node, end_node, exploration_rate = 0.1):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node)

        # Define additional learning parameter
        self.exploration_rate = exploration_rate


    def act(self, state):
        if np.random.random() < self.exploration_rate:
            # Exploration
            action = np.random.choice(len(self.action_space))
        else:
            # Exploitation
            state_index = self.env.state_space.index(state)
            action = np.argmax(self.q_table[state_index])
        return action


class Q_Learning(rl_agent):
    def __init__ (self, env, start_node, end_node):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node)


    def act(self, state):
        # Choose action with Highest Q-value
        state_index = self.env.state_space.index(state)
        action = np.argmax(self.q_table[state_index])
        return action


class td_agent:
    def __init__ (self, env, start_node, end_node):
        # Initialize environment
        self.env = env
        self.start_node = start_node
        self.end_node = end_node

    
    def reset(self):
        # Initialize the distance and predecessor arrays.
        self.distances = {node: float('inf') for node in self.env.nodes}
        self.predecessor = {node: None for node in self.env.nodes}
        self.distances[self.start_node] = 0
        self.priority_queue = [(0, self.start_node)]


    def search(self):
        self.reset()

        while self.priority_queue:
            current_distance, current_node = heapq.heappop(self.priority_queue)

            # If the node is the end node, then stop searching.
            if current_node == self.end_node:
                break

            # Explore the neighbors nodes
            for neigh_edge in self.env.decode_node_to_edges(current_node, direction = 'outgoing'):
                neigh_node = self.env.decode_edge_to_node(neigh_edge)
                
                # If the neighbor is blocked, then skip it.
                if neigh_edge in self.env.blocked_routes:
                    continue
                
                # Calculate the tentative distance of the neighbor.
                tentative_cost = current_distance + self.env.get_distance(current_node, neigh_node)[0]

                # If the tentative distance is less than the current distance of the neighbor:
                if tentative_cost < self.distances[neigh_node]:
                    # Update the distance of the neighbor.
                    self.distances[neigh_node] = tentative_cost
                    
                    # Update the predecessor of the neighbor.
                    self.predecessor[neigh_node] = current_node
                    
                    # Add the neighbor to the priority queue.
                    self.heap_push(tentative_cost, neigh_node)
                
        # Construct the path from the start node to the goal node.
        node_path = []
        edge_path = []
        current_node = self.end_node
        while current_node is not None:
            node_path.append(current_node)
            current_node = self.predecessor[current_node]
        node_path.reverse()

        for index in range(len(node_path)-1):
            edge = set(self.env.decode_node_to_edges(node_path[index], "outgoing")) & set(self.env.decode_node_to_edges(node_path[index+1], "incoming"))
            edge_path.append(next(iter(edge)))

        # Print out results
        print('Search Completed...')
        print(f'-- States: {node_path} \n-- Edges: {edge_path}')
        return node_path, edge_path


class Dijkstra(td_agent):
    def __init__ (self, env, start_node, end_node):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node)


    def heap_push(self, tentative_cost, neigh_node):
        return heapq.heappush(self.priority_queue, (tentative_cost, neigh_node))


class A_Star(td_agent):
    def __init__ (self, env, start_node, end_node):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node)


    def heap_push(self, tentative_cost, neigh_node):
        return heapq.heappush(self.priority_queue, (tentative_cost + self.heuristic(neigh_node, self.end_node), neigh_node))
    

    def heuristic(self, neigh_node, end_node):
        start_x, start_y = self.env.net.getNode(neigh_node).getCoord()
        end_x, end_y = self.env.net.getNode(end_node).getCoord()
        return abs(start_x - end_x) + abs(start_y - end_y)

        
