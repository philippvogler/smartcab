import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from math import log
import matplotlib.pyplot as plt
from numpy import mean

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        states_for_recomendation_nwp = ['forward', 'left', 'right']
        states_for_light = ['green', 'red']
        states_for_actions = [None, 'forward', 'left', 'right']

        # Q-table keys: 3 recomendation_nwp * 2 light * 4 oncoming  * 4 left * 4 action = 384 states
        Q_keys = []

        for action in states_for_actions:
            for left in states_for_actions:
                for oncoming in states_for_actions:
                    for light in states_for_light:
                        for recomendation_nwp in states_for_recomendation_nwp:
                            Q_keys.append((recomendation_nwp,light,oncoming,left,action))

        # Q-table initial values
        Q_initial_values = [random.random() * 4 for _ in range(0, len(Q_keys))] #[0] * len(Q_keys)

        # http://stackoverflow.com/questions/16655089/python-random-numbers-into-a-list
        # http://stackoverflow.com/questions/6863309/how-to-create-a-range-of-random-decimal-numbers-between-0-and-1
        # http://stackoverflow.com/questions/1712227/how-to-get-the-size-of-a-list

        # Assembling the Q-table dictionary
        global Q_table
        Q_table = dict(zip(Q_keys,Q_initial_values))
        #http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python

        #reward list for performance tracking       
        global total_reward        
        total_reward = 0.0
        
        global number_of_actions        
        number_of_actions = 1
        
        global total_reward_list
        total_reward_list = []
        
        global average_reward_list
        average_reward_list = []

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        # Performance tracking
        global total_reward
        global number_of_actions  
        total_reward_list.append(total_reward/number_of_actions)
        average_reward_list.append (mean(total_reward_list))
        
        # Performance chart
        plt.figure(1)
       
        plt.subplot(211)        
        plt.plot(total_reward_list)
 
        plt.title('Performance of learning agent')
        plt.xlabel('# trail')
        plt.ylabel('reward / step')
        
        plt.subplot(212)
        plt.plot(average_reward_list)     
        
        plt.xlabel('# trails')
        plt.ylabel('average reward')
        
        #print "Average reward per action in this run: {} ".format(total_reward/number_of_actions)
        #print "Average total reward over all: {} \n".format(np.mean(total_reward_list))        
        
        # Restet reward counting for the next run
        total_reward = 0.0

      
        number_of_actions = 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self) #{'left': None, 'light': 'green', 'oncoming': None, 'right': None}
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        state = ((self.next_waypoint,) + (inputs['light'], inputs['oncoming'], inputs['left']))
        
        self.state = "NWP: {} / LIGHTS: {} / ONCOMING: {} / ROW: {}".format(state[0],state[1],state[2],state[3])

        # http://stackoverflow.com/questions/16449184/python-converting-string-to-tuple-without-splitting-characters
        # http://stackoverflow.com/questions/7002429/how-can-i-extract-all-values-from-a-dictionary-in-python
        # http://stackoverflow.com/questions/12836128/python-convert-list-to-tuple

        # TODO: Select action according to your policy
        # Fetching the Q-values for the possible actions into a decision table
        decision_table = {None: Q_table[(state + (None,))], 'right': Q_table[(state + ('right',))], 'left': Q_table[(state + ('left',))], 'forward': Q_table[(state + ('forward',))]}

        # Exploration rate epsilon
        epsilon = (log(deadline+0.0001)) * 0.0155

        if  epsilon < random.random():
            # picking the action/Q-value pair with the highest Q-value to exploit the Q table
            curr_qval, action = max((v, k) for k, v in decision_table.iteritems())

        else:
            # picking a random action/Q-value pair with the highest Q-value to explore the Q table
            action =  random.choice([None, 'forward', 'left', 'right'])
            curr_qval = decision_table [(action)]

        #http://stackoverflow.com/questions/9693816/searching-dictionary-for-max-value-then-grabbing-associated-key

        #----
        # Simple Agent:
        # action = self.next_waypoint
        # curr_qval, action = decision_table [(self.next_waypoint)], (self.next_waypoint)

        # Random Agent:
        # action =  random.choice([None, 'forward', 'left', 'right'])

        #----

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        # Set learning rate alpha
        alpha = (1.0 / (t+5)) + 0.75
        
        # Set discount gamma
        gamma = 0.4

        # Build new state
        newinputs = self.env.sense(self)
        newstate = ((self.next_waypoint,) + (newinputs['light'], newinputs['oncoming'], newinputs['left']))

        # Future rewards from q table
        future_table = {None: Q_table[(newstate + (None,))], 'right': Q_table[(newstate + ('right',))], 'left': Q_table[(newstate + ('left',))], 'forward': Q_table[(newstate + ('forward',))]}

        # Max future reward
        future_reward, future_action = max((v, k) for k, v in future_table.iteritems())

        # Calculate new Q-value
        new_qval = reward + gamma * future_reward

        # Update the Q-table
        Q_table[(state + (action,))] = curr_qval + alpha * (new_qval - curr_qval)

        # Performance tracking
        global number_of_actions        
        number_of_actions = number_of_actions + 1
        
        global total_reward   
        total_reward = total_reward + reward

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=30)  # press Esc or close pygame window to quit
    
    plt.show()
   

if __name__ == '__main__':
    run()
