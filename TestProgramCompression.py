""" """
from ProgramCompression import compress_program
from ProgrammingElements import Function, Program, CommandOperation, FunctionCallOperation, FunctionCall
import GameMapExamples
import Search

def test_program_compression():
    path = ['f', 'l', 'f', 'r', 'a', 'f', 'l', 'f', 'r', 'a', 'f', 'l', 'f', 'a']
    operations = CommandOperation.command_array_from_path_string_array(path)
    full_program = Program(operations)
    program = compress_program(full_program)
    print "Program is: "
    print program
    print "Program costs: "
    print program.cost()

def test_game_map_solving_and_compression():
    game = GameMapExamples.GameMapExamples.example1()
    path = Search.search(game)
    operations = CommandOperation.command_array_from_path_string_array(path)
    full_program = Program(operations)
    program = compress_program(operations)
    print "Program is: "
    print program
    print "Program costs: "
    print program.cost()
    result = program.run_program_on_game(game)
    print "Running program on Map: \n Result: " + str(result)

#test_program_compression()
test_game_map_solving_and_compression()
