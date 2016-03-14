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
        recomendation_nwp = None
        actual_action = None
        start_state = None
       
        # Load Q-Tablle: (state), (location), (heading), next_waypoint  {'light': light, 'oncoming': oncoming, 'left': left, 'right': right}
        # Dictionary sems to be a good choice for the Q-Tablle: a keys use the tuple of recomendation, light, oncoming*, and actual action: as values the q value for the key.
        # the initial starting q-values/Dictionaty values should be random -1 to +1
        # Heading, left and right do not make muche sens to the here as they should not be significant to the decision
        Q_table = {} # empty dictionary
        
        # creating the key tupels for the Q table
        states_for_actions = [None, 'forward', 'left', 'right']
        states_for_light = ['green', 'red']
        
        # 2 light * 4 oncoming * 4 left * 4 right * 4 next_waypoint * 4 actual_action = 2 ** 7 = 128 states
        # How to populate a dictionary efficiently?? izip, zip or combinatoric generators
        
        # so geht es nicht. Die itertools sind nicht dafür gemacht.
        action_tupels = itertools.product(states_for_actions, repeat=5)
        print (action_tupels)
        type(action_tupels)
        light_tupels = itertools.cycle(states_for_light, (len(action_tupels)/2))
        Q_keys = zi p(light_tupels, action_tupels)
        
        print Q_keys
        
        # STEP2: Varible for exploration alpha that leads to random action picking
        # alpha = 1
        
        # STEP4: Init Learningrate gamma
        # gamma = 0.2 # learning rate

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        # reload the Q-Tablle
        # set current position and deadline to default
        
    
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
        action = random.choice([None, 'forward', 'left', 'right'])
        
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
