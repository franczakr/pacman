import os
from map import WL, FR

path = './maps/'


def load_maps():
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if file.endswith('.map'):
                files.append(os.path.join(r, file))
    return files


def parse_map(map_file):
    print(str(map_file))
    file = open(map_file, 'r')
    content = file.read()
    map = []
    for line in content.split('\n'):
        map_line = []
        for map_tile in line.split():
            if map_tile == 'WL':
                map_line.append(WL)
            else:
                map_line.append(FR)
        map.append(map_line)
    return map
