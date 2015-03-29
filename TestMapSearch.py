import Game
import GameMapExamples
import Search
def mapSearchTest():
    game = GameMapExamples.GameMapExamples.example2()
    #print game
    path = Search.search(game)
    return path

print mapSearchTest()