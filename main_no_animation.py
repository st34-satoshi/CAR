
import constant
from player import cop
from player import robber
from environment import make_environment
from decide_action import next_action
from calculation import calc
from decide_action import cop_simple_chase
from decide_action import robber_flee_complicatedly

import sys


def main_no_animation():
    # make first state.
    environment = make_environment.make_environment()
    cops_array = []
    robbers_array = []
    id = 1
    for i in range(constant.cops_number):
        cp = cop.Cop(environment, id)
        cops_array.append(cp)
        id += 1
    for i in range(constant.robbers_number):
        rob = robber.Robber(environment, id)
        robbers_array.append(rob)
        id += 1
    # change here to change the algorithm of cops move
    action_cop_class = cop_simple_chase.CopSimpleChase(environment)  # next_action.NextActionCop()
    # change here to change the algorithm of robbers move
    action_robber_class = robber_flee_complicatedly.RobberFleeComp(environment, robbers_array)  # next_action.NextActionRobber()
    steps = 0  # count steps to know the terminating steps
    while True:
        # check collision cops and robbers
        collision_robber_array = calc.collision_robbers_array(cops_array, robbers_array, environment)
        for rob in collision_robber_array:
            robbers_array.remove(rob)
            # print("remove robber id = " + str(rob.id))
        if not robbers_array:
            # there is no robber. it means the end of the game.
            # print("terminate the game! steps = "+str(steps))
            break
        steps += 1
        # make state array. state has id, position, direction
        cops_state_array = []
        robbers_state_array = []
        for cp in cops_array:
            cops_state_array.append(cp.make_state())
        for rob in robbers_array:
            robbers_state_array.append(rob.make_state())
        # decide next action.move cops and robbers. and change to next state
        cops_action_array = action_cop_class.decide_next_action_cop(cops_state_array, robbers_state_array)
        robbers_action_array = action_robber_class.decide_next_action_robber(cops_state_array, robbers_state_array)
        for cp in cops_array:
            if not cp.human:
                for cp_action in cops_action_array:
                    if cp.id == cp_action[0]:
                        cp.move_cop(cp_action[1][0], cp_action[1][1], environment)
                        break
        for rob in robbers_array:
            if not rob.human:
                for rob_action in robbers_action_array:
                    if rob.id == rob_action[0]:
                        rob.move_robber(rob_action[1][0], rob_action[1][1], environment)
    return steps


if __name__ == '__main__':
    terminate_steps = main_no_animation()
    print("the game end. steps = "+str(terminate_steps))
