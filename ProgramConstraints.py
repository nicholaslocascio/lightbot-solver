
class ProgramConstraints(object):
    """docstring for ProgramConstraints"""
    def __init__(self, function_constraints, main_length=float('inf')):
        self.main_length_limit = main_length
        self.function_constraints = function_constraints
        self.num_functions = len(function_constraints)

    def program_fits_constraint(self, program):
        if program.length_of_main() > self.main_length_limit:
            return False
        if self.num_functions >= len(program.functions):
            return False

        return FunctionConstraint.do_functions_fit_constraints(program.functions, self.function_constraints)

class FunctionConstraint(object):
    def __init__(self, length_of_function):
        self.length_of_function = length_of_function

    def does_fit(self, function):
        if len(function) <= self.length_of_function:
            return True
        return False

    @staticmethod
    def do_functions_fit_constraints(functions, constraints):
        for function, constraint in zip(functions, constraints):
            if not constraint.does_fit(function):
                return False
        return True
