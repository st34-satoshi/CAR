import constant
from calculation import calc
from decide_action import calc_action


class CopSimpleChase:
    cop_leave_cop = 2  # the weight cop want to leave from the cops.
    cop_weight_to_robber = 10  # the weight cop want to go to the nearest robber.
    max_turn = constant.cop_max_speed*constant.ratio_speed_direction

    def __init__(self, environment):
        self.environment = environment

    def leave_cop(self, cops_state_array, position):
        # cops try to leave from the other cops.
        mini = constant.robber_radius * 2 + constant.cop_radius * 2  # robberの直径+copの直径
        sum_direction = 0
        sum_weight = 0
        for cop in cops_state_array:
            c_posi = cop[1]
            if not (c_posi[0] == position[0] and c_posi[1] == position[1]):
                # except myself
                dis = self.environment.distance(position, c_posi)
                if dis < mini:
                    weight = (mini - dis) * self.cop_leave_cop
                    direction = self.environment.aim_direction(c_posi, position)
                    vector_leave = calc.synthesis_vector(direction, weight, sum_direction, sum_weight, self.environment)
                    sum_direction = vector_leave[0]
                    sum_weight = vector_leave[1]
        return sum_direction, sum_weight

    def direction_to_robber(self, robbers_state_array, position, direction):
        # cop try to go to the position robber is.一番近いrobberに行く方向とweight
        if not robbers_state_array:
            # when the list robber is empty.list_robbersが空
            return 0, 0
        rob_near = robbers_state_array[0]
        mini = self.environment.max_distance()  # big number
        for rob in robbers_state_array:
            dis = self.environment.distance_with_turn(position, rob[1], direction)
            if dis < mini:
                mini = dis
                rob_near = rob
        return self.environment.aim_direction(position, rob_near[1]), self.cop_weight_to_robber

    def aim_direction(self, state, cops_state_array, robbers_state_array):
        # decide the direction to go.
        # state is id, position, direction
        if not robbers_state_array:
            return 0
        v_leave_cop = self.leave_cop(cops_state_array, state[1])
        v_to_robber = self.direction_to_robber(robbers_state_array, state[1], state[2])
        v_sum = calc.synthesis_vector(v_leave_cop[0], v_leave_cop[1], v_to_robber[0], v_to_robber[1], self.environment)
        return v_sum[0]

    def square_normal(self, cops_state_array, robbers_state_array):
        cops_action_array = []
        for cp in cops_state_array:
            aim_direction = self.aim_direction(cp, cops_state_array, robbers_state_array)
            move_turn = calc_action.move_to_aim_direction(cp[2], aim_direction, self.max_turn)
            cops_action_array.append((cp[0], [move_turn[0], move_turn[1]]))
        return cops_action_array

    def decide_next_action_cop(self, cops_state_array, robbers_state_array):
        # cop chase the robber simply
        if self.environment.environment_type() == 'square':
            return self.square_normal(cops_state_array, robbers_state_array)
        print("no environment in decide_next_action_cop in cop_simple_chase")
        return []

