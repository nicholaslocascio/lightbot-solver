""" Performs Programming Synthesis and Compression """

from ProgrammingElements import Function, Program, CommandOperation, FunctionCallOperation, FunctionCall
import Search
import itertools
from ProgramConstraints import FunctionConstraint

def get_all_programs_compressions(full_program):
    path = full_program
    programs = []
    functions = get_top_potential_functions(full_program)
    for function in functions:
        for start in range(0, len(path)-1):
            new_program = make_program_from_full_program_and_function(path, function)
            programs.append(new_program)
    return programs

def get_all_potential_functions(full_program):
    path = full_program
    functions = set()
    function_set = set()
    for window_size in range(2, len(path)/2):
        for start in range(0, len(path)-window_size):
            end = start + window_size
            commands = path[start:end]
            function = Function(commands)
            if str(function) not in function_set:
                function_set.add(str(function))
                functions.add(function)
    return list(functions)

def get_top_potential_functions(full_program):
    all_functions = get_all_potential_functions(full_program)
    best_functions = {}
    best_functions_count = {}
    for function in all_functions:
        length = len(function)
        best = best_functions_count.get(length, -1)
        count = get_num_times_function_appears_in_full_program(function, full_program)
        if count > best:
            best_functions_count[length] = count
            best_functions[length] = [function]
        elif count == best:
            b = best_functions.get(length)
            if b is None:
                b = []
            b.append(function)
            best_functions[length] = b
    all_best_functions = []
    for key, value in best_functions.iteritems():
        print key, value
        all_best_functions = all_best_functions + value
    return all_best_functions

def get_functions_fitting_constraints(functions, program_constraints):
    num_funcs = program_constraints.num_functions
    all_perms = itertools.permutations(functions, num_funcs)
    fitting_function_pairs = \
    [function_tuple for function_tuple in all_perms \
    if FunctionConstraint.do_functions_fit_constraints( \
        function_tuple, program_constraints.function_constraints)]
    return fitting_function_pairs

def get_num_times_function_appears_in_full_program(function, full_program):
    count = 0
    window_size = len(function)
    for start in range(0, len(full_program)-window_size):
        end = start + window_size
        commands = full_program[start:end]
        f = Function(commands)
        if str(f) == str(function):
            count += 1
    return count


def get_all_programs_with_function_base(game_map, functions):
    programs = []
    for function in functions:
        function_call_operation = FunctionCallOperation(FunctionCall(function, 1))
        path = Search.search(game_map, [function_call_operation])
        program = Program(path)
        programs.append(program)
    return programs

def get_best_program_with_function_tuples_base(game_map, function_tuples, main_limit=float('inf')):
    best_cost = float('inf')
    best_program = None
    for function_tuple in function_tuples:
        function_tuple_operations = []
        for function in function_tuple:
            function_call_operation = FunctionCallOperation(FunctionCall(function, 1))
            function_tuple_operations.append(function_call_operation)
        print "best_cost", best_cost
        program = Search.search(game_map, function_tuple_operations, best_cost, main_limit)
        if program:
            program_cost = program.cost()
            if program_cost < best_cost:
                best_program = program
                best_cost = program_cost
    return best_program

def get_best_program_with_search(game_map, full_program):
    functions = get_top_potential_functions(full_program)
    functions = [[function] for function in functions]
    best = get_best_program_with_function_tuples_base(game_map, functions)
    return best

def get_best_program_with_search_and_constraints(game_map, full_program, program_constraints):
    functions = get_top_potential_functions(full_program)
    function_tuples = get_functions_fitting_constraints(functions, program_constraints)
    best = get_best_program_with_function_tuples_base(game_map, function_tuples, program_constraints.main_length_limit)
    return best

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
    best = min(programs, key=lambda program: program.cost())
    return best

