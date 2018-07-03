# decide next action.
# get cops_state_array and robbers_state_array
# return cops_action_array or robbers_action_array
# if you want to make next_action class, you had better copy or inherit this.

import constant


class NextActionCop:
    # this class is one example of next_action_cop class
    @staticmethod
    def decide_next_action_cop(cops_state_array, robbers_state_array):
        # state has cop/robber id , position and direction
        # return the array of the pair of cop id and action.
        # action is the pair of move and turn.sum of move and turn should be under 1
        # if you want to move only, (1, 0).if turn right, (0, 1).if turn left, (0, -1)
        # if turn right and move, (0.5, 0.5)

        # cops move only straight. not turn

        cops_action_array = []  # the element is the pair of id and action
        for cp in cops_state_array:
            # cp is the state.state is the array of cop id , position and direction
            cops_action_array.append((cp[0], [1, 0]))  # only to move straight.
        return cops_action_array


class NextActionRobber:

    @staticmethod
    def decide_next_action_robber(cops_state_array, robbers_state_array):
        # state has cop/robber id , position and direction
        # return the array of the pair of robber id and action.
        # action is the pair of move and turn.sum of move and turn should be under 1
        # if you want to move only, (1, 0).if turn right, (0, 1).if turn left, (0, -1)
        # if turn right and move, (0.5, 0.5)

        # robbers move to right side.if robber direction is not right, turn to right and move straight
        # robberは右方向に動く。もし向きが右を向いていなければ、右を向くように回転してから、まっすぐ進む。

        robbers_action_array = []
        for rob in robbers_state_array:
            # rob is the state.state is the array of robber id , position and direction
            # position is the pair of x and y.direction is from 0 to 360
            # robber wants to move to right side(direction = 0).
            # if the direction is not 0, turn
            direction = rob[2]
            max_turn = constant.ratio_speed_direction * constant.robber_max_speed
            if direction != 0:
                # the direction is from 0 to 359.999...
                if direction < 180:
                    # turn left
                    if direction < max_turn:
                        # if it turn max, over 0 degree
                        turn_ratio = direction / max_turn
                        action = [1 - turn_ratio, -1*turn_ratio]
                    else:
                        # robber turn max ratio
                        action = [0, -1]
                else:
                    # direction>180, turn right
                    direction = 360.0 - direction  # change to 0 to 180
                    if direction < max_turn:
                        # if it turn max, over 0 degree
                        turn_ratio = direction / max_turn
                        action = [1 - turn_ratio, turn_ratio]
                    else:
                        # robber turn max ratio
                        action = [0, 1]
            else:
                # direction == 0
                action = [1, 0]  # move straight
            robbers_action_array.append((rob[0], action))
        return robbers_action_array
