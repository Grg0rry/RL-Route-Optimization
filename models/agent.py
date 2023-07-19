import numpy as np
import sys
import datetime


class rl_agent():
    def __init__ (self, env, start_node, end_node, learning_rate, discount_factor):
        # Define the learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Initialize environment
        self.env = env
        self.env.set_start_end(start_node, end_node)


    # Reset/Initialize agent
    def reset(self):
        self.q_table = np.zeros((len(self.env.state_space), len(self.env.action_space)))
        self.logs = {}
        self.best_result = 0


    def act(self):
        pass


    def step(self, action, state_list, edge_list):
        # initialize step
        terminate = False
        current_state = state_list[-1]
        current_edge = edge_list[-1] if edge_list else None

        # reward paramaters -- **change values here**
        invalid_action_reward = -50
        dead_end_reward = -50
        loop_reward = -50
        # loop_reward = -30
        completion_reward = 50
        bonus_reward = 50 
        # bonus_reward = ((self.best_result-current_result)/self.best_result)*100 + 50
        continue_reward = 0

        # Get list of outgoing edges     
        outgoing_edges = self.env.decode_node_to_edges(current_state, direction = 'outgoing')

        # Compute reward and next state
        # Out-Of-Bound Action
        if action not in self.env.decode_edges_to_actions(outgoing_edges):
            reward += invalid_action_reward
            next_state = current_state
            next_edge = current_edge

        # Valid Action
        else:
            next_edge = self.env.decode_edges_action_to_edge(outgoing_edges, action)
            next_state = self.env.decode_edge_to_node(next_edge, direction = 'end')
            reward = continue_reward

            # Completed Route
            if next_state in self.env.end_node:
                reward += completion_reward
                terminate = True

                # check if the route is the shortest distance/time
                if self.env.evaluation in ("distance", "d"):
                    current_result = self.env.get_edge_distance(edge_list + [next_edge])
                else:
                    current_result = self.env.get_edge_time(edge_list + [next_edge])

                # evaluation
                if self.best_result == 0:
                    self.best_result = current_result
                elif current_result < self.best_result:
                    for edge in edge_list:
                        state_index = self.env.state_space.index(self.env.decode_edge_to_node(edge, direction = 'start'))
                        action_index = self.env.edge_label[edge]
                        self.q_table[state_index][action_index] += bonus_reward
                    self.best_result = current_result

            # Dead-end Route
            elif not self.env.decode_node_to_edges(next_state, direction = 'outgoing'):
                reward += dead_end_reward
                terminate = True

                # Backtrack and find bottleneck
                for edge in reversed(edge_list):
                    if len(self.env.decode_node_to_edges(self.env.decode_edge_to_node(edge, direction = 'end'), direction = 'outgoing')) > 1:
                        break

                    state_index = self.env.state_space.index(self.env.decode_edge_to_node(edge, direction = 'start'))
                    action_index = self.env.edge_label[edge]
                    self.q_table[state_index][action_index] += dead_end_reward
            
            # Travelling
            elif current_edge != None:
                if (current_edge, next_edge) in [(edge_list[i], edge_list[i+1]) for i in range(len(edge_list)-1)]: # Check if its in a loop
                    reward += loop_reward

        return next_edge, next_state, reward, terminate


    def learn(self, current_state, action, next_state, reward):
        # Update the Q-table
        q_predict = self.q_table[self.env.state_space.index(current_state)][action]
        q_target = reward + self.discount_factor * np.max(self.q_table[self.env.state_space.index(next_state)])
        self.q_table[self.env.state_space.index(current_state)][action] += self.learning_rate * (q_target - q_predict)


    def train(self, num_episodes, threshold):
        start_time = datetime.datetime.now() # time the training process
        self.reset()
        # print('Training Started...')

        for episode in range(num_episodes):
            # Initialize state
            state_journey = [self.env.start_node]
            edge_journey = []
            terminate = False

            # Iterate till terminate
            while True:
                last_state = state_journey[-1]
                if terminate or last_state in self.env.end_node:
                    break

                action = self.act(last_state)
                next_edge, next_state, reward, terminate = self.step(action, state_journey, edge_journey)

                # Learn from the outcome
                self.learn(last_state, action, next_state, reward)

                # Update state
                if last_state != next_state:
                    edge_journey.append(next_edge)
                    state_journey.append(next_state)

            # Append to logs and print after every episode
            self.logs[episode] = [state_journey, edge_journey]
            
            # print(f'{episode}: {self.logs[episode]}')

            # Compute Convergence
            if episode > threshold and self.logs[episode][0][-1] == self.env.end_node:

                # Convergence when 5 consecutive same routes produced
                threshold_lst = list(self.logs.values())[-threshold:]
                if all(x == threshold_lst[0] for x in threshold_lst):
                    end_time = datetime.datetime.now()
                    time_difference = end_time - start_time
                    processing_seconds = time_difference.total_seconds()

                    # --- results output ---
                    print('Training Completed...\n')
                    print(f'Episode {episode}:\n-- States: {self.logs[episode][0]} \n-- Edges: {self.logs[episode][1]}')
                    print(f'-- Processing Time: {processing_seconds} seconds')
                    
                    if self.env.evaluation in ("distance", "d"):
                        print(f'-- Distance travelled: {round(self.env.get_edge_distance(self.logs[episode][1]), 2)} m')
                    else:
                        print(f'-- Travelled Time taken: {round(self.env.get_edge_time(self.logs[episode][1]), 2)} mins')

                    return self.logs[episode][0], self.logs[episode][1], episode, self.logs

            # Unable to converge
            if episode+1 == num_episodes:
                print('Training Completed...')
                end_time = datetime.datetime.now()
                time_difference = end_time - start_time
                processing_seconds = time_difference.total_seconds()
                print(f'-- Processing Time: {processing_seconds} seconds')
                sys.exit(f'Couldnt find shortest path with {num_episodes} episodes')


class SARSA(rl_agent):
    def __init__ (self, env, start_node, end_node, learning_rate = 0.9, discount_factor = 0.1, exploration_rate = 0.1):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node, learning_rate, discount_factor)

        # Define additional parameter
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


class Q_Learning(rl_agent):
    def __init__ (self, env, start_node, end_node, learning_rate = 0.9, discount_factor = 0.1):
        # Inherit from main agent class
        super().__init__(env, start_node, end_node, learning_rate, discount_factor)


    def act(self, state):
        # Choose action with Highest Q-value
        state_index = self.env.state_space.index(state)
        action = np.argmax(self.q_table[state_index])
        return action
