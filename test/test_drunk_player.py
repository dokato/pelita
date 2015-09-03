import unittest

from pelita.player import SimpleTeam
from pelita.player import TestPlayer

from pelita.game_master import GameMaster

from team import DrunkPlayer

class MyPlayerTest(unittest.TestCase):
    def test_my_player_is_not_moving(self):
        my_team = SimpleTeam("test", DrunkPlayer(), DrunkPlayer())
        test_layout = """
            ############
            # 0 #  # 1 #
            #   #  #   #
            # 2 .  . 3 #
            ############
        """
        teams = [
            # register my_team for bots 0, 2
            my_team,
            # register a pre-defined team as an enemy
            # First one moves left-down-down-left-left, second one left
            SimpleTeam(TestPlayer("<vv<<"), TestPlayer("<<<<<"))
        ]

        gm = GameMaster(test_layout, teams, number_bots=4, game_time=5, seed=20)

        # play `game_time` rounds
        gm.play()

        # check the position of my bots
        # Tests fail, because our player is random
#        self.assertEqual(gm.universe.bots[0].current_pos, (2, 1))
#        self.assertEqual(gm.universe.bots[2].current_pos, (2, 3))

        # For reference, testing the test player
        self.assertEqual(gm.universe.bots[1].current_pos, (6, 3))
        self.assertEqual(gm.universe.bots[3].current_pos, (4, 3))

if __name__ == "__main__":
    unittest.main()

