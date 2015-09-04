# -*- coding: utf-8 -*-
# (Specifying utf-8 is always a good idea in Python 2.)
import pdb
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

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0
    
    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts = ["Dominik!", "Kwangjun", "Python School Munich"]
            self.say(self.rnd.choice(texts))
            return stop
    
    def get_move(self):

        self.check_pause()
        possible_moves = list(self.legal_moves.keys())
        return self.rnd.choice(possible_moves)

