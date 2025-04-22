from panda3d.core import BitMask32

from entities.parts.part import Part
from enums.colors import Color


class CubePart( Part ):
	def __init__( self, scale ):
		super( CubePart, self ).__init__( partId = "cube", scale = scale )
		self._objectPath = "obstacles"
		self._color = Color.GREEN
		self._mass = 10000


class SelectionCubePart( Part ):
	def __init__( self, scale ):
		super( SelectionCubePart, self ).__init__( mass = 0, partId = "cube", scale = scale, collideGroup = BitMask32.allOff() )
		self._objectPath = "obstacles"
		self._color = Color.RED_TRANSPARENT
		self._pseudoPart = True