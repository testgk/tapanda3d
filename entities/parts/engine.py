from entities.parts.part import Part
from entities.parts.database import parts


class Engine( Part ):
	def __init__( self, partId ):
		super().__init__( parts.ENGINES, partId, isRendered = False )

	@property
	def objectPath( self ):
		return "engines"


class BasicEngine( Engine ):
	def __init__( self ):
		super().__init__( "basic_engine" )