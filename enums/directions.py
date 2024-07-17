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
    Direction.UP: ( -1, 0 ),
    Direction.DOWN: ( 1, 0 ),
    Direction.LEFT: ( 0 ,1 ),
    Direction.RIGHT: ( 0, -1 ),
    Direction.UP_RIGHT: ( -1, -1 ),
    Direction.DOWN_LEFT: ( 1, 1 ),
    Direction.DOWN_RIGHT: ( -1, 1 ),
    Direction.UP_LEFT: ( 1, -1 ),
}

