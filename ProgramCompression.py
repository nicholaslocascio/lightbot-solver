""" Performs Programming Synthesis and Compression """

from ProgrammingElements import Function, Program, CommandOperation, FunctionCallOperation, FunctionCall
import pprint
pp = pprint.PrettyPrinter(depth=6)

def get_all_programs_compressions(full_program):
    path = full_program
    programs = []
    for window_size in range(2, len(path)-1):
        for start in range(0, len(path)-window_size):
            end = start + window_size
            commands = path[start:end]
            function = Function(commands)
            new_program = make_program_from_full_program_and_function(path, function)
            programs.append(new_program)
    return programs


def make_program_from_full_program_and_function(full_program, function):
    """ """
    path = full_program
    program = Program([])
    window_size = function.num_sub_operations()
    start = 0
    while start < len(path):
        command = path[start]
        end = start + window_size
        if end < len(path):
            commands = path[start:end]
            sub_function = Function(commands)
            if str(function) == str(sub_function):
                function_call_operation = FunctionCallOperation(FunctionCall(function, 1))
                program.add_operation(function_call_operation)
                start += window_size
            else:
                program.add_operation(command)
                start += 1
        else:
            program.add_operation(command)
            start += 1
    return program


def compress_program(full_program):
    programs = get_all_programs_compressions(full_program)
    print len(programs)
    best = min(programs, key=lambda program: program.cost())
    return best



