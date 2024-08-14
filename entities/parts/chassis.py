from entities.parts.part import Part
from entities.parts.partsdb import parts


class Chassis( Part ) :
	def __init__( self, partId ):
		super().__init__( parts.CHASSIS, partId, external = True )

	@property
	def objectPath( self ) -> str:
		return "chassis"

	def _readPartData( self, part_data ):
		self.mobility = part_data[ "mobility" ]


class BasicTracksChassis( Chassis ):
	def __init__( self ):
		super().__init__( "basic_tracks" )

class BasicWheelsChassis( Chassis ):
	def __init__( self ) :
		super().__init__( "basic_wheels" )
