from map import Position


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(map, start, end):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = Position(current_node.position.x + new_position[0],
                                     current_node.position.y + new_position[1])

            if node_position.y > (len(map) - 1) or node_position.y < 0 or node_position.x > (len(map[len(map)-1]) - 1)\
                    or node_position.x < 0:
                continue

            if map[node_position.y][node_position.x] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            flag = False
            for closed_child in closed_list:
                if child == closed_child:
                    flag = True
                    break
            if flag:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position.y - end_node.position.y) ** 2) + ((child.position.x - end_node.position.x) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node:
                    flag = True
                    if child.g < open_node.g:
                        open_list.remove(open_node)
                        open_list.append(child)
                    break
            if flag:
                continue

            open_list.append(child)
