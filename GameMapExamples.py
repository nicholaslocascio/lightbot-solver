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


    @staticmethod
    def example3():
        topography = \
"""\
11111
----1
----1
----1
11111\
"""
        features = \
"""\
lxlxl
----x
----l
----x
xxlxl\
"""
        robot_features = \
"""\
xxxxx
----x
----x
----x
Exxxx\
"""

        return Game.GameMap.game_map_from_strings(topography, features, robot_features)

    @staticmethod
    def example4():
        topography = \
"""\
1111
---1
---1
-111\
"""
        features = \
"""\
xlxl
---x
---l
-xll\
"""
        robot_features = \
"""\
Exxx
xxxx
xxxx
xxxx\
"""

        return Game.GameMap.game_map_from_strings(topography, features, robot_features)