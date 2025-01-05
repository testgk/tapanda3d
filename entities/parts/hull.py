from enums.colors import Color
from entities.parts.part import Part
from entities.parts.database import parts


class Hull( Part ):
	def __init__( self, partId ):
		super().__init__( parts.HULLS, partId, color = Color.GREEN, path = "hulls" )

	def _readPartData( self, part_data ):
		self.__armor = part_data[ "armor" ]


class BasicHull( Hull ):
	def __init__( self ):
		super().__init__( "basic_hull" )
