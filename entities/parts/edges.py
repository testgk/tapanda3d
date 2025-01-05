from enums.colors import Color
from entities.parts.part import Part
from entities.parts.database import parts


class Edege( Part ):
	def __init__( self, partId ):
		super().__init__( parts.HULLS, partId, color = Color.GREEN.value, path = "edges", mass = 0 )


class RightEdge( Edege ):
	def __init__( self ):
		super().__init__( "right_edge" )

class LeftEdge( Edege ):
	def __init__( self ):
		super().__init__( "left_edge" )
