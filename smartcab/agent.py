import random
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
        
        # Variable to recording the current position
        # Variable that records the deadline
        # STEP2: Varible that stears the chance for random action picing

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        # Load the Q-Tablle
        # set current position and deadline to defulte
        
    
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state

        # update the current position
        # update situation: traffic lights, on coming traffice, heading
        # update deadline 

        # TODO: Select action according to your policy
        action = random.choice([None, 'forward', 'left', 'right'])
        
        # filter the Q tablle for current position
        # pic the action/Q-value pair with the highest Q-value
        
        # STEP2: add a if statement that pics a random action from the Q-tablle with alpha percent chance
        # STEP3: tune the action picking depending on the deadline 

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        # update the Q-tablle according to the reward and the current position variable 

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
