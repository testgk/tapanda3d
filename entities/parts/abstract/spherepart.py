from panda3d.core import BitMask32

from entities.parts.part import Part
from enums.colors import Color


class SpherePart( Part ):
	def __init__( self, scale ):
		super().__init__( partId = "cube", scale = scale )
		self._objectPath = "obstacles"
		self._color = Color.GREEN
		self._mass = 10000
