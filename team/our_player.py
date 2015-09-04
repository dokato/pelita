# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from .utils import utility_function

class BorderPlayer(AbstractPlayer):
    """ A player that makes moves at random. """

#    def __init__(self):
#        self.adjacency = AdjacencyList(self.current_uni.free_positions())

    def get_move(self):
        #pdb.set_trace()
        self.adjacency = AdjacencyList(self.current_uni.free_positions())
        try:
            border_path =  self.adjacency.bfs(self.current_pos, self.team_border)
        except NoPathException:
            return stop
        if len(border_path)==0:
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

