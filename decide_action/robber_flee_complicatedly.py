import constant
from decide_action import calc_action
from decide_action import for_robber_comp
from environment import make_environment

import random


class StateRobber:
    # 0:move randomly,1:close to the wall、2:close to the cops
    # 3:stop because surrounded by cops, 4:cops are to close.emergency
    def __init__(self, id):
        self.state = 0
        self.state_count = 0
        self.aim_direction = 0
        self.id = id
        self.placed_array = []
        self.placed_count = 0
        self.robber_save_place_interval = (constant.robber_radius/constant.robber_max_speed)+20
        self.robber_max_save_place = 5

    def set_aim_direction(self, aim_direction):
        self.aim_direction = aim_direction

    def set_state_free(self):
        # set state free.
        self.state = 0
        self.state_count = 0

    def set_state_stop(self):
        self.state = 3
        self.state_count = 0

    def set_placed_list_empty(self):
        self.placed_array = []

    def set_state_emergency(self):
        self.state = 4
        self.state_count = 0

    def set_state_escape_from_wall(self):
        # set state escape from the wall.
        self.state = 1
        self.state_count = 0

    def set_state_flee(self):
        self.state_count = 0
        self.state = 2

    def get_end_state(self, max_number):
        # check the state is finished state.
        if self.state_count > max_number:
            return True
        return False

    def get_state_free(self):
        if self.state == 0:
            return True
        return False

    def get_state_flee(self):
        if self.state == 2:
            return True
        return False

    def get_state_emergency(self):
        if self.state == 4:
            return True
        return False

    def get_state_escape_from_wall(self):
        if self.state == 1:
            return True
        return False

    def get_state_move_free(self):
        # check the state is move_randomly or escape from the wall.
        if self.get_state_free() or self.get_state_escape_from_wall():
            return True
        return False

    def get_state_stop(self):
        if self.state == 3:
            return True
        return False

    def get_placed_list(self):
        return self.placed_array

    def print_state(self):
        print("state: "+str(self.state)+", "+ str(self.state_count))

    def add_state_count(self):
        self.state_count += 1

    def check_stop(self, position, environment):
        # if the robber stop return true.
        if len(self.placed_array) < 1:
            return False
        if self.placed_count == 0:
            # if there the position is same to the position the robber placed last , the robber stop.
            if environment.distance(position, self.placed_array[-1]) < constant.robber_radius:
                return True
        return False

    def save_placed_list(self, position):
        if self.placed_count == 1:
            self.placed_array.append(position)
        self.placed_count += 1
        if self.placed_count > self.robber_save_place_interval:
            self.placed_count = 0
        if len(self.placed_array) > self.robber_max_save_place:
            del self.placed_array[0]


class RobberFleeComp:
    # decide how robber move by state.
    # if there are cop close to the robber , flee from it.

    def __init__(self):
        self.environment = make_environment.make_environment()
        self.state_array = []
        # for rob in robbers_array:
        #     self.state_array.append(StateRobber(rob.id))
        self.distance_escape_from_cop = self.environment.max_distance() / 4  # the distance from the cop , the robber start to flee from it.
        self.distance_escape_from_wall = 50  # the distance from the wall the robber start to flee from it.
        self.max_count_escape_wall = 20  # how long the robber flee from the wall.
        self.distance_emergency_cops = 70  # the distance from the cop to become the emergency.
        self.max_count_stop = 50  # how long continue when the stop happen.
        self.max_count_emergency = 10  # how long continue when the emergency happen.
        self.max_speed = constant.robber_max_speed
        self.max_turn = self.max_speed * constant.ratio_speed_direction

    @staticmethod
    def move_randomly():
        # move randomly.
        move = random.random()
        di = 1.0 - move
        if random.randint(1, 2) == 1:
            di = di * -1
        return move, di

    def move_free_square_normal(self, rob_state, state_robber):
        # the robber move free.but he avoid to go to the wall or corner.
        # rob_state is id, position, direction
        if state_robber.get_state_free():
            # move randomly now.if the wall is close , change the direction to opposite to now.
            direction = rob_state[2]
            if rob_state[1][0] < self.distance_escape_from_wall:
                # close to left wall
                if 90 <= direction < 180:
                    state_robber.set_aim_direction(direction - 90.0)
                elif 180 <= direction < 270:
                    state_robber.set_aim_direction(direction + 90.0)
                state_robber.set_state_escape_from_wall()
                state_robber.add_state_count()
            elif rob_state[1][0] + self.distance_escape_from_wall > self.environment.screen_size_x:
                # close to right wall
                if direction < 180:
                    state_robber.set_aim_direction(direction + 90)
                else:
                    state_robber.set_aim_direction(direction - 90)
                state_robber.set_state_escape_from_wall()
            elif rob_state[1][1] + self.distance_escape_from_wall > self.environment.screen_size_y:
                # close to above wall
                if direction < 90:  # start at closing to the wall
                    state_robber.set_aim_direction(direction - 90 + 360)
                elif 90 <= direction < 180:
                    state_robber.set_aim_direction(direction + 90)
                state_robber.set_state_escape_from_wall()
            elif rob_state[1][1] < self.distance_escape_from_wall:
                # close to below wall
                if 270 > direction > 90:
                    state_robber.set_aim_direction(direction - 90)
                elif direction >= 270:
                    state_robber.set_aim_direction(direction + 90 - 360)
                state_robber.set_state_escape_from_wall()
            else:
                # there is much distance to the wall.move randomly
                return self.move_randomly()
        elif state_robber.get_state_escape_from_wall():
            # the robber try to avoid the wall.
            action = calc_action.move_to_aim_direction(rob_state[2], state_robber.aim_direction, self.max_speed)
            state_robber.add_state_count()
            if state_robber.get_end_state(self.max_count_escape_wall):
                # it is end of avoiding from the wall.
                state_robber.set_state_free()
                state_robber.set_aim_direction(0)
            return action
        else:
            print("error; no state in move_free_square_normal function in robber_flee_comp file")
            state_robber.print_state()
            return 0, 0
        return calc_action.move_to_aim_direction(rob_state[2], state_robber.aim_direction, self.max_speed)

    def decide_next_action_robber(self, cops_state_array, robbers_state_array):
        if not self.state_array:
            # if it is the first time, make robber_state_array
            for rob in robbers_state_array:
                self.state_array.append(StateRobber(rob[0]))

        robbers_action_array = []
        for rob in robbers_state_array:
            # find this rob state
            state_robber = 0
            for st in self.state_array:
                if st.id == rob[0]:
                    state_robber = st
                    break
            if state_robber == 0:
                print("error: no state in RobberFleeComp")
                return []
            # make near cops array
            near_cops_array = calc_action.near_cops_array(rob[1], cops_state_array, self.distance_escape_from_cop, self.environment)
            if len(near_cops_array) < 1:
                # there is no cop close to the robber, move free.
                # if the before state is not move_free, change to move_free state.
                if not state_robber.get_state_move_free():
                    state_robber.set_state_free()
                    state_robber.set_placed_list_empty()
                if self.environment.environment_type() == 'square':
                    action = self.move_free_square_normal(rob, state_robber)
                elif self.environment.environment_type() == 'circle':
                    action = self.move_free_square_normal(rob, state_robber)
                elif self.environment.environment_type() == 'torus':
                    action = self.move_free_square_normal(rob, state_robber)
                else:
                    print("error: no environment in flee_simply function in robber_flee_comp file")
            else:
                # there are some cop close to the robber.
                list_emergency_cops = calc_action.near_cops_array(rob[1], near_cops_array, self.distance_emergency_cops, self.environment)
                if len(list_emergency_cops) < 1:
                    # put on the weight to the cops and wall.move to the direction where is a few cops and wall
                    if state_robber.get_state_move_free():
                        # until now the robber move freely.
                        state_robber.set_aim_direction(
                            for_robber_comp.direction(rob, state_robber.get_placed_list(), near_cops_array, self.environment))
                        state_robber.set_state_flee()
                        state_robber.set_placed_list_empty()
                    elif state_robber.get_state_flee() or state_robber.get_state_emergency():
                        # the robber flee from the cops until now.if the robber stop, change the state to stop
                        state_robber.set_aim_direction(
                            for_robber_comp.direction(rob, state_robber.get_placed_list(), near_cops_array, self.environment))
                        if state_robber.check_stop(rob[1], self.environment):
                            state_robber.set_state_stop()
                            state_robber.set_aim_direction(
                                for_robber_comp.direction_stop(rob, near_cops_array, self.environment))
                        state_robber.save_placed_list(rob[1])
                    elif state_robber.get_state_stop():
                        state_robber.save_placed_list(rob[1])
                        state_robber.add_state_count()
                        if state_robber.get_end_state(self.max_count_stop):
                            state_robber.set_state_flee()
                    else:
                        print('error: robber state' + str(state_robber.state))
                else:
                    # the state is emergency. there are some cops very closet to the robber.
                    if state_robber.get_state_emergency():
                        # before state is emergency.
                        state_robber.set_aim_direction(
                            for_robber_comp.direction_emergency(rob, list_emergency_cops, self.environment))
                        state_robber.add_state_count()
                        if state_robber.get_end_state(self.max_count_emergency):
                            state_robber.set_state_flee()
                            state_robber.set_placed_list_empty()
                    else:
                        # before state is not stop.
                        state_robber.set_state_emergency()
                        state_robber.set_aim_direction(
                            for_robber_comp.direction_emergency(rob, list_emergency_cops, self.environment))
                        state_robber.add_state_count()
                action = calc_action.move_to_aim_direction(rob[2], state_robber.aim_direction, self.max_turn)

            robbers_action_array.append((rob[0], action))
        return robbers_action_array
