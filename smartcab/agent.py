import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
        
        # Global variable for the Q-Table
    Q_table = {}
 
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        # Variable that records the deadline
        #deadline = None
        
        # recording recomendation and actual action for updating the q-table properly
        #recomendation_nwp = None
        #state = None
        #action = None
        #decision_table = {}

        # creating the key tupels for the Q-table
        # recomendation_nwp, light, oncoming, right, action)
        states_for_recomendation_nwp = ['forward', 'left', 'right']
        states_for_light = ['green', 'red']        
        states_for_actions = [None, 'forward', 'left', 'right']
        
        # Q-table keys: 3 recomendation_nwp * 2 light * 4 oncoming  * 4 right * 4 action = 384 states
        Q_keys = []
        
        for action in states_for_actions:
            for right in states_for_actions:
                for oncoming in states_for_actions:
                    for light in states_for_light:
                        for recomendation_nwp in states_for_recomendation_nwp:
                            Q_keys.append((recomendation_nwp,light,oncoming,right,action))
 
        # Q-table initial values    
        # Q_initial_values = [random.random() for _ in range(0, len(Q_keys))] 
        Q_initial_values = [int(random.random() * 10) for _ in range(0, len(Q_keys))] 
        # QUESTION: can I incentivese exploration in the beginning by setting very hight inital values?
        # http://stackoverflow.com/questions/16655089/python-random-numbers-into-a-list
        # http://stackoverflow.com/questions/6863309/how-to-create-a-range-of-random-decimal-numbers-between-0-and-1
        # http://stackoverflow.com/questions/1712227/how-to-get-the-size-of-a-list

        
        # Assambling the Q-table dictionary
        global Q_table
        Q_table = dict(zip(Q_keys,Q_initial_values))
        #http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
        
        #Performance mesurement
        global totalReward        
        totalReward = 0.0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        #deadline = None
        #recomendation_nwp = None
        #state = None
        #action = None
        #decision_table = {}
    
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        #print type(self.next_waypoint) #forward
        #print (inputs) # {'light': 'green', 'oncoming': None, 'right': None, 'left': None}
        #print (deadline) #25. int

        # TODO: Update state

        state = ((self.next_waypoint,) + tuple(inputs.values()[0:3])) # without the left input
        #         (recomendation_nwp)  + (light,oncoming,right)
        # http://stackoverflow.com/questions/16449184/python-converting-string-to-tuple-without-splitting-characters        
        # http://stackoverflow.com/questions/7002429/how-can-i-extract-all-values-from-a-dictionary-in-python
        # http://stackoverflow.com/questions/12836128/python-convert-list-to-tuple        

        # TODO: Select action according to your policy
        
        # fetching the Q-values for the possible actions into a decision table     
        decision_table = {None: Q_table[(state + (None,))], 'right': Q_table[(state + ('right',))], 'left': Q_table[(state + ('left',))], 'forward': Q_table[(state + ('forward',))]}        

        # Exploitation rate gamma
        gamma = (1 / (deadline + 0.00001)) + 0.9

        if  random.random() < gamma:
            # pick the action/Q-value pair with the highest Q-value to Exploit the Q table
            maxQval, action = max((v, k) for k, v in decision_table.iteritems())       
            # http://stackoverflow.com/questions/9693816/searching-dictionary-for-max-value-then-grabbing-associated-key
        
        else:
            # pick a random action to explore
            action =  random.choice([None, 'forward', 'left', 'right'])
            # get the (not neccessarily really max) maxQval form the decision table
            maxQval = decision_table [action]
            
        # Simple Agent: 
        # action = self.next_waypoint 
        
        # Random Agent: 
        # action =  random.choice([None, 'forward', 'left', 'right'])
        

        # ADDITION: tune the action picking depending on the deadline: exploration/exploitation

        # Execute action and get reward
        reward = self.env.act(self, action)
        #valid_actions = [None, 'forward', 'left', 'right']

        # TODO: Learn policy based on state, action, reward
           
        # decreasing learning rate alpha
        alpha = 1/((t/50)+1)

        # update the Q-tablle according to the reward and the stats maxQval
        Q_table[(state + (action,))] = (maxQval + (alpha * reward))
        # http://www.tutorialspoint.com/python/python_dictionary.htm
        
        global totalReward
        totalReward = totalReward + reward
       
        print "Q learning: state = {}, action = {}, maxQval = {}, reward = {}, timestep = {}, totalReward = {} \n".format(state, action, maxQval, reward, t, totalReward)
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
