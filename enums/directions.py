from enum import Enum

class Direction( Enum ):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_RIGHT = 5
    UP_LEFT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

def allDirections():
    for direction in Direction:
        yield direction

mapDirections = {
    Direction.UP: (),
    Direction.DOWN: (),
    Direction.LEFT: (),
    Direction.RIGHT: (),
    Direction.UP_RIGHT: (),
    Direction.DOWN_LEFT: (),
    Direction.DOWN_RIGHT: (),
    Direction.UP_LEFT: (),
}

