# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import stop

# use relative imports for things inside your module
from .utils import utility_function

class DrunkPlayer(AbstractPlayer):
    """ Basically a clone of the RandomPlayer. """

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        print(self.current_uni.pretty)

    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            self.say("What a headache!")
            return stop

    def get_move(self):
        utility_function()

        self.check_pause()

        # legal_moves returns a dict {move: position}
        # we always need to return a move
        possible_moves = list(self.legal_moves.keys())
        # selecting one of the moves
        return self.rnd.choice(possible_moves)

