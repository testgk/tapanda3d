from enum import Enum
from panda3d.core import LVecBase4f




class Color:
    # Direct constants without using Enum
    RED = LVecBase4f( 1, 0, 0, 1 )
    GREEN = LVecBase4f( 0, 1, 0, 1 )
    BLUE = LVecBase4f( 0, 0, 1, 1 )
    WHITE = LVecBase4f( 1, 1, 1, 1 )
    BLACK = LVecBase4f( 0, 0, 0, 1 )
    YELLOW = LVecBase4f( 1, 1, 0, 1 )
    ORANGE = LVecBase4f( 1, 0.5, 0, 1 )
    CYAN = LVecBase4f( 0, 1, 1, 1 )
    MAGENTA = LVecBase4f( 1, 0, 1, 1 )
    RED_TRANSPARENT = LVecBase4f( 1, 0, 0, 0.5 )