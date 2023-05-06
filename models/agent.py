import numpy as np


class agent:
    def __init__ (self, env, learning_rate = 0.9, discount_factor = 0.1):
        # Define the learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Initialize environment
        self.env = env
        
    # Reset agent
    def reset(self):
        """ Complete reset agent """
        self.__init__(self.env)
        self.start_node, self.end_node, self.start_edges, self.end_edges, self.action_space = self.env.set_start_end()
        self.q_table = np.zeros((len(self.env.state_space), len(self.action_space)))


    def act(self, state):
        pass


    def step(self, action, current_state):
        terminate = False
        reward = 0
        # print(f'state: {current_state}, action: {action}')

        if action not in self.env.decode_state_to_actions(self.action_space, current_state): # -- out of bound
            reward = -50
            next_state = current_state
        else:
            next_state = self.env.decode_state_action_to_state(self.action_space, current_state, action)
            if next_state in self.env.blocked_routes: # -- blocked_routes
                reward = -50
                terminate = True
            elif next_state in self.end_edges: # -- completed
                reward = 100
                terminate = True
            else:
                if current_state.replace("-", "") == next_state.replace("-", ""):
                    reward = -50
                elif self.env.state_direction[current_state] == self.env.state_direction[next_state]:
                    reward = 50
                elif self.env.get_distance(next_state, self.end_node, 'edge', 'node') < self.env.get_distance(current_state, self.end_node, 'edge', 'node'):
                    reward = 50

            # else:
            #     # get distance to completion
            #     if self.env.get_distance(next_state, self.end_node, 'edge', 'node') < self.env.get_distance(current_state, self.end_node, 'edge', 'node'):
            #         reward = 50 # Closer to end node      
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
        print('Training Started...')

        for episode in range(num_episodes):
            # Initialize state
            

            ## D
            self.start_edges = ['-gneE10', 'gneE11']
            ^       
            np.argmax(self.q_table['gneE10'])
            ^

            ## G
            self.start_edges = ['-gneE11', '-gneE16', 'gneE12']
            ^       
            np.argmax(self.q_table['gneE16'])
            ^

            ## C
            self.start_edges = ['-gneE0', '-gneE5', 'gneE1', 'gneE10']


            
            index_list = [self.env.state_space.index(state) for state in self.start_edges]
            arr = self.q_table[index_list]
            max_value = np.max(arr)
            max_row_index = np.where(arr == max_value)[0][0]
            state = self.env.state_space[index_list[max_row_index]]


            #state = np.random.choice(self.start_edges)
            journey = [state]
            terminate = False
            # status = {prev_state: "", prev_action: None, curr_state: state, curr_action = None, next_state: "", next_state: None}

            while True:
                if terminate or state in self.end_edges:
                    break

                # Choose an action
                action = self.act(state)
                next_state, reward, terminate = self.step(action, state)
                # print(f'state: {state}; reward: {reward}')

                # Learn from the outcome
                self.learn(state, action, next_state, reward)
                
                # Update state and action
                state = next_state
                journey.append(state)

            #print(self.q_table)

            # Append to logs
            logs[episode] = journey
            print(f'{episode}: {journey}')
            if episode > 0 and journey[-1] in self.end_edges:
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
            action = np.random.choice(len(self.action_space))
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
        #print(f'state: {state}, action: {self.q_table[state_index]}')
        #print(action)
        return action

    