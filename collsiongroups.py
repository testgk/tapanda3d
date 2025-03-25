from panda3d.core import BitMask32



class CollisionGroup:
    PICKER = BitMask32( 0 )
    TERRAIN = BitMask32( 1 )
    MODEL = BitMask32( 4 )
    ROLLS = BitMask32( 2 )
    TURRET = BitMask32( 8 )
