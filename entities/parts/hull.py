from entities.parts.database import parts
from entities.parts.part import Part
from enums.colors import Color


class Hull( Part ):
	def __init__( self, partId ):
		super().__init__( parts.HULLS, partId )
		self._color = Color.GREEN.value
		self._rigidGroup = "hull_mobility"
		self.collideGroup = 4

	@property
	def objectPath( self ) -> str:
		return "hulls"

	def _readPartData( self, part_data ):
		self.armor = part_data[ "armor" ]


class BasicHull( Hull ):
	def __init__( self ):
		super().__init__( "basic_hull" )
