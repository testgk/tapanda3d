from collsiongroups import CollisionGroup
from entities.parts.part import Part
from enums.colors import Color


class Rolls( Part ):
	def __init__( self, rollType ):
		super().__init__( partId = f'{rollType}_rolls' )
		self._color = Color.MAGENTA.value
		self.collideGroup = CollisionGroup.ROLLS

	@property
	def objectPath( self ) -> str:
		return "mobility/rolls"
