# -*- coding: utf-8 -*-
# (Specifying utf-8 is always a good idea in Python 2.)
import pdb
from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from .utils import utility_function

from pelita.graph import AdjacencyList, diff_pos, NoPathException, manhattan_dist
import numpy as np


class BorderPlayer(AbstractPlayer):
    """ A player that makes moves at random. """

    def find_path(self, thingslist):
        """ finds the path to the nearest object
        *thingslist* - list of tuples with objects positions
        """
        self.adjacency = AdjacencyList(self.current_uni.free_positions())
        try:
            pathd =  self.adjacency.bfs(self.current_pos, thingslist)
        except NoPathException:
            return None
        return pathd

    def read_score(self):
        self.score_history[0, self.round_index] = self.current_uni.teams[0].score
        self.score_history[1, self.round_index] = self.current_uni.teams[1].score

    def get_move(self):
        border_path =  self.find_path(self.team_border)
        self.say("Border!!!!")
        if len(border_path)==0:
            return stop
        if border_path==None:
            return stop
        return diff_pos(self.current_pos, border_path.pop())


class OurPlayer(AbstractPlayer):

    def set_initial(self):
        self.current_strategy = 0
        self.round_index = None
        self.score_history = np.zeros([2, 300])
        self.tracking_idx = None
        self.path = []
        self.food_strategy = True
        self.chase_mode = False

    def find_path(self, thingslist):
        """ finds the path to the nearest object
        *thingslist* - list of tuples with objects positions
        """
        self.adjacency = AdjacencyList(self.current_uni.free_positions())
        try:
            pathd =  self.adjacency.bfs(self.current_pos, thingslist)
        except NoPathException:
            return None
        return pathd

    def read_score(self):
        self.score_history[0, self.round_index] = self.current_uni.teams[0].score
        self.score_history[1, self.round_index] = self.current_uni.teams[1].score

    @property
    def tracking_target(self):
        """ Bot object we are currently tracking. """
        return self.current_uni.bots[self.tracking_idx]

    @property
    def path_to_target(self):
        """ Path to the target we are currently tracking. """
        self.adjacency = AdjacencyList(self.current_uni.free_positions())
        try:
            return self.adjacency.a_star(self.current_pos,
                    self.tracking_target.current_pos)
        except NoPathException:
            return None

    def start_chase(self):
        self.say("Chase him!")
        self.chase_mode = True
        if self.partner:
            self.partner.chase_mode = True
    
    def stop_chase(self):
        self.say("Stopit!")
        self.chase_mode = False
        if self.partner:
            self.partner.chase_mode = False
    
    def go_for_boarder(self):
        border_path =  self.find_path(self.team_border)
        #self.say("Border!!!!")
        if len(border_path)==0:
            return stop
        if border_path==None:
            return stop
        return diff_pos(self.current_pos, border_path.pop())
    
    def go_for_food(self):
        food_path =  self.find_path(self.enemy_food)
        #self.say("Omnomnom!!!!")
        if food_path==None:
            return stop
        if len(food_path)==0:
            return stop
        return diff_pos(self.current_pos, food_path.pop())

    def random_move(self):
        #self.say("Let's the fight begin!")
        legal_moves = self.legal_moves
        # Remove stop
        try:
            del legal_moves[stop]
        except KeyError:
            pass
        # now remove the move that would lead to the previous_position
        # unless there is no where else to go.
        if len(legal_moves) > 1:
            for (k,v) in legal_moves.items():
                if v == self.previous_pos:
                    break
            del legal_moves[k]
        # just in case, there is really no way to go to:
        if not legal_moves:
            return stop
        # and select a move at random
        return self.rnd.choice(list(legal_moves.keys()))

    def attack_move(self):
        self.adjacency = AdjacencyList(self.current_uni.free_positions())
        attackpath = []
        if self.tracking_idx is not None:
            # if the enemy is no longer in our zone
            if not self.team.in_zone(self.tracking_target.current_pos):
                self.tracking_idx = None
                return  self.go_for_food()
            # otherwise update the path to the target
            else:
                attackpath = self.path_to_target
        if self.tracking_idx is None:
            # check the enemy positions
            possible_targets = [enemy for enemy in self.enemy_bots
                    if self.team.in_zone(enemy.current_pos)]
            if possible_targets:
                # get the path to the closest one
                try:
                    possible_paths = [(enemy, self.adjacency.a_star(self.current_pos, enemy.current_pos))
                                      for enemy in possible_targets]
                except NoPathException:
                    return None
            else:
                return self.go_for_food()

            if possible_paths:
                closest_enemy, path = min(possible_paths,
                                          key=lambda enemy_path: len(enemy_path[1]))
                self.tracking_idx = closest_enemy.index
        if len(attackpath)==0:
            return self.random_move()
        return diff_pos(self.current_pos, attackpath.pop())

    def get_move(self):
        if self.round_index == 2 and self.me.index == 0:        #find some more clever conditions
            self.start_chase()
        if self.round_index == 5 and self.me.index == 2:        #find some more clever conditions
            self.stop_chase()
        if self.chase_mode:
            self.say("Chase!!")
        if self.round_index is None:
            self.round_index = 0
        else:
            self.round_index += 1
        self.read_score()
        if self.round_index < 14 and self.me.index == 0:
            return self.random_move()
        
        #if self.me.is_destroyer:
        #    return self.attack_move()
        if self.me.is_destroyer:
            if self.food_strategy:
                m1 = self.go_for_boarder()
                if m1 != stop:
                    return m1
                else:
                    return self.go_for_food()
        else:
            return self.go_for_food()
            #dangerous_enemy_pos = [bot.current_pos
            #    for bot in self.enemy_bots if bot.is_destroyer]
            #next_move = self.go_for_food()
            #for dd in dangerous_enemy_pos:
            #    if (manhattan_dist(self.current_pos, dd) <= 2):
            #        return tuple((-1)*x for x in next_move)
            #return next_move
