# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from .utils import utility_function

class OurPlayer(AbstractPlayer):

    def get_move(self):

        self.check_pause()
        possible_moves = list(self.legal_moves.keys())
        return self.rnd.choice(possible_moves)

