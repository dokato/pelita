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


    def go_for_boarder(self):
        border_path =  self.find_path(self.team_border)
        self.say("Border!!!!")
        if len(border_path)==0:
            return stop
        if border_path==None:
            return stop
        return diff_pos(self.current_pos, border_path.pop())
    
    def go_for_food(self):
        food_path =  self.find_path(self.enemy_food)
        self.say("Omnomnom!!!!")
        print('went for food')
        if food_path==None:
            return stop
        if len(food_path)==0:
            return stop
        return diff_pos(self.current_pos, food_path.pop())

    def safe_move(self, next_move):
        dangerous_enemies = [bot for bot in self.enemy_bots if bot.is_destroyer]
        print ('got dangerous enemies')
        valid_moves = self.legal_moves.values()
        enemy_valid_moves_values = [bot.legal_moves.values() for bot in dangerous_enemies]
        enemy_valid_moves_values = [item for sublist in enemy_valid_moves_values for item in    sublist]
        if [sum(x) for x in zip(next_move,self.current_pos)] in enemy_valid_moves_values:
            valid_moves = [i for i in valid_moves if i not in enemy_valid_moves_values]
            return self.rnd.choice(valid_moves)
        else:
            return(next_move) 
        #check that next_move isn't in enemy_valid_moves.values() (don't forget to either flatten or sth)
        for de in dangerous_enemies:
            print(self.current_pos, dd)
            #list comp to filter valid_moves based on the valid moves of the enemy
            #pick a random move from valid_moves
            if (manhattan_dist(self.current_pos, dd) <= 2):
                valid_moves = [i for i in valid_moves if i != next_move and i != (0,0)]
                print ('too close')
                return self.rnd.choice(valid_moves)
            else:
                return next_move

    def get_move(self):
        if self.round_index is None:
            self.round_index = 0
        else:
            self.round_index += 1
        self.read_score()
        #possible_moves = list(self.legal_moves.keys())
        if self.me.is_destroyer:
            #m1 = self.go_for_boarder()
            #if m1 != stop:
            #    return m1
            #else:
            return self.go_for_food()
        else:
            next_move = self.go_for_food()
            return self.safe_move(next_move, dangerous_enemy_pos)
            
            
            return next_move

