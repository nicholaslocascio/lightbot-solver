import Game

class GameMapExamples(object):
    @staticmethod
    def example1():
        topography = \
"""\
-1-
-1-
-1-
-1-\
"""
        features = \
"""\
-l-
-l-
-l-
-l-\
"""
        robot_features = \
"""\
-S-
-x-
-x-
-x-\
"""
        return Game.GameMap.game_map_from_strings(topography, features, robot_features)

    @staticmethod
    def example2():
        topography = \
"""\
-1----
-11---
--11--
---11-\
"""
        features = \
"""\
-x----
-xl---
--xl--
---xl-\
"""
        robot_features = \
"""\
-S----
-xx---
--xx--
---xx-\
"""

        return Game.GameMap.game_map_from_strings(topography, features, robot_features)