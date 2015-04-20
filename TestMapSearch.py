import Game
import GameMapExamples
import Search
def mapSearchTest():
    game = GameMapExamples.GameMapExamples.example1()
    path = Search.search(game)
    return path

print mapSearchTest()