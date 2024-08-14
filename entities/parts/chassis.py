from entities.parts.part import Part
from entities.parts.partsdb import parts


class Chassis( Part ) :
	def __init__( self, partId ):
		super().__init__( parts.CHASSIS, partId )

class BasicTracksChassis( Chassis ):
	def __init__( self ):
		super().__init__( "basic_tracks" )

class BasicWheelsChassis( Chassis ):
	def __init__( self ) :
		super().__init__( "basic_wheels" )
