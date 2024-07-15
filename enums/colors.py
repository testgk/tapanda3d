from enum import Enum
from panda3d.core import Vec4

class Color(Enum):
    RED = Vec4( 1, 0, 0, 1 )
    GREEN = Vec4( 0, 1, 0, 1 )
    BLUE = Vec4( 0, 0, 1, 1 )
    WHITE = Vec4( 1, 1, 1, 1 )
    BLACK = Vec4( 0, 0, 0, 1 )
    YELLOW = Vec4( 1, 1, 0, 1 )
    CYAN = Vec4( 0, 1, 1, 1 )
    MAGENTA = Vec4( 1, 0, 1, 1 )
