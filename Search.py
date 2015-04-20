class GameMapSearchNode(object):
    """docstring for GameMapSearchNode"""
    def __init__(self, game_map, transformation, parent):
        super(GameMapSearchNode, self).__init__()
        self.parent = parent
        self.game_map = game_map
        self.transformation = transformation

    def get_tranformation_path(self):
        path = []
        node = self
        while node.transformation:
            transformation = node.transformation
            path.append(transformation)
            node = node.parent
        path.reverse()
        return path

def search(game_map, additional_function=None):
    start_node = GameMapSearchNode(game_map, None, None)
    agenda = [start_node]
    seen = set()
    depth = 0
    while agenda:
        depth += 1
        if depth > 4000:
            raise Exception('Search depth limit reached')
        node = agenda.pop(0)
        game_map = node.game_map
        game_map_str = game_map.__str__()
        seen.add(game_map_str)
        if game_map.check_if_solved():
            return node.get_tranformation_path()
        neighbor_maps, transformations = game_map.get_neighbor_maps_and_transformations(additional_function)
        for neighbor_map, transformation in zip(neighbor_maps, transformations):
            neighbor_node = GameMapSearchNode(neighbor_map, transformation, node)
            neighbor_map_str = neighbor_map.__str__()
            if neighbor_map_str not in seen:
                agenda.append(neighbor_node)
                seen.add(neighbor_map_str)
    return None
