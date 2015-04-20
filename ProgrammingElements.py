import hashlib
import Game

class Element(object):
    def transform(self, game_map):
        raise Exception("Must Implement Method")

class Operation(object):
    def __init__(self, operation):
        self.operation = operation

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.operation == other.operation
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def transform(self, game_map):
        raise NotImplementedError


class CommandOperation(Operation):
    def __init__(self, operation):
        if not isinstance(operation, basestring):
            raise Exception("Sub operations must be primitive strings")
        self.operation = operation

    def __str__(self):
        return str(self.operation)

    @staticmethod
    def command_array_from_path_string_array(path):
        return [CommandOperation(p) for p in path]

    def transform(self, game_map):
        transform_function = Game.GameMap.tranform_function_from_transformation(self)
        return transform_function(game_map)

class Program(object):
    def __init__(self, operations):
        self.operations = []
        for operation in operations:
            self.add_operation(operation)

    def add_operation(self, operation):
        if isinstance(operation, Function):
            operation = FunctionCallOperation(FunctionCall(operation, 1))
        if not isinstance(operation, Operation):
            raise Exception("Must add Operation")
        elif isinstance(operation, CommandOperation):
            self.operations.append(operation)
        elif isinstance(operation, FunctionCallOperation):
            if len(self.operations) > 0:
                last_operation = self.operations[-1]
                if isinstance(operation, FunctionCallOperation) and isinstance(last_operation, FunctionCallOperation) and str(last_operation.function_call.function) == str(operation.function_call.function):
                    last_operation.increase_call_count()
                else:
                    self.operations.append(operation)
            else:
                self.operations.append(operation)
        else:
            raise Exception("Unsupported Class")

    def __str__(self):
        out = ""
        out += "main method: \n"
        out += str(self.operations)
        functions = {operation.function_call.function for operation in self.operations if isinstance(operation, FunctionCallOperation)}
        out += "\nFunctions: \n"
        for function in functions:
            out += function.get_unique_id() + " : "
            out += str(function)
        return out

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.operations)

    def __getitem__(self, i):
        return self.operations[i]

    def cost(self):
        cost_sum = 0
        counted_functions = set()
        for operation in self.operations:
            if isinstance(operation, CommandOperation):
                cost_sum += 1
            elif isinstance(operation, FunctionCallOperation):
                cost_sum += 1
                if str(operation) not in counted_functions:
                    cost_sum += operation.num_sub_operations()
                    cost_sum += 0.01 * operation.function_call.num_calls
                    counted_functions.add(str(operation))
        return cost_sum

    def run_program_on_game(self, game):
        game_map = game
        for operation in self.operations:
            game_map = operation.transform(game_map)
            if game_map.check_if_solved():
                return True
        return False

class Function(object):
    def __init__(self, operations):
        self.operations = operations

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.operations) == len(other.operations):
                for (op1, op2) in zip(self.operations, other.operations):
                    if op1 is not op2:
                        return False
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def num_sub_operations(self):
        return len(self.operations)

    def __str__(self):
        return str(self.operations)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.operations)

    def get_unique_id(self):
        hash_object = hashlib.md5(str(self.operations))
        unique_id = "F_" + hash_object.hexdigest()[0:4]
        return unique_id

    def transform(self, game_map):
        for operation in self.operations:
            game_map = operation.transform(game_map)
        return game_map

    def __hash__(self):
        return hash(str(self))


class FunctionCall(object):
    def __init__(self, function, num_calls):
        self.function = function
        self.num_calls = num_calls

class FunctionCallOperation(Operation):
    def __init__(self, function_call):
        super(FunctionCallOperation, self).__init__(function_call)
        self.function_call = function_call

    def __str__(self):
        unique_id = self.function_call.function.get_unique_id()
        out = "(" + str(unique_id) + ", #" + str(self.function_call.num_calls) + ")"
        return out

    def num_sub_operations(self):
        return self.function_call.function.num_sub_operations()

    def increase_call_count(self):
        self.operation.num_calls += 1

    def transform(self, game_map):
        for i in range(0, self.function_call.num_calls):
            game_map = self.function_call.function.transform(game_map)
        return game_map
