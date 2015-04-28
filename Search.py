import ProgrammingElements
import Queue as Q

class GameMapSearchNode(object):
    """docstring for GameMapSearchNode"""
    def __init__(self, game_map, program):
        super(GameMapSearchNode, self).__init__()
        self.game_map = game_map
        self.program = program

    def get_tranformation_path(self):
        return self.program

def cost_from_node(node):
    return node.program.cost()

def heuristic_from_node(node):
    return node.game_map.get_heuristic_cost()*1e-3

def heuristic_plus_cost_from_node(node):
    return cost_from_node(node)+heuristic_from_node(node)

def search(game_map, additional_functions=None, cost_limit=float('inf'), main_limit=float('inf')):
    start_node = GameMapSearchNode(game_map, ProgrammingElements.Program([]))
    agenda = Q.PriorityQueue()
    agenda.put((heuristic_plus_cost_from_node(start_node), start_node))
    seen = set()
    depth = 0
    while agenda and not agenda.empty():
        depth += 1
        if depth > 4000:
            raise Exception('Search depth limit reached')
        cost, node = agenda.get()
        if node.program.length_of_main() > main_limit:
            continue
        if node.program.cost() > cost_limit:
            return None
        program = node.program
        game_map = node.game_map
        game_map_str = game_map.__str__()
        seen.add(game_map_str)
        if game_map.check_if_solved():
            print "Nodes expanded:" +  str(depth)
            print cost
            print program
            return node.program
        neighbor_maps, operations = game_map.get_neighbor_maps_and_operations(additional_functions)
        for neighbor_map, operation in zip(neighbor_maps, operations):
            new_program = ProgrammingElements.Program(program.operations + [operation])
            neighbor_node = GameMapSearchNode(neighbor_map, new_program)
            neighbor_map_str = neighbor_map.__str__()
            if neighbor_map_str not in seen:
                agenda.put((heuristic_plus_cost_from_node(neighbor_node), neighbor_node))
                seen.add(neighbor_map_str)
    return None
