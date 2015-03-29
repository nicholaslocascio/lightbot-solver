"""Define Map Class"""

import copy

class GameMap(object):
    """Map"""

    def __init__(self, robot, cells, width, height):
        self.robot = robot
        self.cells = cells
        self.width = width
        self.height = height

    def __str__(self):
        topography_string_lines = []
        feature_string_lines = []
        robot_string_lines = []
        rx, ry = self.robot.coordinates()
        for y in range(self.height):
            topography_line = ""
            feature_line = ""
            robot_line = ""
            for x in range(self.width):
                cell = self.get_cell(x, y)
                topography_line += cell.topography
                if cell.topography == '-':
                    feature_line += '-'
                    robot_line += '-'
                else:
                    feature_line += cell.feature
                    if rx == x and ry == y:
                        robot_line += self.robot.get_orientation_string()
                    else:
                        robot_line += 'x'

            topography_string_lines.append(topography_line)
            feature_string_lines.append(feature_line)
            robot_string_lines.append(robot_line)

        strings = ['\n'.join(topography_string_lines), '\n'.join(feature_string_lines), '\n'.join(robot_string_lines)]
        full_string = '\n\n'.join(strings)
        return full_string

    @staticmethod
    def game_map_from_strings(topography, features, robot_features):
        robot = Robot.robot_from_string(robot_features)
        topography_lines = topography.split('\n')
        features_lines = features.split('\n')
        if len(topography_lines) is not len(features_lines) \
        and len(topography_lines[0]) is not len(features_lines[0]):
            raise Exception('size mismatch')
        height = len(topography_lines)
        width = len(topography_lines[0])
        cells = {}
        y = 0
        for top_line,features_line in zip(topography_lines, features_lines):
            x = 0
            for topography_char, feature_char in zip(top_line, features_line):
                cell = Cell(x, y, topography_char, feature_char)
                cells[x, y] = cell
                x += 1
            y += 1
        return GameMap(robot, cells, width, height)

    def get_cell(self, x, y):
        return self.cells[x, y]

    def __copy__(self):
        new_cells = copy.deepcopy(self.cells)
        new_robot = copy.copy(self.robot)
        return GameMap(new_robot, new_cells, self.width, self.height)

    @staticmethod
    def transform_map_turn_cc(game_map):
        game_map.robot.turn_counter_clockwise()
        return game_map

    @staticmethod
    def transform_map_turn_c(game_map):
        game_map.robot.turn_clockwise()
        return game_map

    @staticmethod
    def transform_map_go_forward(game_map):
        game_map.robot.go_forward()
        return game_map

    @staticmethod
    def transform_map_activate(game_map):
        x, y = game_map.robot.coordinates()
        cell = game_map.get_cell(x, y)
        if cell.feature is "l":
            cell.feature = "L"
        elif cell.feature is "L":
            cell.feature = "l"
        return game_map

    def check_if_solved(self):
        for pos, cell in self.cells.iteritems():
            #print "feat ", cell.feature
            if cell.feature is 'l':
                return False
        return True

    @staticmethod
    def is_valid_map(game_map):
        x, y = game_map.robot.coordinates()
        in_bounds = (x >= 0 and y >= 0 and x < game_map.width and y < game_map.height)
        if in_bounds:
            cell = game_map.get_cell(x, y)
            if cell.is_valid():
                return True
        return False

    @staticmethod
    def tranformation_from_tranform_function(transform):
        if transform is GameMap.transform_map_turn_cc:
            return 'l'
        elif transform is GameMap.transform_map_turn_c:
            return 'r'
        elif transform is GameMap.transform_map_activate:
            return 'a'
        elif transform is GameMap.transform_map_go_forward:
            return 'f'

    def get_neighbor_maps_and_transformations(self):
        valid_transform_functions = [\
        GameMap.transform_map_turn_cc, 
        GameMap.transform_map_turn_c,
        GameMap.transform_map_go_forward,
        GameMap.transform_map_activate]
        neighbor_maps = []
        transformations = []
        for transform in valid_transform_functions:
            new_map = copy.copy(self)
            new_map = transform(new_map)
            transformation = GameMap.tranformation_from_tranform_function(transform)
            if GameMap.is_valid_map(new_map):
                neighbor_maps.append(new_map)
                transformations.append(transformation)
        return neighbor_maps, transformations

class Cell(object):
    """Cell"""
    def __init__(self, x, y, topography, feature):
        self.x = x
        self.y = y
        self.feature = feature
        self.topography = topography

        if topography is not '-':
            self.z = int(topography)
        else:
            self.z = None

    def is_valid(self):
        return (self.topography is not '-')

    def coordinates(self):
        return (self.x, self.y)

    def __copy__(self):
        return Cell(self.x, self.y, self.topography, self.feature)


class Robot(object):
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation

    @staticmethod
    def orientation_from_string(orientation_char):
        if orientation_char is 'E':
            return 0
        elif orientation_char is 'N':
            return 90
        elif orientation_char is 'W':
            return 180
        elif orientation_char is 'S':
            return 270
        raise Exception('Invalid Orientation: ' + str(orientation_char))

    def get_orientation_string(self):
        if self.orientation == 0:
            return 'E'
        elif self.orientation == 90:
            return 'N'
        elif self.orientation == 180:
            return 'W'
        elif self.orientation == 270:
            return 'S'
        raise Exception('Invalid Orientation: ' + str(self.orientation))

    def __copy__(self):
        return Robot(self.x, self.y, self.orientation)

    def coordinates(self):
        return (self.x, self.y)

    def turn_clockwise(self):
        self.orientation = (self.orientation-90)%360

    def turn_counter_clockwise(self):
        self.orientation = (self.orientation+90)%360

    def get_direction_vector(self):
        if self.orientation == 0:
            return [1, 0]
        elif self.orientation == 90:
            return [0, -1]
        elif self.orientation == 180:
            return [-1, 0]
        elif self.orientation == 270:
            return [0, 1]
        raise Exception('Invalid Orientation: ' + str(self.orientation))


    def go_forward(self):
        direction = self.get_direction_vector()
        self.x += direction[0]
        self.y += direction[1]

    @staticmethod
    def robot_from_string(featureString):
        lines = featureString.split('\n')
        y = 0
        for line in lines:
            x = 0
            for featureChar in line:
                if featureChar in {'N', 'W', 'E', 'S'}:
                    return Robot(x, y, Robot.orientation_from_string(featureChar))
                x += 1
            y += 1
        raise Exception('No Robot Found')
