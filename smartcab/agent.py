import random
import itertools
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        # Variable that records the deadline
        deadline = None
        
        # recording recomendation and actual action for updating the q-table properly
        # recomendation_nwp = None
        # action = None
       
        # Load Q-Tablle:  {'light': light, 'oncoming': oncoming, 'left': left, 'right': right}
        # Dictionary sems to be a good choice for the Q-table: a keys use the tuple of recomendatio_nwp, light, oncoming, left, right and actual action:  for the key.
        
        Q_table = {} # empty dictionary
        
        # creating the key tupels for the Q-table
        states_for_actions = [None, 'forward', 'left', 'right']
        states_for_light = ['green', 'red']
        
        # Q-table keys: 4 recomendation_nwp * 2 light * 4 oncoming * 4 left * 4 right * 4 action = 2 ** 7 = 128 states
        Q_keys = []
        
        for action in states_for_actions:
            for right in states_for_actions:
                    for left in states_for_actions:
                            for oncoming in states_for_actions:
                                for light in states_for_light:
                                    for recomendation_nwp in states_for_actions:
                                        Q_keys.append((recomendation_nwp,light,oncoming,left,right,action)
 
        # Q-table initial values    
        
        Q_initial_values = [random.random() for _ in range(0, len(Q_key))]
        #http://stackoverflow.com/questions/6863309/how-to-create-a-range-of-random-decimal-numbers-between-0-and-1
        #http://stackoverflow.com/questions/1712227/how-to-get-the-size-of-a-list
        
        # Assambling the Q-table dictionary
        
        Q_table = dict(zip(Q_keys,Q_initial_values))
        #http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
        
        # STEP2: Varible for exploration alpha that leads to random action picking
        # alpha = 1
        
        # STEP4: Init Learningrate gamma
        # gamma = 0.2 # learning rate

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        # set deadline to default
        deadline = None
        recomendation_nwp = None
        action = None
        
    
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state

        # How to make use of the planners recomendation ??? By putting them into the state instead of the position!

        # update the recomendation, lights, on coming traffice
        # tupels seame to be the natural choice here

        # update deadline 

        # STEP2: Create a decreasing alpha for exploration
        # if deadline != None
        #   alpha = 1- 1/deadline

        # TODO: Select action according to your policy
        action = self.next_waypoint    # random.choice([None, 'forward', 'left', 'right'])
        
        # filter the Q tablle for current position
        # pick the action/Q-value pair with the highest Q-value
        
        # STEP2: add a if statement that pics a random action from the Q-tablle with alpha percent chance
        # STEP3: tune the action picking depending on the deadline 

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        # update the Q-tablle according to the reward and the current position variable

        # STEP4: Include a learningrate gamma

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
