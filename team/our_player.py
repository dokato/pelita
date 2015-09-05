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
        self.border_mode = True
        self.chase_count = 0

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
        #self.say("Chase him!")
        self.chase_mode = True
        self.chase_count += 1
        if self.partner:
            self.partner.chase_mode = True
            self.partner.chase_count += 1
    
    def stop_chase(self):
        #self.say("Stopit!")
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


    def safe_move(self, next_move):
        
        dangerous_enemies = [enemy for enemy in self.enemy_bots if enemy.is_destroyer]
        valid_pos = self.legal_moves.values()
        enemy_valid_pos_values = [self.current_uni.legal_moves(enemy.current_pos).values() for enemy in dangerous_enemies]
        enemy_valid_pos_values = [item for sublist in enemy_valid_pos_values for item in    sublist]
        next_pos = tuple([sum(x) for x in zip(next_move,self.current_pos)])
        if next_pos in enemy_valid_pos_values:
            valid_pos = [i for i in valid_pos if i not in enemy_valid_pos_values]
            if len(valid_pos) > 0:
                next_pos = self.rnd.choice(valid_pos)
                next_move = tuple([x[0] - x[1] for x in zip(next_pos,self.current_pos)])
                return(next_move)
            else:
                return(stop)
        else:
            return(next_move) 
        

    def random_move(self):
        #self.say("Let the fight begin!")

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
                return None
            if possible_paths:
                closest_enemy, path = min(possible_paths,
                                          key=lambda enemy_path: len(enemy_path[1]))
                self.tracking_idx = closest_enemy.index
        if len(attackpath)==0:
            return self.random_move()
        return diff_pos(self.current_pos, attackpath.pop())
    
    def get_distance_to_me(self, pos):
        return manhattan_dist(self.current_pos, pos)
    
    def get_closest_eatable_enemy_pos(self):
        enemies = [(enemy.current_pos, self.get_distance_to_me(enemy.current_pos)) for enemy in self.enemy_bots if enemy.is_harvester]
        
        if len(enemies) != 0:
            enemies = sorted(enemies, key=lambda x: x[1])
            return enemies[0]
        return None
        

    def get_move(self):
        self.say("Bot" + str(self.me.index))
#        if self.round_index == 2 and self.me.index == 0:        #find some more clever conditions
#            self.start_chase()
#        if self.round_index == 5 and self.me.index == 2:        #find some more clever conditions
#            self.stop_chase()
#        if self.chase_mode:
#            self.say("Chase!!")
        if self.round_index is None:
            self.round_index = 0
        else:
            self.round_index += 1
        self.read_score()
        if self.round_index < 14 and self.me.index == 0:
            next_move = self.random_move()


        #switch both players to chase mode, if both are close but on two sides
        en = self.get_closest_eatable_enemy_pos()
        if en:
            other_bot = [x for x in self.team_bots if x != self.me][0]
            dist_enemy_to_other_bot = manhattan_dist(other_bot.current_pos, en[0])

            if (en[1] <= 5) and (dist_enemy_to_other_bot <= 5) and (self.get_distance_to_me(other_bot.current_pos) > en[1]):
                self.start_chase()
                if self.chase_count > 5:
                    self.stop_chase()
            else:
                self.stop_chase()

            if self.chase_mode:
                self.say("Chasemode")
                return self.safe_move(self.attack_move())
            
        if self.me.is_destroyer:
            #am = self.attack_move()
            #if am:
            #    next_move = am
            if self.food_strategy:
                if self.border_mode:
                    m1 = self.go_for_boarder()
                    if m1 != stop:
                        self.say("Boarder")
                        next_move = m1
                    else:
                        self.say("Food")
                        next_move = self.go_for_food()
                else:
                    self.say("Food")
                    self.border_mode = False
                    next_move = self.go_for_food()
        else:
            next_move = self.go_for_food()
        
        return self.safe_move(next_move)
