#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam
from .our_player import OurPlayer, BorderPlayer
from .trys import DominikPlayer

# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def factory():
    return SimpleTeam("group3", DominikPlayer(), OurPlayer())
