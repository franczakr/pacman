FLOOR = 0
WALL = 1
TILESIZE = 50
MAPWIDTH = 16
MAPHEIGHT = 16


class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Position) and self.y == other.y and self.x == other.x

    def __hash__(self):
        return hash((self.x, self.y))


class Map:
    tilemap = []
    fruits = set()
    tiles_to_repaint = set()

    def init_map(self):
        self.tilemap = [
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
        ]

    def init_fruits(self):
        for x in range(1, MAPWIDTH - 1):
            for y in range(1, MAPHEIGHT - 1):
                if self.tilemap[y][x] == FLOOR:
                    self.fruits.add(Position(x, y))
