from entities.parts.part import Part
from enums.colors import Color


class Rolls( Part ):
	def __init__( self, rollType ):
		super().__init__( partId = f'{rollType}_rolls' )
		self._rigidBodyMask = 2
		self._color = Color.MAGENTA.value

	@property
	def objectPath( self ) -> str:
		return "mobility/rolls"
