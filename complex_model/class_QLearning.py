class QLearning:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.Q = np.zeros((num_states, num_actions))

    def choose_action(self, state, available_actions):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(available_actions)
        else:
            return np.argmax(self.Q[state, available_actions])

    def update(self, state, action, reward, next_state):
        td_target = reward + self.discount_factor * np.max(self.Q[next_state])
        td_error = td_target - self.Q[state, action]
        self.Q[state, action] += self.learning_rate * td_error
