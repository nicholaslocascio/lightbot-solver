""" """
import ProgramCompression
import ProgrammingElements
import GameMapExamples
import Search

def test_program_compression():
    path = ['f', 'l', 'f', 'r', 'a', 'f', 'l', 'f', 'r', 'a', 'f', 'l', 'f', 'a']
    operations = ProgrammingElements.CommandOperation.command_array_from_path_string_array(path)
    full_program = ProgrammingElements.Program(operations)
    program = ProgramCompression.compress_program(full_program)
    print "Program is: "
    print program
    print "Program costs: "
    print program.cost()

def test_game_map_solving_and_compression():
    game = GameMapExamples.GameMapExamples.example2()
    path = Search.search(game)
    full_program = ProgrammingElements.Program(path)
    program = ProgramCompression.compress_program(path)
    print "Program is: "
    print program
    print "Program costs: "
    print program.cost()
    result = program.run_program_on_game(game)
    print "Running program on Map: \n Result: " + str(result)

def test_game_map_compression_with_search():
    game = GameMapExamples.GameMapExamples.example3()
    path = Search.search(game)
    full_program = ProgrammingElements.Program(path)
    program = ProgramCompression.get_best_program_with_search(game, full_program)
    print "Program is: "
    print program
    print "Program costs: "
    print program.cost()
    result = program.run_program_on_game(game)
    print "Running program on Map: \n Result: " + str(result)


#test_game_map_solving_and_compression()
test_game_map_compression_with_search()
