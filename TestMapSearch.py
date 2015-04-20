import GameMapExamples
import Search
from ProgrammingElements import Function, CommandOperation

def mapSearchTest():
    game = GameMapExamples.GameMapExamples.example2()
    path = Search.search(game)
    return path

def mapSearchTestWithFunction():
    ps = ['f', 'l', 'f', 'r', 'a']
    operations = CommandOperation.command_array_from_path_string_array(ps)
    function = Function(operations)
    game = GameMapExamples.GameMapExamples.example2()
    path = Search.search(game, function)
    return path

print mapSearchTestWithFunction()