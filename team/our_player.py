# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)
from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from .utils import utility_function
from pelita.graph import AdjacencyList, diff_pos

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

    def get_move(self):
        #pdb.set_trace()
        border_path =  self.find_path(self.team_border)
        self.say("Border!!!!")
        if len(border_path)==0:
            return stop
        if border_path==None:
            return stop
        return diff_pos(self.current_pos, border_path.pop())

class OurPlayer(AbstractPlayer):

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.texts = ["Dominik!", "Kwangjun", "Python School Munich"]
    
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
        if len(food_path)==0:
            return stop
        if food_path==None:
            return stop
        return diff_pos(self.current_pos, food_path.pop())

    def get_move(self):
        #possible_moves = list(self.legal_moves.keys())
        if self.me.is_destroyer:
            m1 = self.go_for_boarder()
            if m1 != stop:
                return m1
            else:
                return self.go_for_food()
        else:
            return self.go_for_food()

