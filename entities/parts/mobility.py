from entities.parts.part import Part
from entities.parts.database import parts


class Mobility( Part ) :
	def __init__( self, partId ):
		super().__init__( parts.MOBILITY, partId, external = True )

	@property
	def objectPath( self ) -> str:
		return "mobility"

	def _readPartData( self, part_data ):
		self.mobile_ability = part_data[ "mobile_ability" ]


class BasicTracks( Mobility ):
	def __init__( self ):
		super().__init__( "basic_tracks" )

class BasicWheels( Mobility ):
	def __init__( self ) :
		super().__init__( "basic_wheels" )
