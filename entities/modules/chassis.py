from entities.modules.module import Module
from entities.parts.hull import Hull, BasicHull
from entities.parts.mobility import Mobility, BasicTracks, BasicWheels
from entities.parts.part import Part


class Chassis( Module ) :
	def __init__( self, hull: Hull, mobility: Mobility ):
		self._hull = hull
		self._mobility = mobility
		super().__init__( [ self._hull, self._mobility ] )

	def mobility( self ) -> Part:
		return self._mobility

	def hull( self ) -> Part:
		return self._hull

class BasicTracksChassis( Chassis ):
	def __init__( self ):
		super().__init__( BasicHull(), BasicTracks() )

class BasicWheelsChassis( Chassis ):
	def __init__( self ) :
		super().__init__( BasicHull(), BasicWheels() )
