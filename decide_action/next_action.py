# decide next action.
# get cops_state_array and robbers_state_array
# return cops_action_array and _robbers_action_array
# if you want to make decide_action class, you had better copy this.


class NextAction:

    @staticmethod
    def decide_next_action(cops_state_array, robbers_state_array):
        # state has cop/robber id , position and direction
        # action is id and the pair of move and turn.sum of move and turn should be under 1
        # if you want to move only, (1, 0).if turn right, (0, 1).if turn left, (0, -1)
        # if turn right and move, (0.5, 0.5)

        cops_action_array = []
        robbers_action_array = []
        for cp in cops_state_array:
            cops_action_array.append((cp[0], [1, 0]))
        for rob in robbers_state_array:
            robbers_action_array.append((rob[0], [1, 0]))
        return cops_action_array, robbers_action_array
