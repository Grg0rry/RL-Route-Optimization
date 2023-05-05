import numpy as np


class agent:
    def __init__ (self, env, learning_rate = 0.9, discount_factor = 0.1):
        # Define the learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Initialize Q-table
        self.env = env
        self.q_table = np.zeros((len(env.state_space), len(env.action_space)))

        # User Defined
        self.start_node = ""
        self.end_node = ""
        self.start_edges = []
        self.end_edges = []


    # Reset agent
    def reset(self):
        """ Complete reset agent """
        self.__init__(self.env)


    # Set starting and ending nodes
    def set_start_end(self):
        """
        Receive user input to set the Starting and Ending Nodes for the route

        Returns:
        - None
        """
        
        nodes_lst = self.env.nodes

        # Receive Input from User to select starting and ending Nodes
        def node_response(nodes_lst, prompt):
            print(self.env.route_map)
            response = input(prompt).upper()
            if response not in nodes_lst:
                print("Invalid node!!!")
                return node_response(nodes_lst, prompt)
            return response

        # Update class
        self.start_node = "B" #node_response(nodes_lst, "Please Enter a Starting Point ==> ")
        self.end_node =  "N" #node_response(nodes_lst, "Please Enter a Ending Point ==> ")
        self.start_edges = self.env.decode_node_to_edge(self.start_node, 'outgoing')
        self.end_edges = self.env.decode_node_to_edge(self.end_node, 'incoming')


    def act(self, state):
        pass


    def step(self, action, current_state):
        terminate = False
        reward = 0

        if action not in self.env.decode_state_to_actions(current_state): # -- out of bound
            reward = -50
            next_state = current_state
        else:
            next_state = self.env.decode_state_action_to_state(current_state, action)
            if next_state in self.env.blocked_routes: # -- blocked_routes
                reward = -50
                terminate = True
            elif next_state in self.end_edges: # -- completed
                reward = 100
                terminate = True
            else:
                # get distance to completion
                if self.env.get_distance(next_state, self.end_node, 'edge', 'node') < self.env.get_distance(current_state, self.end_node, 'edge', 'node'):
                    reward = 50 # Closer to end node      
        return next_state, reward, terminate


    def learn(self, current_state, action, next_state, reward):
        # Update the Q-table
        q_predict = self.q_table[self.env.state_space.index(current_state)][action]
        q_target = reward + self.discount_factor * np.max(self.q_table[self.env.state_space.index(next_state)])
        self.q_table[self.env.state_space.index(current_state)][action] += self.learning_rate * (q_target - q_predict)


    def train(self, num_episodes):
        logs = {}
        similar = 0
        self.reset()
        self.set_start_end()
        print('Training Started...')

        for episode in range(num_episodes):
            # Initialize state
            state = np.random.choice(self.start_edges)  # -- program chooses a random start edge if there are more than one
            journey = [state]

            while True:
                # Choose an action
                action = self.act(state)
                next_state, reward, terminate = self.step(action, state)

                # Learn from the outcome
                self.learn(state, action, next_state, reward)
                
                # Update state and action
                state = next_state
                journey.append(state)

                if terminate:
                    break

            # Append to logs
            logs[episode] = journey
            print(f'{episode}: {journey}')
            if episode > 0:
                if journey == logs[episode - 1]:
                    similar += 1

            Threshold = 5
            if similar == Threshold:
                print('Training Completed...')
                print(f'Episode {episode}: {journey}\n')
                break
            elif episode == num_episodes:
                print('Training Completed...')
                print(f'Couldnt find shortest path with {num_episodes} episodes\n')
        return logs, episode


class SARSA(agent):
    def __init__ (self, env, exploration_rate = 0.1):
        # Inherit from main agent class
        super().__init__(env)

        # Define additional learning parameter
        self.exploration_rate = exploration_rate


    def act(self, state):
        if np.random.random() < self.exploration_rate:
            # Exploration
            action = np.random.choice(len(self.env.action_space))
        else:
            # Exploitation
            state_index = self.env.state_space.index(state)
            action = np.argmax(self.q_table[state_index])
        return action



class Q_Learning(agent):
    def __init__ (self, env):
        # Inherit from main agent class
        super().__init__(env)


    def act(self, state):
        # Choose action with Highest Q-value
        state_index = self.env.state_space.index(state)
        action = np.argmax(self.q_table[state_index])
        return action

    