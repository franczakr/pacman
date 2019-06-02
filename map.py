FR = 0
WL = 1
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

    def __init__(self, tilemap):
        self.tilemap = tilemap

    def init_fruits(self):
        for x in range(1, MAPWIDTH - 1):
            for y in range(1, MAPHEIGHT - 1):
                if self.tilemap[y][x] == FR:
                    self.fruits.add(Position(x, y))
