#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam
from .our_player import BorderPlayer, OurPlayer

# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def factory():
    player1 = OurPlayer('Bonnie')
    player2 = OurPlayer('Clyde')
    team = SimpleTeam("Bonnie and Clyde", player1, player2)
    player1.partner = player2
    player2.partner = player1
    return team

# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ ./pelitagame path_to/groupN/:alternate_factory

