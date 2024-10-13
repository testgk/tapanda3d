from panda3d.core import BitMask32



class CollisionGroup:
    GROUP_PICKER = BitMask32.bit( 0 )  # Group for the picker
    GROUP_TERRAIN = BitMask32.bit( 1 )  # Group for the terrain
    GROUP_MODEL = BitMask32.bit( 2 )  # Group for the car
    GROUP_ROLLS = BitMask32.bit( 3 )